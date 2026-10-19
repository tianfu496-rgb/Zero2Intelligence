# ORB

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：SURF](09-SURF.md) · [下一篇：描述子与特征匹配](11-描述子与特征匹配.md)

> 局部特征 · FAST 角点和二进制描述子

## ORB

ORB：

> Oriented FAST and Rotated BRIEF

由：

- FAST：关键点检测
- BRIEF：特征描述

组成。

优势：

- 快
- 计算量低
- 适合实时应用
- 描述子为二进制

OpenCV：

```python
orb = cv2.ORB_create()

keypoints, descriptors = orb.detectAndCompute(
    gray,
    None
)
```

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：SURF](09-SURF.md) · [下一篇：描述子与特征匹配](11-描述子与特征匹配.md)
