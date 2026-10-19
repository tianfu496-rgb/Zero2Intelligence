# XGBoost

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：GBDT：梯度提升树](11-GBDT.md) · [下一篇：Voting 与 Stacking](13-Voting与Stacking.md)

> 集成方法 · 二阶近似、树复杂度惩罚与梯度提升


## 与 GBDT 的关系

XGBoost 提供梯度提升的高效实现。树提升器在每轮同时利用损失的一阶、二阶信息，并在目标中加入树的复杂度惩罚。它也支持线性提升器，具体行为取决于 `booster`。

## 树提升的目标

$$
\mathcal L=\sum_i\ell(y_i,\hat y_i)+\sum_t\Omega(f_t)
$$

对一棵有 $`T`$ 个叶子、叶子输出为 $`w_j`$ 的树，一种常见惩罚形式为：

$$
\Omega(f)=\gamma T+\frac\lambda2\sum_{j=1}^{T}w_j^2
$$

第 $`t`$ 轮的二阶近似省略常数后为：

$$
\widetilde{\mathcal L}^{(t)}=\sum_i\left[g_if_t(x_i)+\frac12h_if_t(x_i)^2\right]+\Omega(f_t)
$$

这里 $`g_i`$、$`h_i`$ 分别是损失对当前预测的一阶、二阶导数。它们用于选择分裂与叶子输出。

## 初始化示例

`xgboost` 需单独安装。以下仅初始化二分类模型，训练数据应先划分完成。

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='binary:logistic',
    eval_metric='logloss',
    random_state=42,
)
```

重点调节学习率、树数、树深、行列采样比例与正则系数。缺失值分支可以在训练时学习；这并不免除数据质量检查。模型优劣应在相同数据划分和指标下比较。

参考：[XGBoost 提升树原理](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)。


---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：GBDT：梯度提升树](11-GBDT.md) · [下一篇：Voting 与 Stacking](13-Voting与Stacking.md)
