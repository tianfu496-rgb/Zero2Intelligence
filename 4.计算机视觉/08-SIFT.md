# SIFT

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Harris 角点检测](07-Harris.md) · [下一篇：SURF](09-SURF.md)

> 局部特征 · 尺度空间、关键点与描述子

## SIFT

SIFT：

> Scale-Invariant Feature Transform

主要特点：

- 尺度不变
- 旋转不变
- 对一定程度的光照变化具有鲁棒性

---

### SIFT 流程

```text
Gaussian Scale Space
       ↓
Difference of Gaussian
       ↓
Keypoint Localization
       ↓
Orientation Assignment
       ↓
Descriptor
```

尺度空间：

$$
L(x,y,\sigma)=G(x,y,\sigma)*I(x,y)
$$

DoG：

$$
D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma)
$$

经典 SIFT Descriptor：

$$
4\times4\times8=128
$$

即：

> **128 维描述子。**

OpenCV：

```python
sift = cv2.SIFT_create()

keypoints, descriptors = sift.detectAndCompute(
    gray,
    None
)
```

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Harris 角点检测](07-Harris.md) · [下一篇：SURF](09-SURF.md)
