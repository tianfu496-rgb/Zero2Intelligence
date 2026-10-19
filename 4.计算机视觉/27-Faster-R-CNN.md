# Faster R-CNN

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Fast R-CNN](26-Fast-R-CNN.md) · [下一篇：YOLO](28-YOLO.md)

> 目标检测 · RPN 与两阶段检测

## Faster R-CNN

进一步加入：

> **RPN（Region Proposal Network）**

流程：

```text
Image
 ↓
Backbone CNN
 ↓
Feature Map
 ↓
RPN
 ↓
Region Proposals
 ↓
RoI Pooling / RoI Align
 ↓
Classification + BBox Regression
```

核心：

> **让候选区域生成也由神经网络完成。**

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：Fast R-CNN](26-Fast-R-CNN.md) · [下一篇：YOLO](28-YOLO.md)
