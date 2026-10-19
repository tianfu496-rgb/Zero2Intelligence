# Transformer 与注意力学习笔记

> 本笔记根据“Transformer 实战营”六份公开课课件整理，覆盖文本表示、注意力、Encoder–Decoder、Decoder-Only 训练、自回归推理、KV Cache 以及 Attention 中 Softmax 的 GPU 优化。它侧重理解“数据怎样流动、每个张量在做什么、如何验证模型是否正确”。

## 1. 全局学习地图

Transformer 的完整链路可以概括为：

```text
原始文本
  → Tokenizer / Token ID
  → Token Embedding + Position Encoding
  → Attention / Transformer Blocks
  → Logits
  → Loss（训练）或下一个 Token（推理）
```

以机器翻译为例：

```text
英文句子 → 编码器生成上下文表示
        → 解码器基于目标前缀逐词生成中文句子
```

学习 Transformer 要同时抓住两条线：

1. **原理线**：注意力到底如何让 token 根据上下文选择信息。
2. **工程线**：张量形状、Mask、Loss、训练日志、Checkpoint 与推理性能如何验证。

---

## 2. 从硬对齐到软对齐

### 2.1 为什么不能逐词直译

早期机器翻译可理解成“一个源词对应一个目标词”的硬对齐。例如：

```text
I → 我，love → 爱，you → 你
```

但自然语言依赖上下文和语法结构。例如 `bank` 在 `river bank` 中更可能是“河岸”，在 `money bank` 中更可能是“银行”。逐词固定映射无法区分这种语义。

### 2.2 软对齐思想

注意力机制引入**软对齐**：生成或理解当前 token 时，不是只选一个词，而是为上下文中每个 token 分配一个连续权重。权重越大，说明当前位置更应参考该 token 的信息。

```text
当前 token 的需求
      ↓
计算与各上下文 token 的相关度
      ↓
Softmax 归一化为权重
      ↓
对上下文信息加权求和
```

注意力比较的是 token 的**向量表示**，不是直接比较文字本身。因此先有 token id 与 embedding，后有注意力计算。

---

## 3. 文本如何变成模型输入

### 3.1 Token、词表与 Token ID

神经网络只能处理数值张量。Tokenizer 将文本切成 token，并由词表（Vocabulary）将每个 token 映射为唯一整数 id。

```text
文本：我 爱 编程 。
Token：我 | 爱 | 编程 | 。
ID：  101 102 103 104
```

常见特殊 token：

| Token | 作用 |
| --- | --- |
| `<PAD>` | 补齐不同长度的序列，使一个 batch 具有相同长度 |
| `<BOS>` / `<SOS>` | 序列起始符，提示生成开始 |
| `<EOS>` | 序列结束符，提示生成停止 |
| `<UNK>` | 词表外（OOV）token 的占位符 |

特殊 token 的编号没有绝对固定规则，以**实际 tokenizer/词表**为准。训练、推理、加载 checkpoint 时必须使用配套词表，否则同一个 id 可能代表不同 token。

### 3.2 BPE 子词分词

BPE（Byte Pair Encoding）从细粒度符号开始，反复统计相邻符号对的频率，并合并最高频的一对。它处在“按词切分”和“按字符切分”之间：

- **词级**：序列短，但词表大，未登录词问题明显。
- **字符级**：词表小且几乎没有未知词，但序列长。
- **子词级 BPE**：高频片段作为整体，罕见词拆成多个子词，兼顾词表规模与泛化能力。

训练 BPE 得到的合并规则与词表是模型输入定义的一部分，不能随意替换。

### 3.3 Embedding

Token ID 只是离散编号，不表示语义距离。Embedding 层是一个可学习矩阵：

$$
E\in\mathbb{R}^{V\times d_{model}}
$$

其中 $`V`$ 是词表大小。输入 id 为 $`i`$ 时，模型取出矩阵第 $`i`$ 行，得到 $`d_{model}`$ 维向量。

若 batch 大小为 $`B`$、序列长度为 $`T`$，则：

```text
input_ids:       (B, T)
token_embedding: (B, T, d_model)
```

---

## 4. 位置编码

### 4.1 为什么需要位置信息

注意力会并行处理所有位置，本身不区分 token 顺序。于是“猫追狗”和“狗追猫”在仅看词集合时没有差别，但语义完全相反。

