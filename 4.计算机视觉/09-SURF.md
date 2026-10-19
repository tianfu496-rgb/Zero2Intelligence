# SURF

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：SIFT](08-SIFT.md) · [下一篇：ORB](10-ORB.md)

> 局部特征 · 近似计算与加速特征提取

## SURF

SURF：

> Speeded-Up Robust Features

设计目标：

> 在保持尺度、旋转鲁棒性的同时提高速度。

核心思想包括：

- Integral Image
- Box Filter
- Hessian Matrix

SURF 与 SIFT：

|          | SIFT | SURF                 |
| -------- | ---- | -------------------- |
| 尺度不变 | ✓    | ✓                    |
| 旋转不变 | ✓    | ✓                    |
| 速度     | 较慢 | 通常更快             |
| 核心     | DoG  | Hessian + Box Filter |

> ⚠️ SURF 受专利/实现许可历史影响，实际 OpenCV 环境中不一定默认提供。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：SIFT](08-SIFT.md) · [下一篇：ORB](10-ORB.md)
