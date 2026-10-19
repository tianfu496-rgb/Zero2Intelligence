# CNN 基础与训练

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：双目与对极几何](17-双目与对极几何.md) · [下一篇：LeNet、AlexNet 与 VGG](19-LeNet-AlexNet-VGG.md)

> 分类网络 · 卷积层、池化、归一化与损失

## CNN

CNN：

> Convolutional Neural Network

核心结构：

```text
Input
 ↓
Convolution
 ↓
Activation
 ↓
Pooling
 ↓
Convolution
 ↓
...
 ↓
Fully Connected / Classification Head
```

CNN 擅长处理：

> **具有空间结构的数据。**

## 卷积层

卷积核：

```math
K\in\mathbb{R}^{H\times W\times C}
```

卷积的核心：

> **局部连接 + 权重共享。**

优点：

- 参数量减少
- 可以提取局部特征
- 保留空间结构

---

### 参数量

Kernel：

```math
K\times K
```

输入通道：

CinC_{in}

输出通道：

CoutC_{out}

参数量：

K2CinCoutK^2C_{in}C_{out}

如果有 Bias：

K2CinCout+CoutK^2C_{in}C_{out}+C_{out}

## Padding / Stride

输出尺寸：

```math
O=\left\lfloor\frac{N+2P-K}{S}\right\rfloor+1
```

其中：

- $`N`$：输入尺寸
- $`P`$：Padding
- $`K`$：Kernel
- $`S`$：Stride

## Pooling

### Max Pooling

取窗口最大值。

```text
1  3
2  4

→ 4
```

### Average Pooling

取平均值。

作用：

- 降低空间尺寸
- 减少计算
- 提高一定程度的平移鲁棒性
- 扩大感受野

PyTorch：

```python
import torch.nn as nn

pool = nn.MaxPool2d(
    kernel_size=2,
    stride=2
)
```

## ReLU

```math
\mathrm{ReLU}(x)=\max(0,x)
```

```python
relu = nn.ReLU()
```

优点：

- 简单
- 计算快
- 缓解部分梯度消失问题

缺点：

> 负数区域梯度为 0，可能出现 Dead ReLU。

## Fully Connected Layer

全连接层：

```math
y=Wx+b
```

每个输出神经元连接所有输入。

通常 CNN 最后可以：

```text
Feature Map
 ↓
Flatten / Global Pooling
 ↓
Fully Connected
 ↓
Class Scores
```

## Batch Normalization

对于一个 Batch：

```math
\hat{x}=\frac{x-\mu_B}{\sqrt{\sigma_B^2+\epsilon}}
```

然后：

```math
y=\gamma\hat{x}+\beta
```

其中：

- $`\gamma`$：可学习缩放
- $`\beta`$：可学习偏移

作用：

- 稳定训练
- 加快收敛
- 一定程度上减少过拟合

PyTorch：

```python
bn = nn.BatchNorm2d(64)
```

## Dropout

训练时随机将部分神经元置零。

```python
dropout = nn.Dropout(p=0.5)
```

作用：

> **减少过拟合。**

注意：

> Dropout 通常只在训练阶段启用。

## Backpropagation

神经网络训练：

```text
Input
 ↓
Forward
 ↓
Prediction
 ↓
Loss
 ↓
Backward
 ↓
Gradient
 ↓
Optimizer
 ↓
Parameter Update
```

梯度下降：

```math
\theta_{t+1}=\theta_t-\eta\nabla_\theta L
```

其中：

- $`\theta`$：参数
- $`\eta`$：Learning Rate
- $`L`$：Loss

---

### PyTorch 示例

```python
optimizer.zero_grad()

output = model(x)

loss = criterion(output, y)

loss.backward()

optimizer.step()
```

## Loss Function

### MSE

常用于回归：

```math
L=\frac1N\sum_i(y_i-\hat y_i)^2
```

---

### Cross Entropy

分类任务常用：

```math
L=-\sum_i y_i\log p_i
```

如果真实类别是 $`k`$：

```math
L=-\log p_k
```

因此：

> 真实类别预测概率越高 → Loss 越小。

PyTorch：

```python
criterion = nn.CrossEntropyLoss()

loss = criterion(
    prediction,
    label
)
```

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：双目与对极几何](17-双目与对极几何.md) · [下一篇：LeNet、AlexNet 与 VGG](19-LeNet-AlexNet-VGG.md)