位置编码（Position Encoding, PE）为每个位置提供位置信息，并与 token embedding 相加：

$$
X=TokenEmbedding+PositionalEncoding
$$

相加要求二者最后一维相同，结果仍为 `(B, T, d_model)`。

### 4.2 原始 Transformer 的正弦位置编码

对位置 $`pos`$ 和向量维度组 $`i`$：

$$
PE(pos,2i)=\sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$

$$
PE(pos,2i+1)=\cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$

- $`pos`$：token 在序列中的位置，从 0 开始。
- $`i`$：位置编码向量内部的维度组编号。
- $`d_{model}`$：模型隐藏维度。

不同维度使用不同频率的 sin/cos，使模型能从向量中推断相对或绝对位置信息。现代模型也会使用可学习位置编码、RoPE 等方案；核心目的相同：让模型知道顺序。

---

## 5. 缩放点积注意力

### 5.1 Q、K、V 的含义

输入表示 $`X`$ 分别经过三组可学习线性变换：

$$
Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V
$$

可以这样直观理解：

| 向量 | 问题 | 作用 |
| --- | --- | --- |
| Query（Q） | 我现在需要什么信息？ | 发起查询 |
| Key（K） | 我能提供什么线索？ | 与 Query 匹配 |
| Value（V） | 我实际携带什么内容？ | 按注意力权重被汇总 |

Q、K、V 并不是三份外部输入，而通常是对同一输入或不同来源表示做不同的线性投影。

### 5.2 公式与计算步骤

缩放点积注意力（Scaled Dot-Product Attention）：

$$
Attention(Q,K,V)=\operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}+M\right)V
$$

其中 $`M`$ 为可选的 mask。

计算过程：

1. **打分**：$`S=QK^T`$，得到每个 Query 对所有 Key 的相关度。
2. **缩放**：除以 $`\sqrt{d_k}`$，避免维度大时点积数值过大、Softmax 过度饱和。
3. **加 Mask**：禁止关注的位置加上极小值（实现中常为 `-inf` 或很小的负数）。
4. **归一化**：$`A=softmax(S)`$，每一行成为概率分布。
5. **加权汇总**：输出 $`O=AV`$。

若 `Q` 的形状为 `(B, H, Lq, d_k)`，`K` 为 `(B, H, Lk, d_k)`，则：

```text
scores = Q @ K.transpose(-2, -1)  # (B, H, Lq, Lk)
weights = softmax(scores, dim=-1) # 最后一维之和为 1
output = weights @ V              # (B, H, Lq, d_v)
```

### 5.3 Self-Attention 与 Cross-Attention

- **Self-Attention**：Q、K、V 都来自同一序列。每个 token 从本序列中聚合上下文。
- **Cross-Attention**：Q 来自解码器当前表示，K、V 来自编码器输出。解码器借此读取源语言信息。

### 5.4 多头注意力

多头注意力（Multi-Head Attention）将隐藏维度切成 $`h`$ 个头，在不同子空间中独立计算注意力，再拼接投影：

$$
MultiHead(Q,K,V)=Concat(head_1,...,head_h)W_O
$$

常见关系为：

$$
d_k=d_{model}/h
$$

多头机制让模型可以并行学习不同关联模式，例如局部搭配、长距离依赖、指代关系等。

---

## 6. Mask：模型“能看什么”的规则

Mask 不会删除 token，而是在 Softmax **之前**修改 attention score，使禁止位置在 Softmax 后得到接近 0 的权重。

### 6.1 Padding Mask

同一 batch 中句子长度不同，短句用 `<PAD>` 补齐。Padding Mask 屏蔽补齐位置，避免模型把注意力分给无意义的 PAD。

```text
真实序列：<BOS> 我 爱 <EOS>
补齐后：  <BOS> 我 爱 <EOS> <PAD> <PAD>
```

无论当前 Query 位于哪里，Key/Value 中的 `<PAD>` 都应被屏蔽。

### 6.2 Causal Mask

Causal Mask（因果掩码）用于自回归解码，保证位置 $`i`$ 只能关注当前位置和左侧位置 $`j\le i`$：

$$
M_{i,j}=\begin{cases}
0,&j\le i\\
-\infty,&j>i
\end{cases}
$$

