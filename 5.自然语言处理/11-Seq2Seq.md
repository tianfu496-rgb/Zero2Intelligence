# Seq2Seq 与机器翻译

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：RNN 人名分类案例](10-人名分类.md) · [下一篇：注意力机制](12-Attention.md)

> 序列模型 · 编码器、解码器和 Teacher Forcing

## RNN 案例：Seq2Seq 英译法

Seq2Seq 通常由编码器和解码器组成：

```text
English tokens → Encoder RNN → encoder states
                                  ↓
<BOS> → Decoder RNN → French tokens → <EOS>
```

- **编码器**：读取源语言序列，产生隐藏状态。
- **解码器**：从 `<BOS>` 开始，逐词预测目标语言 token。
- **训练阶段**：常用 Teacher Forcing，即输入真实的上一个目标词。
- **推理阶段**：输入模型上一步自己预测的词，直到生成 `<EOS>` 或到达长度上限。
- **解码策略**：贪心搜索简单但容易局部最优；Beam Search 保留多个候选，通常能改善翻译质量。

训练与推理的不一致会导致 exposure bias：训练时模型总见到真实历史，推理时却要面对自己的错误历史。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：RNN 人名分类案例](10-人名分类.md) · [下一篇：注意力机制](12-Attention.md)
