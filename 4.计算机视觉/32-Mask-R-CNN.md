# 实例分割与 Mask R-CNN

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：U-Net](31-U-Net.md) · [下一篇：Vision Transformer](33-ViT.md)

> 深度分割 · 实例区分与掩码分支

## Instance Segmentation

Instance Segmentation：

> 不仅预测类别，还区分同类别的不同实例。

例如：

```text
两只猫

Semantic:
cat cat cat cat

Instance:
cat_1 cat_1
cat_2 cat_2
```

## Instance Segmentation

目标：

> 同时完成 Detection + Pixel-level Mask。

典型模型：

> Mask R-CNN

## Mask R-CNN

Mask R-CNN 可以理解为：

> Faster R-CNN + Mask Branch

结构：

```text
Image
 ↓
Backbone
 ↓
RPN
 ↓
RoI
 ├── Classification
 ├── Bounding Box
 └── Mask
```

因此每个目标得到：

- 类别
- Bounding Box
- Pixel Mask

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：U-Net](31-U-Net.md) · [下一篇：Vision Transformer](33-ViT.md)
