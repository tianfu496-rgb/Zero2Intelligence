# DenseNet

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：ResNet](21-ResNet.md) · [下一篇：图像分类与迁移学习](23-图像分类与迁移.md)

> 分类网络 · 密集连接与特征复用

## DenseNet

DenseNet：

> **每一层都与后续层连接。**

$$
x_l=H_l([x_0,x_1,\dots,x_{l-1}])
$$

其中 $`[\cdot]`$ 表示 Concatenation。

特点：

- 特征复用
- 梯度传播好
- 参数利用率高

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：ResNet](21-ResNet.md) · [下一篇：图像分类与迁移学习](23-图像分类与迁移.md)
