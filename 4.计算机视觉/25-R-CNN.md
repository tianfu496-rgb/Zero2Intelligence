# R-CNN

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：目标检测基础与指标](24-检测基础与指标.md) · [下一篇：Fast R-CNN](26-Fast-R-CNN.md)

> 目标检测 · 候选区域与逐区域特征提取

## R-CNN

R-CNN：

> Regions with CNN features

流程：

```text
Image
 ↓
Selective Search
 ↓
Region Proposals
 ↓
CNN
 ↓
Feature
 ↓
SVM Classification
 ↓
Bounding Box Regression
```

问题：

> 每个 Region 都单独进行 CNN，计算重复严重。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：目标检测基础与指标](24-检测基础与指标.md) · [下一篇：Fast R-CNN](26-Fast-R-CNN.md)
