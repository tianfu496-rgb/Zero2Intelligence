# CLIP

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Vision Transformer](33-ViT.md) · [下一篇：Diffusion 扩散模型](35-Diffusion.md)

> 现代视觉 · 图文对齐和跨模态表示

## CLIP

CLIP：

> Contrastive Language-Image Pre-training

核心思想：

> **同时学习图像和文本的表示，使匹配的图像-文本靠近，不匹配的远离。**

例如：

```text
Image ──→ Image Encoder ──→ Image Embedding
                                      │
                                      │ similarity
                                      ↓
Text  ──→ Text Encoder ───→ Text Embedding
```

典型应用：

- Zero-shot Classification
- Image-Text Retrieval
- 多模态理解

核心思想：

> 图像和文本进入共同的 embedding space。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Vision Transformer](33-ViT.md) · [下一篇：Diffusion 扩散模型](35-Diffusion.md)
