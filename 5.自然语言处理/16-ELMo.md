# ELMo

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：迁移学习与微调](15-迁移学习与微调.md) · [下一篇：BERT](17-BERT.md)

> 预训练模型 · 双向 LSTM 与上下文词向量

## ELMo 模型的介绍

ELMo（Embeddings from Language Models）基于双向 LSTM 语言模型，将不同层的隐藏状态加权组合，得到随上下文变化的词向量。

它的重要贡献是证明了**上下文相关表示**的价值：同一个词在不同句子中的向量可以不同。与 BERT 相比，ELMo 使用 LSTM，双向信息通常由两个单向语言模型分别得到；BERT 则通过 Transformer 的 MLM 更深度地融合双向上下文。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：迁移学习与微调](15-迁移学习与微调.md) · [下一篇：BERT](17-BERT.md)