例如长度为 4 的下三角可见关系：

```text
位置 0：可看 0
位置 1：可看 0, 1
位置 2：可看 0, 1, 2
位置 3：可看 0, 1, 2, 3
```

若不使用 Causal Mask，训练位置可以直接读取右侧的真实答案，造成信息泄漏。下三角 mask 让所有位置仍能并行计算，同时保证每个位置看到的上下文符合真实生成时的条件。

### 6.3 三处注意力使用什么 Mask

| 位置 | 注意力类型 | 常用 Mask |
| --- | --- | --- |
| Encoder | Self-Attention | 源序列 Padding Mask |
| Decoder 第一层注意力 | Masked Self-Attention | 目标序列 Padding Mask + Causal Mask |
| Decoder 第二层注意力 | Cross-Attention | 源序列 Padding Mask |

两种 mask 合并时必须确认框架接口的布尔语义：有的 API 中 `True` 表示“屏蔽”，有的 API 中 `True` 表示“保留”。不要凭习惯判断，应打印小矩阵或写单元测试验证每一位。

---

## 7. Encoder–Decoder Transformer

### 7.1 Encoder 的职责

Encoder 双向读取完整源序列，生成带上下文的表示。单个 Encoder Layer 通常包括：

```text
输入
 → Multi-Head Self-Attention
 → Residual Add + LayerNorm
 → Feed-Forward Network（FFN）
 → Residual Add + LayerNorm
```

FFN 对每个位置独立进行相同的非线性变换，常写作：

$$
FFN(x)=\sigma(xW_1+b_1)W_2+b_2
$$

经过 $`N`$ 层后，编码器输出 `memory`，形状通常为 `(B, S, d_model)`，其中 $`S`$ 是源序列长度。

### 7.2 Decoder 的职责

Decoder 根据已生成的目标前缀和编码器 `memory`，预测下一个目标 token。一个 Decoder Layer 包含：

```text
目标表示
 → Masked Self-Attention
 → Add + Norm
 → Cross-Attention（读取 encoder memory）
 → Add + Norm
 → FFN
 → Add + Norm
```

Decoder 最后经过线性层 `LM Head` 映射到词表大小，产生 logits：

```text
decoder_hidden: (B, T, d_model)
logits:         (B, T, vocab_size)
```

### 7.3 机器翻译数据流

```text
源句：i love you
  → 源 Token ID + 位置编码
  → Encoder
  → encoder memory

目标前缀：<BOS> 我 爱
  → Decoder（自注意力只能看左侧）
  → Cross-Attention 读取 encoder memory
  → 预测：你
  → 最终输出：我 爱 你 <EOS>
```

Encoder–Decoder 很适合源序列和目标序列角色明确的任务，如翻译、摘要和改写。

---

## 8. 训练：Teacher Forcing、标签右移与 Loss

### 8.1 Teacher Forcing

训练时已知正确目标序列，Decoder 输入真实的前缀，而不是模型上一步生成结果。

```text
Decoder 输入：<BOS> 我 爱 你
监督标签：  我 爱 你 <EOS>
```

这就是**标签右移（Label Shift）**：输入与目标长度一致，目标相对输入左移一位。它定义了每个位置“要预测谁”。

### 8.2 为什么训练能并行

虽然推理时需要逐 token 生成，但训练时可把完整目标序列一次输入 Decoder。Causal Mask 会为每个位置限制可见前缀，因此一次前向传播可以同时计算所有位置的 logits。

```text
输入位置 0：只看 <BOS>，预测“我”
输入位置 1：看 <BOS> 我，预测“爱”
输入位置 2：看 <BOS> 我 爱，预测“你”
```

### 8.3 Logits、Softmax 与交叉熵

Logits 是模型对词表每个 token 输出的原始分数。Softmax 将它们转成概率：

$$
p(y=k)=\frac{e^{z_k}}{\sum_j e^{z_j}}
$$

单个位置的交叉熵损失为：

$$
Loss=-\log p(y_{true})
$$

正确 token 的概率越低，Loss 越大。实际实现一般直接使用 `CrossEntropyLoss`，不要先手动做 Softmax，以避免数值稳定性问题。

### 8.4 PAD 不参与 Loss 与 Accuracy

