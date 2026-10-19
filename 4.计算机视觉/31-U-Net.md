# U-Net

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：语义分割与 FCN](30-语义分割与FCN.md) · [下一篇：实例分割与 Mask R-CNN](32-Mask-R-CNN.md)

> 深度分割 · 编码器、解码器和跳跃连接

## U-Net

U-Net 采用：

> **Encoder-Decoder + Skip Connection**

结构：

```text
Encoder                  Decoder

Image
 ↓                         ↑
Conv                      Conv
 ↓                         ↑
Conv                      Conv
 ↓                         ↑
Bottleneck ─────────────→
```

Skip Connection 将 Encoder 的高分辨率特征传给 Decoder。

优势：

> 保留细节信息，适合医学图像分割等像素级任务。

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：语义分割与 FCN](30-语义分割与FCN.md) · [下一篇：实例分割与 Mask R-CNN](32-Mask-R-CNN.md)
