# Fast R-CNN

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：R-CNN](25-R-CNN.md) · [下一篇：Faster R-CNN](27-Faster-R-CNN.md)

> 目标检测 · 共享特征图与 RoI Pooling

## Fast R-CNN

改进：

> **整张图只进行一次 CNN。**

流程：

```text
Image
 ↓
CNN
 ↓
Feature Map
 ↓
RoI Pooling
 ↓
Classification + BBox Regression
```

优点：

> 比 R-CNN 快很多。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：R-CNN](25-R-CNN.md) · [下一篇：Faster R-CNN](27-Faster-R-CNN.md)
