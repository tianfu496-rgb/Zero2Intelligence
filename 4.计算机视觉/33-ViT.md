# Vision Transformer

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：实例分割与 Mask R-CNN](32-Mask-R-CNN.md) · [下一篇：CLIP](34-CLIP.md)

> 现代视觉 · Patch、Token 与自注意力

## Vision Transformer

如果课程涉及：

ViT：

> 将图像划分为 Patch，把 Patch 当作 Token 输入 Transformer。

流程：

```text
Image
 ↓
Patch
 ↓
Patch Embedding
 ↓
Position Embedding
 ↓
Transformer Encoder
 ↓
Classification Head
```

Self-Attention：

```math
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
```

## Vision Transformer

ViT 核心：

> 用 Transformer 处理图像 Patch 序列。

假设图像大小：

```math
H\times W
```

Patch 大小：

```math
P\times P
```

Patch 数量：

```math
N=\frac{HW}{P^2}
```

然后：

```math
\text{Image}\rightarrow N\text{ Patches}\rightarrow N\text{ Tokens}\rightarrow\text{Transformer}
```

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：实例分割与 Mask R-CNN](32-Mask-R-CNN.md) · [下一篇：CLIP](34-CLIP.md)
