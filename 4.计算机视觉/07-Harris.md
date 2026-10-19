# Harris 角点检测

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Canny 边缘检测](06-Canny.md) · [下一篇：SIFT](08-SIFT.md)

> 局部特征 · 角点、结构矩阵与响应函数

## Corner Detection

Corner 的基本特征：

> 在两个方向上都有明显的灰度变化。

三种典型区域：

| 区域     | x 方向变化 | y 方向变化 |
| -------- | ---------- | ---------- |
| 平坦区域 | 小         | 小         |
| 边缘     | 大         | 小         |
| 角点     | 大         | 大         |

## Harris Corner

核心思想：

考虑窗口发生小位移后的变化：

```math
E(u,v)=\sum_{x,y}w(x,y)[I(x+u,y+v)-I(x,y)]^2
```

近似：

```math
E(u,v)\approx\begin{bmatrix}u&v\end{bmatrix}M\begin{bmatrix}u\\v\end{bmatrix}
```

其中：

```math
M=\begin{bmatrix}\sum I_x^2&\sum I_xI_y\\\sum I_xI_y&\sum I_y^2\end{bmatrix}
```

Harris response：

```math
R=\det(M)-k\bigl(\mathrm{trace}(M)\bigr)^2
```

### 判断

- $`R`$ 大：Corner
- $`R`$ 小：Flat
- $`R`$ 为较大的负值：Edge

OpenCV：

```python
gray = np.float32(gray)

dst = cv2.cornerHarris(
    gray,
    blockSize=2,
    ksize=3,
    k=0.04
)
```

### 缺点

Harris：

> **对尺度变化不具有天然不变性。**

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Canny 边缘检测](06-Canny.md) · [下一篇：SIFT](08-SIFT.md)
