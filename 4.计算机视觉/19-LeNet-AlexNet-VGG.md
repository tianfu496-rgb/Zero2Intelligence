# LeNet、AlexNet 与 VGG

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：CNN 基础与训练](18-CNN基础与训练.md) · [下一篇：GoogLeNet 与 Inception](20-Inception.md)

> 分类网络 · 从早期 CNN 到深层小卷积核

## LeNet

LeNet 是早期经典 CNN。

基本结构：

```text
Input
 ↓
Conv
 ↓
Pooling
 ↓
Conv
 ↓
Pooling
 ↓
FC
 ↓
Output
```

主要用于：

> 手写数字识别。

意义：

> 证明 CNN 对图像识别非常有效。

## AlexNet

AlexNet 在 ImageNet 竞赛中取得重要突破。

特点：

- 更深的 CNN
- ReLU
- Dropout
- GPU 训练
- Data Augmentation

核心贡献：

> 推动深度 CNN 在大规模图像分类中的应用。

## VGG

VGG 的核心思想：

> **使用大量 $`3\times3`$ 小卷积核构建深层网络。**

典型：

- VGG-16
- VGG-19

特点：

- 结构简单
- 网络较深
- 参数量较大

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：CNN 基础与训练](18-CNN基础与训练.md) · [下一篇：GoogLeNet 与 Inception](20-Inception.md)
