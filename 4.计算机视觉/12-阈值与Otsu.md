# 阈值分割与 Otsu

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：描述子与特征匹配](11-描述子与特征匹配.md) · [下一篇：K-Means 图像分割](13-KMeans分割.md)

> 传统分割 · 固定阈值和最大类间方差

目标：

> **将图像划分成具有相似性质的区域。**

## Thresholding

最简单的分割方法：

$$
g(x,y)=\begin{cases}1,&I(x,y)>T\\0,&I(x,y)\le T\end{cases}
$$

```python
_, binary = cv2.threshold(
    gray,
    127,
    255,
    cv2.THRESH_BINARY
)
```

## Otsu

Otsu 自动寻找最佳阈值。

核心：

> **最大化类间方差。**

设前景和背景分为两类：

$$
\sigma_B^2=\omega_0\omega_1(\mu_0-\mu_1)^2
$$

选择使 $`\sigma_B^2`$ 最大的阈值。

OpenCV：

```python
threshold, binary = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
```

优点：

> 不需要人工指定阈值。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：描述子与特征匹配](11-描述子与特征匹配.md) · [下一篇：K-Means 图像分割](13-KMeans分割.md)