PAD 仅用于凑齐长度，不是模型需要学习的真实内容。因此：

- Loss 使用 `ignore_index=pad_id` 或等价机制。
- Accuracy 只在非 PAD 的有效位置统计。

否则模型只要猜中大量 PAD，就可能得到虚高准确率。

### 8.5 一次训练 Step

```text
读取 batch 的 inputs / targets
      ↓
Forward：得到 logits 和 loss
      ↓
Backward：计算各参数梯度
      ↓
可选：Gradient Clipping
      ↓
optimizer.step()：更新参数
      ↓
optimizer.zero_grad()：清除旧梯度
```

只有执行 `optimizer.step()`，参数才真正学习。梯度裁剪用于限制异常大的梯度范数，降低训练发散风险。

### 8.6 验证与 Checkpoint

训练集参与反向传播和参数更新；验证集只做 forward，用于衡量模型的泛化能力。不要仅凭训练 Loss 判断模型有效。

一个可恢复的 checkpoint 至少应保存：

| 内容 | 用途 |
| --- | --- |
| `model state_dict` | 已学到的模型参数 |
| `optimizer state_dict` | 动量、二阶矩等优化器状态，支持精确续训 |
| metadata | step、模型配置、词表/数据位置、验证指标等 |

加载时应先用配置重建相同结构，再加载权重；同时确保 tokenizer、BPE 规则与 checkpoint 配套。

---

## 9. Decoder-Only 与 GPT 类模型

### 9.1 与 Encoder–Decoder 的区别

| 架构 | 信息流 | 典型任务 |
| --- | --- | --- |
| Encoder–Decoder | Encoder 双向读源序列；Decoder 读目标左侧并 Cross-Attention 读 Encoder 输出 | 翻译、摘要、序列到序列生成 |
| Decoder-Only | 单条序列，只用 Causal Self-Attention 读左侧上下文 | 通用续写、对话、代码生成 |
| Encoder-Only | 双向 Self-Attention 读完整输入 | 分类、检索、表征、抽取 |

Decoder-Only 不是简单“删掉 Encoder”，而是把条件、上下文和目标组织成一条 token 序列，并统一为**预测下一个 token**的训练目标。

### 9.2 Decoder-Only 前向结构

```text
Token IDs (B, T)
  → Token Embedding (B, T, C)
  → N × Decoder Block
  → Final Norm + LM Head
  → Logits (B, T, V)
```

单个 Decoder Block 常见结构：

```text
x
 → Norm → Causal Self-Attention → Residual Add
 → Norm → MLP                   → Residual Add
```

其中：

- `B`：batch size。
- `T`：sequence length。
- `C`：hidden dimension。
- `V`：vocabulary size。

### 9.3 标签右移与 Causal Mask 的分工

这是最容易混淆的一点：

| 机制 | 解决的问题 |
| --- | --- |
| Label Shift | 定义当前位置的正确答案，即“要预测什么” |
| Causal Mask | 限制当前位置可读取的上下文，即“允许看什么” |

两者必须同时存在。只有标签右移但没有因果约束，会发生未来信息泄漏；只有因果约束却没有正确 targets，则没有训练监督信号。

---

## 10. 推理：自回归生成与解码策略

### 10.1 自回归生成

推理阶段没有真实目标序列，模型每次将刚预测出的 token 拼回输入，继续预测下一个 token：

```text
Prompt
  → 模型输出 logits
  → 选择下一个 token
  → 追加到上下文
  → 重复，直到 <EOS> 或达到最大长度
```

训练时的 Teacher Forcing 与推理时的自回归输入不同，这种差异也称为 exposure bias。

### 10.2 贪心与采样

- **Greedy Decoding**：每步选择概率最高的 token。结果确定，适合正确性验证和性能基准，但可能重复或落入局部模式。
- **Sampling**：按概率分布随机采样，文本更多样，但结果不完全可复现。
- **Temperature**：调节分布尖锐程度。温度低时更确定，温度高时更随机。
- **Top-k**：只在概率最高的 k 个候选中采样。
- **Top-p**：在累计概率达到阈值 p 的最小候选集合中采样。

做 Cache 与 No-Cache 的正确性对比、性能对比时，应固定模型、输入、最大生成长度和解码规则，通常采用 `temperature=0` 的贪心解码。

