# FastText

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Word2Vec 与 Embedding](04-Word2Vec-Embedding.md) · [下一篇：文本数据分析与增强](06-数据分析与增强.md)

> 输入与基线 · 子词表示与轻量文本分类

## FastText 工具介绍

FastText 是 Meta 开源的高效文本表示与分类工具。它的特点是将词表示为字符 n-gram 的组合，因此对未登录词、拼写变化和形态丰富语言更友好。

与 Word2Vec 相比，FastText 不只学习整词向量，也学习子词向量。例如 `where` 可由 `<wh`、`whe`、`her`、`ere`、`re>` 等 n-gram 共同表示。

## FastText 文本分类

FastText 分类通常采用“词向量平均 + 线性分类器”的轻量结构，并使用层次 softmax 或负采样提升大类别场景的效率。

训练数据常用一行一个样本的格式：

```text
__label__positive 这个产品很好用
__label__negative 物流太慢了
```

优点是训练快、部署轻量，适合基线模型和资源受限场景；缺点是对复杂语序和深层语义的表达弱于 Transformer。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Word2Vec 与 Embedding](04-Word2Vec-Embedding.md) · [下一篇：文本数据分析与增强](06-数据分析与增强.md)
