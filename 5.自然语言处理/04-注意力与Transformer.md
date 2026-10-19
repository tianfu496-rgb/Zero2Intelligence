# 注意力与 Transformer

[仓库首页](../README.md) · [本主题目录](README.md) · [上一章：序列建模与机器翻译](03-序列建模与机器翻译.md) · [下一章：预训练与迁移学习](05-预训练与迁移学习.md)

> 本章目标：从软对齐进入注意力、多头机制、编码器与解码器。

## 本章目录

- [注意力机制](#注意力机制)
- [Transformer 的结构与实现](#transformer-的结构与实现)
- [Transformer 常见问答](#transformer-常见问答)

## 注意力机制

### 注意力机制介绍

Seq2Seq 的早期做法把整个源句压缩进一个固定长度向量，长句会形成信息瓶颈。注意力机制让解码器在生成每个词时，动态查看全部编码器状态。

对解码第 $`t`$ 步，计算当前解码状态 $`s_{t-1}`$ 与每个编码状态 $`h_i`$ 的匹配分数：

```math
\alpha_{t,i}=\text{softmax}(score(s_{t-1},h_i))
```

```math
c_t=\sum_i\alpha_{t,i}h_i
```

$`\alpha_{t,i}`$ 是注意力权重，$`c_t`$ 是上下文向量。它能学习软对齐关系，例如翻译某个法语词时更关注对应的英语词。

### 注意力机制扩展阅读

- **加性注意力（Bahdanau Attention）**：用小型前馈网络计算匹配分数。
- **点积注意力（Luong / Dot-product）**：用向量点积计算，速度较快。
- **自注意力（Self-Attention）**：同一序列内部的每个 token 都关注其他 token，是 Transformer 的核心。
- **交叉注意力（Cross-Attention）**：一个序列的 Query 关注另一个序列的 Key、Value，常用于编码器—解码器结构。

注意力权重有一定可解释性，但不能简单等同于因果解释或模型真实“理由”。

## Transformer 的结构与实现

### Transformer 的背景介绍

Transformer 出自 2017 年论文 *Attention Is All You Need*。它抛弃循环结构，主要依赖注意力机制建模全局关系。

相对 RNN 的优势：

- 同一层中可并行处理所有 token，训练效率高。
- 任意两个位置之间的信息交互路径更短，擅长长距离依赖。
- 易于扩展为大规模预训练模型，如 BERT、GPT、T5。

局限是标准自注意力的时间和空间复杂度随序列长度呈 $`O(n^2)`$ 增长，超长文本成本较高。

### 认识 Transformer 的架构

原始 Transformer 是 encoder-decoder 架构：

```text
输入嵌入 + 位置编码
        ↓
Encoder × N ────────────────┐
                              ↓
目标词嵌入 + 位置编码 → Decoder × N → Linear + Softmax
```

- **Encoder**：由多头自注意力、前馈网络、残差连接、层归一化组成，适合“理解”类任务。
- **Decoder**：在此基础上多了编码器—解码器注意力，并对自身未来位置使用 causal mask，适合自回归生成。
- **Encoder-only**：如 BERT，双向理解文本。
- **Decoder-only**：如 GPT，按从左到右预测下一个 token。

### 细节原理解析

#### 输入部分：Token Embedding 与位置编码

自注意力本身不包含顺序信息，因此输入表示为：

```math
X=TokenEmbedding+PositionalEncoding
```

原始论文使用正弦/余弦位置编码；现代模型也常使用可学习位置编码、RoPE（旋转位置编码）等方案。

#### 自注意力机制

输入 $`X`$ 分别线性映射得到 Query、Key、Value：

```math
Q=XW_Q,\quad K=XW_K,\quad V=XW_V
```

缩放点积注意力为：

```math
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d_k}}+M)V
```

其中 $`M`$ 是 mask：padding mask 屏蔽补齐 token；causal mask 屏蔽未来 token。除以 $`\sqrt{d_k}`$ 可防止维度较大时点积过大，导致 softmax 梯度过小。

#### 多头注意力（Multi-Head Attention）

多头注意力在多个子空间并行计算注意力，再拼接投影：

```math
MultiHead=Concat(head_1,...,head_h)W_O
```

不同的头可学习不同类型的关系，如局部搭配、指代、句法关联等。

#### 编码器层

一个 Encoder Layer：

```text
输入 → Multi-Head Self-Attention → Add & Norm → Feed Forward → Add & Norm
```

前馈网络（FFN）对每个位置独立、共享参数地进行非线性变换，通常维度先扩大再压回。残差连接帮助深层训练，LayerNorm 稳定激活分布。

#### 解码器层

Decoder Layer 包含三部分：

1. **Masked Self-Attention**：每个位置只能看见当前及之前 token。
2. **Cross-Attention**：Query 来自解码器，Key/Value 来自编码器输出。
3. **FFN**：逐位置非线性变换。

最后通过线性层映射到词表大小，再以 softmax 得到下一个 token 的概率分布。

### Transformer 的构建过程

实现时的关键检查点：

1. 定义 tokenizer、词表、`<PAD>/<BOS>/<EOS>` 与 batch mask。
2. 实现 token embedding 与位置编码，并确保维度为 `[batch, seq_len, d_model]`。
3. 实现 scaled dot-product attention，正确处理 padding 和 causal mask。
4. 叠加多头注意力、FFN、残差连接、LayerNorm，组成编码器/解码器层。
5. 使用交叉熵训练。对 `<PAD>` 位置设置 `ignore_index`，避免其影响损失。
6. 推理时从 `<BOS>` 自回归生成；可使用贪心、beam search、top-k、top-p、temperature 等策略。

常见错误：mask 方向写反、忘记在 attention score 上加 mask、将 padding 计入损失、位置编码与 embedding 维度不匹配。

## Transformer 常见问答

#### Q1：为什么 Transformer 需要位置编码？

自注意力对输入 token 的排列本身不敏感。如果没有位置编码，“我喜欢你”和“你喜欢我”会得到相同的词集合信息。位置编码将顺序注入 token 表示。

#### Q2：Self-Attention 的 Q、K、V 分别是什么？

可以把 Query 理解为“我正在寻找什么”，Key 理解为“我能提供什么线索”，Value 是“被选中后传递的内容”。Q 与 K 的相似度决定对 V 的加权方式。

#### Q3：为什么使用多头注意力？

单个注意力头只能在一个表示子空间中建立关系；多头机制让模型从多个角度同时关注序列，再融合结果，表达能力更强。

#### Q4：Transformer 和 RNN 的主要区别？

RNN 按顺序递归计算，天然有顺序信息但难并行、长依赖路径长；Transformer 用位置编码表示顺序，能并行计算且任意位置直接交互，但标准注意力对长序列开销大。

#### Q5：LayerNorm 与 BatchNorm 为什么不同？

BatchNorm 依赖 batch 维统计量，在变长序列和小 batch 中不方便；LayerNorm 对每个样本的特征维度归一化，不依赖 batch 大小，因此更适合 Transformer。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一章：序列建模与机器翻译](03-序列建模与机器翻译.md) · [下一章：预训练与迁移学习](05-预训练与迁移学习.md)
