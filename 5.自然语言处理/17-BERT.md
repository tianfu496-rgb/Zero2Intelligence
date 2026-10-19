# BERT

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：ELMo](16-ELMo.md) · [下一篇：GPT](18-GPT.md)

> 预训练模型 · 双向 Encoder、MLM 和理解任务

## BERT 模型特点

BERT（Bidirectional Encoder Representations from Transformers）使用 Transformer Encoder，通过双向上下文生成 token 表示。

- **Masked Language Model（MLM）**：随机遮住部分 token，让模型预测它们，从左右两侧学习上下文。
- **Next Sentence Prediction（NSP）**：原始 BERT 用于学习句对关系；后续研究表明它并非总是必要。
- **特殊 token**：`[CLS]` 常作为分类汇总表示，`[SEP]` 分隔句子，`[MASK]` 用于 MLM。
- **微调方式**：在 `[CLS]` 输出上加分类层可做分类；使用每个 token 输出可做 NER、抽取式问答等。

BERT 并非天然适合从左到右自由生成：MLM 训练方式与自回归生成不完全一致，生成一般更常使用 GPT/T5/BART 类模型。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：ELMo](16-ELMo.md) · [下一篇：GPT](18-GPT.md)
