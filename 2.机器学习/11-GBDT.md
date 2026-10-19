# GBDT：梯度提升树

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：AdaBoost](10-AdaBoost.md) · [下一篇：XGBoost](12-XGBoost.md)

> 集成方法 · 拟合损失函数的负梯度并逐轮更新


## 从“重加权样本”到“拟合梯度”

GBDT 构建加性模型：每一轮训练一棵回归树，为当前模型提供修正量。它使用损失对当前预测的负梯度作为拟合目标；平方误差下，负梯度与残差成比例。

$$
r_{it}=-\left.\frac{\partial\ell(y_i,F(x_i))}{\partial F(x_i)}\right|_{F=F_{t-1}}
$$

$$
F_t(x)=F_{t-1}(x)+\eta\gamma_t h_t(x)
$$

其中 $`h_t`$ 是本轮树，$`\gamma_t`$ 为步长，$`\eta`$ 为学习率。具体实现还可以为不同叶子分别优化输出值。

## 训练顺序

1. 初始化常数预测。
2. 根据当前预测计算负梯度。
3. 用回归树拟合该修正目标。
4. 缩放并累加这棵树的输出，重复训练。

## 初始化示例


```python
from sklearn.ensemble import GradientBoostingClassifier

gbdt = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,            # 通常用浅树（弱学习器）
    subsample=1.0
)
```


较小学习率通常需要更多树；树深影响交互复杂度，`subsample` 可引入样本随机性。使用验证集联合选择这些参数，而非单独增加轮数。

参考：[scikit-learn 梯度提升](https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting)。


---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：AdaBoost](10-AdaBoost.md) · [下一篇：XGBoost](12-XGBoost.md)
