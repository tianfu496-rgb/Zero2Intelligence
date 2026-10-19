# 学习笔记

从 Python 出发，逐步学习机器学习、深度学习、视觉与语言模型。四个核心主题已按知识依赖拆成 **81 篇独立章节**；每个主题都有目录，每篇章节都有前后翻页导航。

## 从哪里开始

| 顺序 | 主题目录 | 内容与阅读顺序 |
| --- | --- | --- |
| 1 | [Python 基础](1.PYTHON基础/Python%20笔记.md) | 语法 → 数据结构 → 函数与对象 → 并发与工程化 |
| 2 | [机器学习 · 13 章](2.机器学习/README.md) | 数据与评估 → KNN → 线性回归 → Logistic 回归 → 决策树 → 集成方法 |
| 3 | [深度学习 · 9 章](3.深度学习/README.md) | 神经网络 → 激活函数 → 反向传播与损失 → 优化器 → 训练稳定性 → 架构 |
| 4A | [计算机视觉 · 40 章](4.计算机视觉/README.md) | 图像处理 → 特征与几何 → CNN → 检测与分割 → ViT、CLIP、Diffusion |
| 4B | [自然语言处理 · 19 章](5.自然语言处理/README.md) | 文本表示 → FastText → RNN/LSTM/GRU → 注意力与 Transformer → 预训练模型 |
| 5 | [Transformer 与注意力工程专题](6.Transformer与注意力/Transformer与注意力学习笔记.md) | 张量与 Mask → 训练与标签移动 → 自回归推理 → KV Cache 与性能 |
| 6 | [RAG：检索增强生成](AI_Agent/RAG%28Retrieval%20Augmented%20Generation%29检索增强生成.md) | 资料分片 → 召回 → 重排 → 基于资料生成回答 |
| 协作工具 | [Git 学习笔记](Git/Git学习笔记.md) | 提交、分支、冲突处理与 GitHub 协作 |

视觉与语言是两条可并行选择的方向。初学者先完成机器学习和深度学习；已有基础时可直接从下面的算法入口进入。

## 算法直达

### 机器学习

| 基础模型 | 集成方法 |
| --- | --- |
| [KNN](2.机器学习/04-KNN.md) | [集成学习概览](2.机器学习/08-集成学习概览.md) |
| [线性回归](2.机器学习/05-线性回归.md) | [随机森林 Random Forest](2.机器学习/09-随机森林.md) |
| [Logistic 回归](2.机器学习/06-Logistic回归.md) | [AdaBoost](2.机器学习/10-AdaBoost.md) |
| [决策树](2.机器学习/07-决策树.md) | [GBDT](2.机器学习/11-GBDT.md) |
| [模型评估与拟合](2.机器学习/03-模型评估与拟合.md) | [XGBoost](2.机器学习/12-XGBoost.md)、[Voting 与 Stacking](2.机器学习/13-Voting与Stacking.md) |

### 视觉与语言

| 方向 | 常用入口 |
| --- | --- |
| 图像处理 | [卷积](4.计算机视觉/03-卷积与相关.md)、[Canny](4.计算机视觉/06-Canny.md)、[Harris](4.计算机视觉/07-Harris.md)、[SIFT](4.计算机视觉/08-SIFT.md)、[ORB](4.计算机视觉/10-ORB.md) |
| 视觉网络 | [CNN](4.计算机视觉/18-CNN基础与训练.md)、[ResNet](4.计算机视觉/21-ResNet.md)、[Faster R-CNN](4.计算机视觉/27-Faster-R-CNN.md)、[YOLO](4.计算机视觉/28-YOLO.md)、[U-Net](4.计算机视觉/31-U-Net.md)、[ViT](4.计算机视觉/33-ViT.md) |
| 文本表示 | [TF-IDF](5.自然语言处理/03-OneHot-BoW-TFIDF.md)、[Word2Vec](5.自然语言处理/04-Word2Vec-Embedding.md)、[FastText](5.自然语言处理/05-FastText.md) |
| 序列与语言模型 | [RNN](5.自然语言处理/07-RNN.md)、[LSTM](5.自然语言处理/08-LSTM.md)、[GRU](5.自然语言处理/09-GRU.md)、[Transformer](5.自然语言处理/13-Transformer.md)、[BERT](5.自然语言处理/17-BERT.md)、[GPT](5.自然语言处理/18-GPT.md) |

## 阅读与维护

- 初次学习按主题目录编号阅读；复习时从算法名进入。各篇的顶部、底部均有目录和前后篇链接。
- 原来的四个总笔记文件已改为章节入口，旧文件链接仍可进入新目录。
- 每篇只有一个一级标题；正文使用二级、三级标题组织概念、公式和示例。
- 行内公式使用 GitHub 支持的带反引号定界形式，避免下划线等字符与 Markdown 冲突：

````markdown
行内公式：$`\hat y=w^Tx+b`$

独立公式：

```math
\sigma(z)=\frac{1}{1+e^{-z}}
```
````

- 独立公式使用 `math` 围栏块，保留矩阵中的 `\\` 换行；函数名可使用 `\mathrm{softmax}` 等写法。
- 表格中的绝对值使用 `\lvert x\rvert`，范数使用 `\lVert x\rVert`，条件概率竖线使用 `\mid`，避免用裸 `|` 打断表格。命令与紧随的字母之间需有空格或花括号。
- 代码示例使用标明语言的围栏代码块。片段需要的输入数据、库和前置步骤应在正文中说明。

公式写法参考：[GitHub 数学表达式文档](https://docs.github.com/zh/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)。
