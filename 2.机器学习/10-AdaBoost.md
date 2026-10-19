# AdaBoost

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：随机森林 Random Forest](09-随机森林.md) · [下一篇：GBDT：梯度提升树](11-GBDT.md)

> 集成方法 · 通过样本权重逐轮训练弱分类器


## 从装袋到提升

AdaBoost 顺序训练弱分类器。前一轮错误分类的样本会获得更高权重，下一轮模型因此更加关注难例；最后将弱分类器加权组合。

## 二分类的经典形式

下面采用标签 $`y_i\in\{-1,+1\}`$ 的二分类 AdaBoost 形式。它与多分类 SAMME 的系数形式有区别。

$$
\epsilon_t=\sum_{i=1}^{n}w_i^{(t)}\mathbf{1}[h_t(x_i)\ne y_i]
$$

$$
\alpha_t=\frac12\log\frac{1-\epsilon_t}{\epsilon_t}
$$

$$
w_i^{(t+1)}=\frac{w_i^{(t)}\exp(-\alpha_ty_ih_t(x_i))}{Z_t}
$$

$`Z_t`$ 使权重之和恢复为 1；最终预测为 $`H(x)=\operatorname{sign}(\sum_t\alpha_th_t(x))`$。

## 初始化示例


```python
from sklearn.ensemble import AdaBoostClassifier

ada = AdaBoostClassifier(
    n_estimators=50,
    learning_rate=1.0
)
```


`n_estimators` 控制轮数，`learning_rate` 调节每轮贡献。常用浅树作为基学习器。错误标签也可能被不断加权，因此应检查噪声、异常点与验证集表现。

新版 scikit-learn 的 `AdaBoostClassifier` 已移除旧的 `algorithm` 参数；示例采用当前接口。参考：[AdaBoostClassifier 文档](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html)。


---

[仓库首页](../README.md) · [本主题目录](README.md) · [上一篇：随机森林 Random Forest](09-随机森林.md) · [下一篇：GBDT：梯度提升树](11-GBDT.md)
