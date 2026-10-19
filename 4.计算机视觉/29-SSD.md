# SSD

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：YOLO](28-YOLO.md) · [下一篇：语义分割与 FCN](30-语义分割与FCN.md)

> 目标检测 · 多尺度特征图上的检测

## SSD

SSD：

> Single Shot MultiBox Detector

特点：

> 在多个尺度的 Feature Maps 上进行检测。

```text
Backbone
 ├── Feature Map 1 → Detection
 ├── Feature Map 2 → Detection
 ├── Feature Map 3 → Detection
 └── ...
```

因此可以处理不同大小的目标。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：YOLO](28-YOLO.md) · [下一篇：语义分割与 FCN](30-语义分割与FCN.md)
