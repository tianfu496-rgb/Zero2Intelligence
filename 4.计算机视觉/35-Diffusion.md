# Diffusion 扩散模型

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：CLIP](34-CLIP.md) · [下一篇：核心知识对比](36-核心知识对比.md)

> 现代视觉 · 前向加噪与反向去噪

## Diffusion

Diffusion Model 的核心思想：

### Forward Process

逐渐向图像添加噪声：

```math
x_0\rightarrow x_1\rightarrow x_2\rightarrow\cdots\rightarrow x_T
```

最终：

```math
x_T\approx\mathcal N(0,I)
```

### Reverse Process

训练模型学习：

```math
x_T\rightarrow x_{T-1}\rightarrow\cdots\rightarrow x_0
```

即：

> **从噪声逐渐生成图像。**

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：CLIP](34-CLIP.md) · [下一篇：核心知识对比](36-核心知识对比.md)
