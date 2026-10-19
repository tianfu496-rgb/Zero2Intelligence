# One-hot、BoW 与 TF-IDF

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：文本预处理](02-文本预处理.md) · [下一篇：Word2Vec 与 Embedding](04-Word2Vec-Embedding.md)

> 输入与基线 · 从离散编码到统计文本表示

## One-hot 编码

若词表大小为 $`V`$，每个词用一个长度为 $`V`$ 的向量表示，所在词表位置为 1，其余为 0。

- 优点：直观、无需训练。
- 缺点：维度高、极度稀疏；任意两个不同词的向量距离相同，无法表达语义相似性。

## Bag of Words 与 TF-IDF

**词袋模型（BoW）**只统计词是否出现或出现次数，不保留顺序。

TF-IDF 用词频与逆文档频率衡量词的重要性：

$$
TF\text{-}IDF(w,d)=TF(w,d)\times \log\frac{N}{DF(w)+1}
$$

它适合传统文本分类和检索，但仍忽略词序与上下文。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：文本预处理](02-文本预处理.md) · [下一篇：Word2Vec 与 Embedding](04-Word2Vec-Embedding.md)