---

## 11. KV Cache、Prefill 与 Decode

### 11.1 两个推理阶段

```text
Prompt → Prefill → 首个 token
首个 token 之后 → Decode 循环 → 后续 token
```

- **Prefill**：一次处理完整 prompt，建立历史上下文，主要影响首 token 延迟。
- **Decode**：每次只生成一个新 token，主要影响持续生成速度。

### 11.2 KV Cache 的作用

在每层注意力中，历史 token 的 K、V 对于后续生成不会改变。没有 Cache 时，每生成一个 token 都要重算完整历史的 K、V；使用 KV Cache 后：

1. Prefill 时计算并保存历史 K、V。
2. Decode 时只计算新 token 的 K、V。
3. 将新 K、V 追加到缓存，Q 与历史缓存做注意力。

因此 KV Cache 通常降低 Decode 阶段的重复计算，提高持续生成吞吐；代价是额外显存。它对 TTFT 的影响通常较小，对 TPOT 的影响更直接。

### 11.3 推理性能指标

| 指标 | 含义 | 主要受什么影响 |
| --- | --- | --- |
| TTFT | Time To First Token，从请求到首 token 的时间 | prompt 长度、Prefill 计算 |
| TPOT | Time Per Output Token，首 token 后每个输出 token 的时间 | Decode 效率、KV Cache |
| TPS / tok/s | 每秒生成 token 数 | batch、硬件利用率、Decode 效率 |
| E2E | 端到端总时延 | Prefill、Decode、生成长度 |
| Peak VRAM | 峰值显存 | 模型参数、batch、序列长度、KV Cache |
| GPU Utilization | GPU 忙碌程度 | 数据供给、并行度、算子效率 |

实验需先验证 Cache 与 No-Cache 的贪心输出逐 token 一致，再比较性能。仅比较一次运行的总耗时不够，应固定 shape/dtype、预热、多次重复，并报告统计量。

---

## 12. Attention 中的 Softmax

### 12.1 Softmax 位于哪里

Attention 的常见实现：

```python
scores = q @ k.transpose(-2, -1) / scale
scores = scores.masked_fill(mask == 0, -1e9)
attn = torch.softmax(scores, dim=-1)
out = attn @ v
```

对于 scores 的形状 `(B, H, Lq, Lk)`：

- `B`：batch size。
- `H`：attention heads。
- `Lq`：query length。
- `Lk`：key length。
- Softmax 沿最后一维 `Lk` 进行，每一个 query 对所有 key 得到概率分布。

可把高维张量视为很多条独立行：

```text
rows = B × H × Lq
cols = Lk
```

每一行都独立完成 max、exp/sum 和归一化。

### 12.2 稳定 Softmax

直接计算 $`\exp(x_i)`$ 可能溢出。数值稳定的 Softmax 先减去该行最大值：

$$
softmax(x_i)=\frac{\exp(x_i-\max(x))}{\sum_j\exp(x_j-\max(x))}
$$

计算可分为三步：

1. 沿行规约得到 `row_max`。
2. 计算 `exp(x - row_max)` 并规约求和。
3. 每个元素除以行和，写回输出。

减去最大值不改变 Softmax 结果，因为分子分母同时乘了相同常数；同时可保证最大指数项为 `exp(0)=1`。

### 12.3 GPU 中的三种并行映射

课件以 Softmax 为例对比三种实现思路：

| 版本 | 一行由谁处理 | 规约方式 | 特点 |
| --- | --- | --- | --- |
| v1 | 一个线程 | 串行扫描 | 简单、正确，宽行时循环过长 |
| v2 | 一个 block | shared memory 树形规约 | 行内并行度高，适合较宽行，但同步成本高 |
| v3 | 一个 wave | 寄存器 + shuffle | 避免共享内存与块级同步，中窄行常更有优势 |

在特定教学环境中，v3 在中窄行常表现较好，v2 在超宽行可能反超；成熟算子库通常会依据 shape、dtype 与硬件选择更合适的实现。因此不要根据单一 shape 宣称某个 kernel 永远最快。

### 12.4 自定义算子是否值得接回模型

“能运行”不代表“值得替换框架实现”。至少需要三类证据：

