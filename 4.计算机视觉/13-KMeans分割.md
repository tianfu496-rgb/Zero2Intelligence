# K-Means 图像分割

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：阈值分割与 Otsu](12-阈值与Otsu.md) · [下一篇：区域生长与分水岭](14-区域生长与分水岭.md)

> 传统分割 · 像素聚类与目标函数

## K-means

把像素看成数据点：

$$
x_i=[R_i,G_i,B_i]
$$

目标：

$$
J=\sum_{i=1}^{N}\lVert x_i-\mu_{c_i}\rVert^2
$$

流程：

```text
初始化 K 个中心
      ↓
分配样本
      ↓
重新计算中心
      ↓
重复直到收敛
```

OpenCV：

```python
data = img.reshape((-1, 3))
data = np.float32(data)

criteria = (
    cv2.TERM_CRITERIA_EPS +
    cv2.TERM_CRITERIA_MAX_ITER,
    100,
    0.2
)

K = 3

_, labels, centers = cv2.kmeans(
    data,
    K,
    None,
    criteria,
    10,
    cv2.KMEANS_RANDOM_CENTERS
)

result = centers[
    labels.flatten()
].reshape(img.shape)

result = np.uint8(result)
```

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：阈值分割与 Otsu](12-阈值与Otsu.md) · [下一篇：区域生长与分水岭](14-区域生长与分水岭.md)
