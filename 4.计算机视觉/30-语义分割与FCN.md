# 语义分割与 FCN

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：SSD](29-SSD.md) · [下一篇：U-Net](31-U-Net.md)

> 深度分割 · 逐像素分类和全卷积网络

## Semantic Segmentation

目标：

> **给每个像素分配一个类别。**

例如：

```text
Pixel → road
Pixel → car
Pixel → person
Pixel → sky
```

注意：

同类别不同实例通常不区分。

## Semantic Segmentation

目标：

> 每一个像素预测一个类别。

典型模型：

- FCN
- U-Net
- DeepLab

输出：

$$
H\times W\times C
$$

每个像素都有 $`C`$ 个类别的预测。

## FCN

FCN：

> Fully Convolutional Network

核心思想：

> **将传统 CNN 中的全连接层替换为卷积结构，使网络能够输出空间特征图。**

流程：

```text
Image
 ↓
CNN
 ↓
Feature Map
 ↓
Upsampling
 ↓
Pixel-wise Prediction
```

核心贡献：

> 将 CNN 从图像级分类扩展到像素级预测。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：SSD](29-SSD.md) · [下一篇：U-Net](31-U-Net.md)
