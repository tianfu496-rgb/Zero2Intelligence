# Logistic 回归

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：线性回归](05-线性回归.md) · [下一篇：决策树](07-决策树.md)

> 单模型 · Sigmoid、交叉熵与分类边界

逻辑回归虽名带"回归"，实为**二分类算法**，核心是在线性回归输出 $`z = w^Tx + b`$ 上套一层 **Sigmoid 函数**压缩成概率，用**交叉熵损失**（等价于最大似然估计）训练。

## 定义与本质

| 维度                  | 说明                                                         |
| :-------------------- | :----------------------------------------------------------- |
| **任务**              | 分类（主要二分类，可扩展多分类）                             |
| **本质**              | 线性回归 + Sigmoid 激活 = 概率输出                           |
| **模型** | $`P(y=1\mid x)=\sigma(w^Tx+b)=\dfrac{1}{1+e^{-z}}`$ |
| **决策边界**          | 线性超平面 $`\{x: w^Tx + b = 0\}`$，概率≥0.5 判正类            |
| **对数几率（Logit）** | $`\log\dfrac{P(y=1\mid x)}{P(y=0\mid x)}=w^Tx+b`$，即对数几率是特征的线性组合 |

> **线性回归 → 逻辑回归**：线性回归输出 $`(-\infty, +\infty)`$，不能解释为概率；Sigmoid 压缩到 $`(0,1)`$ 才可解释为"属于正类的概率"。

## Sigmoid 函数

$$
\sigma(z) = \frac{1}{1 + e^{-z}}, \quad z = w^Tx + b
$$

- **性质**：S 形曲线，将任意实数映射到 $`(0,1)`$；单调递增、平滑可微
- **导数简洁**：$`\sigma'(z) = \sigma(z)(1 - \sigma(z))`$
- **局限**：输入趋于 ±∞ 时梯度趋零（深层网络中易梯度消失）；含指数运算

## 损失函数：交叉熵（对数损失）

$$
L = -\frac{1}{m}\sum_{i=1}^{m}[y_i\log\hat{y}_i + (1-y_i)\log(1-\hat{y}_i)]
$$

| 真实值 y | 预测 ŷ | 损失                 |
| :------- | :----- | :------------------- |
| 1        | 接近 1 | 小（预测对且自信）   |
| 1        | 接近 0 | 极大（预测错且自信） |
| 0        | 接近 0 | 小                   |
| 0        | 接近 1 | 极大                 |

**关键性质**：
- 损失是**凸函数**，梯度下降必收敛到全局最优
- **MLE 等价性**：假设 y 服从伯努利分布，最大化似然 ↔ 最小化交叉熵
- 预测错误且自信时损失指数级增长，给模型强"纠错信号"

<details>
<summary>📖 为什么不用 MSE？</summary>

1. **MSE + Sigmoid 会导致损失函数非凸**，存在多个局部极小值，梯度下降难找全局最优
2. **梯度形式复杂**：MSE 对参数的偏导含 $`\sigma'(z)`$ 项，当预测接近 0 或 1 时梯度趋零，学习停滞
3. **概率依据缺失**：MSE 对应高斯假设，而分类标签服从伯努利分布，交叉熵才是 MLE 的自然产物

</details>

## 梯度下降求解

**梯度公式极其简洁**：

$$
\frac{\partial L}{\partial w_j} = \frac{1}{m}\sum_{i=1}^{m}(\hat{y}_i - y_i)x_{ij}, \quad w_j := w_j - \alpha \cdot (\hat{y} - y)x_j
$$

> **形式与线性回归梯度完全相同**，区别在于 $`\hat{y}`$ 经过了 Sigmoid 压缩。这个"预测值−真实值"的形式是**神经网络反向传播的基石**。

## 多分类扩展

| 策略        | OvR（One-vs-Rest）                        | Softmax（多项逻辑回归）     |
| :---------- | :---------------------------------------- | :-------------------------- |
| **原理**    | N 类训练 N 个二分类器，每类 vs 其他所有类 | 直接输出各类概率，和为 1    |
| **模型数**  | N 个                                      | 1 个                        |
| **优点**    | 实现简单、计算高效、适合类别多            | 保留类别间相关性，精度更高  |
| **缺点**    | 忽略类别间关系，类别不均衡时退化          | 类别极多时计算开销大        |
| **sklearn** | `multi_class='ovr'`（liblinear 默认）     | `multi_class='multinomial'` |
| **适用**    | 类别多、效率优先                          | 类别少、精度优先            |

