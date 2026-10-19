# ResNet

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：GoogLeNet 与 Inception](20-Inception.md) · [下一篇：DenseNet](22-DenseNet.md)

> 分类网络 · 残差连接与深层网络训练

## ResNet

ResNet 核心：

> Residual Connection

$$
y=F(x)+x
$$

即：

```text
       ┌──────────────┐
       │              ↓
x → Conv → Conv → Add → y
```

解决深层网络中的：

- 梯度传播困难
- 网络退化

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：GoogLeNet 与 Inception](20-Inception.md) · [下一篇：DenseNet](22-DenseNet.md)
