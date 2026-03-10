# 神经网络算法程序说明

## 程序概述

这是一个**从头实现的神经网络（MLP）**程序，用于鸢尾花（Iris）多分类问题。不依赖深度学习框架，完全用NumPy实现核心算法。

## 核心算法

### 1. **网络架构**
- 输入层：4个神经元（对应4个特征）
- 隐藏层1：8个神经元
- 隐藏层2：6个神经元
- 输出层：3个神经元（对应3个分类）

### 2. **激活函数**
- **隐藏层**：ReLU (Rectified Linear Unit)
  $$f(x) = \max(0, x)$$
  
- **输出层**：Softmax
  $$f(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}$$

### 3. **损失函数**
交叉熵损失（Cross-Entropy Loss）：
$$L = -\frac{1}{m}\sum_{i=1}^{m} \sum_{j=1}^{k} y_{ij} \log(\hat{y}_{ij})$$

### 4. **训练算法**
- **优化器**：Mini-batch 梯度下降
- **学习率**：0.01
- **反向传播**：从输出层逐层计算梯度
- **权重初始化**：Xavier初始化

## 主要特性

✅ **从头实现**
- 不使用TensorFlow、PyTorch等框架
- 完全用NumPy实现前向传播和反向传播

✅ **完整的训练流程**
1. 数据加载和预处理
2. 数据标准化
3. One-hot编码
4. Mini-batch训练
5. 验证和测试

✅ **详细的输出信息**
- 每10个epoch显示训练进度
- 最终测试精度和混淆矩阵
- 训练过程图表

## 运行结果

**程序输出示例：**
```
============================================================
神经网络算法实现 - 鸢尾花分类
============================================================

数据集：150样本，4个特征，3个类别
分割：训练(96) 验证(24) 测试(30)

训练过程：
Epoch 10/100 - 损失: 1.0083 - 验证精度: 0.5417
Epoch 20/100 - 损失: 0.9443 - 验证精度: 0.5833
...
Epoch 100/100 - 损失: 0.4507 - 验证精度: 0.8750

评估结果：
- 测试精度: 0.8333 (83.33%)
- 混淆矩阵已生成

图表已保存为: neural_network_results.png
```

## 核心代码组件

### NeuralNetwork 类

```python
class NeuralNetwork:
    def __init__(self, layer_sizes, learning_rate, random_state)
    def forward_propagation(self, X)              # 前向传播
    def backward_propagation(self, X, y, ...)    # 反向传播
    def update_parameters(self, ...)               # 参数更新
    def train(self, X_train, y_train, ...)        # 训练方法
    def predict(self, X)                          # 预测方法
```

### 关键方法

| 方法 | 功能 |
|------|------|
| `forward_propagation()` | 执行前向传播，返回每层激活值 |
| `backward_propagation()` | 从输出层反向计算梯度 |
| `cross_entropy_loss()` | 计算交叉熵损失 |
| `relu()` / `softmax()` | 激活函数实现 |

## 学习知识点

这个程序涵盖的重要概念：

1. **神经网络基础**
   - 权重和偏置初始化
   - 前向传播计算
   
2. **反向传播算法**
   - 链式法则求导
   - 梯度计算和更新
   
3. **优化技巧**
   - Mini-batch训练
   - 学习率设置
   - 数据标准化
   
4. **评估指标**
   - 交叉熵损失
   - 准确率
   - 混淆矩阵

## 扩展方向

可以进一步改进的方向：

- [ ] 添加Dropout正则化
- [ ] 实现动量算法（Momentum）
- [ ] 支持自定义网络深度
- [ ] 添加学习率衰减
- [ ] 实现批量归一化（Batch Normalization）
- [ ] 支持不同的激活函数
- [ ] 可视化网络结构

## 代码文件位置

📁 `/Users/pr/Public/workspace/Python/Demo/neural_network.py`

## 依赖

- `numpy` - 数值计算
- `scikit-learn` - 数据集和评估指标
- `matplotlib` - 可视化

---

这是一个完整的、可运行的神经网络实现，适合学习和理解深度学习基础！
