# Canny 边缘检测

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Sobel、Prewitt 与 Laplacian](05-梯度边缘算子.md) · [下一篇：Harris 角点检测](07-Harris.md)

> 局部运算 · 平滑、非极大值抑制和双阈值

## Canny

Canny 是经典边缘检测算法。

流程：

```text
Gaussian Blur
      ↓
Gradient
      ↓
Non-Maximum Suppression
      ↓
Double Threshold
      ↓
Edge Tracking by Hysteresis
      ↓
Final Edge
```

OpenCV：

```python
edges = cv2.Canny(
    gray,
    threshold1=50,
    threshold2=150
)
```

### Canny 两个阈值

- 高阈值：强边缘
- 低阈值：弱边缘

弱边缘如果与强边缘连接，则保留。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Sobel、Prewitt 与 Laplacian](05-梯度边缘算子.md) · [下一篇：Harris 角点检测](07-Harris.md)