> **Softmax 函数**：$`\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_k e^{z_k}}`$，是 Sigmoid 在多分类下的自然推广，所有类别概率归一化为 1。

## 正则化

逻辑回归默认带正则化，sklearn 用 **C** 控制强度（C 是 λ 的倒数）：

| 参数      | 选项               | 效果                                                   |
| :-------- | :----------------- | :----------------------------------------------------- |
| `penalty` | `'l2'`（默认）     | 权重整体缩小，不归零，稳定                             |
|           | `'l1'`             | 权重归零，**特征选择**，稀疏解                         |
|           | `'elasticnet'`     | L1+L2 结合，兼顾稀疏与稳定                             |
|           | `None`             | 无正则化                                               |
| `C`       | 正浮点（默认 1.0） | **C 越小→正则越强→易欠拟合；C 越大→正则越弱→易过拟合** |

> `solver` 与正则化的匹配：liblinear 支持 L1/L2；lbfgs/newton-cg/sag 仅 L2；saga 支持 L1/L2/ElasticNet。

## 优缺点与适用场景

| 优点                                      | 缺点                               |
| :---------------------------------------- | :--------------------------------- |
| 简单高效、训练快、可并行                  | 假设线性决策边界，非线性需特征工程 |
| 输出概率，可解释性强（系数=对数几率变化） | 对异常值和多重共线性敏感           |
| 损失凸，全局最优解                        | 类别严重不平衡时表现差             |
| 是神经网络 Softmax 层的雏形               | 高维特征需正则化防止过拟合         |

**适用场景**：二分类基线模型、需概率输出和强可解释性的场景（金融风控、医疗诊断、点击率预估、垃圾邮件检测、疾病预测）。

## 评估指标

分类任务常用：
- **Accuracy**：整体正确率（类别平衡时）
- **Precision / Recall / F1**：不平衡数据必备
- **ROC-AUC**：衡量正负样本区分能力，对阈值不敏感
- **混淆矩阵**：可视化各类别对错情况

## 代码实现要点

```python
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV

# 1. 划分 + 标准化（迭代优化必需，否则收敛慢或不稳）
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y)
scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_te_s = scaler.transform(X_te)

# 2. 建模
model = LogisticRegression(
    penalty='l2',            # l1/l2/elasticnet/None
    C=1.0,                   # 正则强度倒数，越小越强
    solver='lbfgs',          # lbfgs/liblinear/saga/newton-cg/sag
    max_iter=100,
    class_weight='balanced', # 类别不平衡时自动加权
    multi_class='auto'       # auto/ovr/multinomial
).fit(X_tr_s, y_tr)

# 3. 调 C（交叉验证）
grid = GridSearchCV(LogisticRegression(penalty='l2'),
                    {'C':[0.01,0.1,1,10,100]}, cv=5, scoring='f1')

# 4. 输出
print("权重:", model.coef_, "截距:", model.intercept_)
print("概率:", model.predict_proba(X_te_s)[:5])  # 每行两类概率
print("类别:", model.predict(X_te_s)[:5])
```

**关键参数速查**：`penalty`（正则类型）、`C`（强度）、`solver`（求解器）、`class_weight`（类别平衡）、`multi_class`（多分类策略）、`max_iter`（最大迭代）。

***

## 速记口诀

| 要点     | 一句话                                            |
| :------- | :------------------------------------------------ |
| 本质     | 名为回归实为分类，线性回归+Sigmoid=概率           |
| 损失     | 交叉熵=对数损失，等价于 MLE，凸函数保证全局最优   |
| 不用 MSE | MSE+Sigmoid 非凸、梯度消失、概率依据不符          |
| 梯度     | $`\hat{y} - y`$，形式极简，是反向传播基石           |
| 多分类   | OvR（N 个二分类）vs Softmax（归一化概率）         |
| 正则     | C 越小正则越强；L1 稀疏特征选择，L2 稳定默认      |
| 前提     | 线性可分；需特征标准化；类别不平衡用 class_weight |
| 输出     | `predict_proba` 出概率，`predict` 出类别          |

---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：线性回归](05-线性回归.md) · [下一篇：决策树](07-决策树.md)
