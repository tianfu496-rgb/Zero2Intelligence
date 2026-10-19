# GoogLeNet 与 Inception

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：LeNet、AlexNet 与 VGG](19-LeNet-AlexNet-VGG.md) · [下一篇：ResNet](21-ResNet.md)

> 分类网络 · 多尺度分支与通道压缩

## GoogLeNet / Inception

核心：

> **Inception Module**

同时使用不同大小卷积：

```text
        Input
       /  |  \
     1x1 3x3 5x5
       \  |  /
        Concat
```

优点：

> 同时捕获不同尺度的信息。

另外使用 $`1\times1`$ Conv：

> **降低通道数、减少计算量。**

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：LeNet、AlexNet 与 VGG](19-LeNet-AlexNet-VGG.md) · [下一篇：ResNet](21-ResNet.md)
