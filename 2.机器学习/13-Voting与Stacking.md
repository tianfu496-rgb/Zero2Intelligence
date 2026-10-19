# Voting 与 Stacking

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：XGBoost](12-XGBoost.md)

> 集成方法 · 固定聚合与学习聚合规则的区别


## Voting：先定义聚合规则

Hard Voting 对类别投票；Soft Voting 对类别概率做平均或加权平均。Soft Voting 需要基模型提供可比较的概率估计。

```math
\hat y=\mathrm{arg\,max}_k\sum_{b=1}^{B}\omega_b p_b(y=k\mid x)
```

## Stacking：再训练一个元模型

第一层模型产生预测，第二层模型学习怎样使用这些预测。训练元模型时应使用折外预测，避免让元模型看到基模型对自身训练样本的过度乐观输出。

1. 在每个训练折上拟合基模型。
2. 为留出折生成预测，拼成完整的折外特征矩阵。
3. 用折外特征和原标签训练元模型。
4. 基模型用完整训练集重训，再为新样本生成元特征。

## 初始化示例

```python
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
    StackingClassifier,
    VotingClassifier,
)
from sklearn.linear_model import LogisticRegression

estimators = [
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
    ('ada', AdaBoostClassifier(n_estimators=50, random_state=42)),
    ('gbdt', GradientBoostingClassifier(n_estimators=100, random_state=42)),
]

stacking = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(),
    cv=5,
    stack_method='predict_proba',
)

voting = VotingClassifier(
    estimators=estimators[:2],
    voting='soft',
)
```

两者都需要独立验证。时间序列、分组样本等任务还需按数据结构设计交叉验证，避免时间或分组泄漏。

参考：[StackingClassifier 文档](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html)。


---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：XGBoost](12-XGBoost.md)
