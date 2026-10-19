# 注意力机制

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Seq2Seq 与机器翻译](11-Seq2Seq.md) · [下一篇：Transformer](13-Transformer.md)

> 注意力与 Transformer · 软对齐、匹配分数与上下文加权

## 注意力机制介绍

Seq2Seq 的早期做法把整个源句压缩进一个固定长度向量，长句会形成信息瓶颈。注意力机制让解码器在生成每个词时，动态查看全部编码器状态。

对解码第 $`t`$ 步，计算当前解码状态 $`s_{t-1}`$ 与每个编码状态 $`h_i`$ 的匹配分数：

```math
\alpha_{t,i}=\text{softmax}(score(s_{t-1},h_i))
```

```math
c_t=\sum_i\alpha_{t,i}h_i
```

$`\alpha_{t,i}`$ 是注意力权重，$`c_t`$ 是上下文向量。它能学习软对齐关系，例如翻译某个法语词时更关注对应的英语词。

## 注意力机制扩展阅读

- **加性注意力（Bahdanau Attention）**：用小型前馈网络计算匹配分数。
- **点积注意力（Luong / Dot-product）**：用向量点积计算，速度较快。
- **自注意力（Self-Attention）**：同一序列内部的每个 token 都关注其他 token，是 Transformer 的核心。
- **交叉注意力（Cross-Attention）**：一个序列的 Query 关注另一个序列的 Key、Value，常用于编码器—解码器结构。

注意力权重有一定可解释性，但不能简单等同于因果解释或模型真实“理由”。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Seq2Seq 与机器翻译](11-Seq2Seq.md) · [下一篇：Transformer](13-Transformer.md)