1. **正确性**：与高精度参考实现比较；检查最大绝对误差、行和误差、NaN/Inf、极端输入和 Mask 语义。
2. **算子性能**：在目标硬件与真实 shape 上预热、多次测量，比较中位数/均值和波动。
3. **端到端收益**：接回真实 Transformer 后，确认最终 logits 或任务输出一致，且整体延迟确有稳定改善。

优化闭环：

```text
Profiling 定位瓶颈
  → 判断计算/访存/调度限制
  → 选择库、融合或手写 kernel
  → 正确性与性能验证
  → 端到端验证后再接入
```

---

## 13. 训练与性能排查清单

### 13.1 训练前

- tokenizer、词表、BPE 合并规则和 checkpoint 是否配套。
- `<PAD>` 的真实 id 是否已确认，是否假定它一定为 0。
- 输入、目标和 logits 形状是否分别符合预期。
- Padding Mask、Causal Mask 的方向和布尔语义是否用小矩阵验证。
- dtype、设备和后端是否可用。

### 13.2 训练中

- Loss 是否为有限值，是否总体下降。
- 是否发生 NaN、Inf 或 OOM。
- Accuracy 和 Loss 是否忽略 PAD。
- 验证集是否独立于训练集，验证阶段是否没有 backward/step。
- batch 增大后，吞吐是否真实提升，还是只增加显存占用。
- GPU 利用率低时，先检查数据加载和数据传输，不要直接归因于硬件。

### 13.3 推理与优化中

- Cache 与 No-Cache 在贪心解码下是否输出一致。
- 是否在同一模型、dtype、prompt、batch、生成长度和解码参数下比较。
- 是否区分 TTFT、TPOT、TPS 与 E2E，而非只看总时长。
- 手写算子是否首先通过正确性和真实 shape 的 benchmark。

---

## 14. 高频问答

### Q1：Attention 为什么要除以 $`\sqrt{d_k}`$？

当 $`d_k`$ 增大，Q 和 K 点积的数值方差也会增大。过大的分数会让 Softmax 分布过尖，梯度变小。缩放可以保持数值范围更稳定。

### Q2：Q、K、V 为什么不能只用一个向量？

它们来自不同的可学习投影，使模型能分别学习“查询需求”“匹配线索”和“传递内容”。若完全共用表示，表达灵活性会受限。

### Q3：Padding Mask 与 Causal Mask 有什么区别？

Padding Mask 屏蔽的是无意义的补齐 token；Causal Mask 屏蔽的是未来 token，防止生成训练时偷看答案。Decoder Self-Attention 往往同时需要两者。

### Q4：为什么训练时能并行，而推理时通常不能？

训练时完整目标序列已知，Causal Mask 能在一次矩阵计算中模拟每个前缀；推理时下一个 token 未知，必须先生成它才能作为下一步输入。

### Q5：Label Shift 与 Causal Mask 能互相替代吗？

不能。Label Shift 指定监督标签，Causal Mask 限制可见范围，二者解决不同问题。

### Q6：KV Cache 改变模型输出吗？

正确实现下不会。它只缓存历史 K/V、避免重复计算，应与无缓存推理给出相同的确定性输出。输出不一致通常说明缓存索引、位置编码、mask 或数值路径存在问题。

### Q7：为什么成熟库往往比手写 kernel 快？

成熟库通常已针对不同 shape、数据类型和硬件特征调优，并会在多个实现之间选择。手写 kernel 的价值在于理解机制、针对特殊真实 shape 做优化，或探索算子融合；不应默认它一定更快。

---

## 15. 复习路线

1. 先掌握 Token、Embedding、位置编码与张量形状。
2. 手推一次 $`QK^T`$、Softmax、加权 V 的注意力计算。
3. 用小矩阵分别验证 Padding Mask 和 Causal Mask。
4. 画出 Encoder–Decoder 的三处注意力及其 Q/K/V 来源。
5. 理解标签右移、Teacher Forcing、交叉熵、PAD 忽略和一次训练 step。
6. 对比 Encoder–Decoder 与 Decoder-Only 的信息流。
7. 用同一模型对比贪心/采样、Cache/No-Cache，并记录 TTFT、TPOT、TPS、显存。
8. 最后学习稳定 Softmax 与 GPU 上的规约方式，建立“正确性优先、真实负载验证”的优化习惯。
