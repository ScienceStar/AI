"""
神经网络算法实现
从头构建一个简单的多层感知器（MLP）
用于鸢尾花分类问题
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt


class NeuralNetwork:
    """
    简单的多层感知器（MLP）神经网络
    使用反向传播算法训练
    """
    
    def __init__(self, layer_sizes, learning_rate=0.01, random_state=42):
        """
        初始化神经网络
        
        Args:
            layer_sizes: 列表，每层的神经元数量，如[4, 8, 6, 3]表示
                        输入层4个，隐藏层8个，隐藏层6个，输出层3个
            learning_rate: 学习率
            random_state: 随机种子
        """
        np.random.seed(random_state)
        self.learning_rate = learning_rate
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        
        # 初始化权重和偏置
        self.weights = []
        self.biases = []
        
        for i in range(self.num_layers - 1):
            # 使用Xavier初始化
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * \
                np.sqrt(1.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            
            self.weights.append(w)
            self.biases.append(b)
    
    @staticmethod
    def relu(x):
        """ReLU激活函数"""
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x):
        """ReLU导数"""
        return (x > 0).astype(float)
    
    @staticmethod
    def softmax(x):
        """Softmax激活函数用于输出层"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    @staticmethod
    def cross_entropy_loss(y_true, y_pred):
        """交叉熵损失函数"""
        m = y_true.shape[0]
        # 防止log(0)
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        loss = -np.sum(y_true * np.log(y_pred)) / m
        return loss
    
    def forward_propagation(self, X):
        """
        前向传播
        
        Args:
            X: 输入数据 (m, n_input)
            
        Returns:
            activations: 每层的激活值
            z_values: 每层的未激活值
            output: 网络输出
        """
        activations = [X]
        z_values = []
        
        current_input = X
        
        # 隐藏层：使用ReLU激活
        for i in range(self.num_layers - 2):
            z = np.dot(current_input, self.weights[i]) + self.biases[i]
            z_values.append(z)
            current_input = self.relu(z)
            activations.append(current_input)
        
        # 输出层：使用Softmax激活
        z = np.dot(current_input, self.weights[-1]) + self.biases[-1]
        z_values.append(z)
        output = self.softmax(z)
        activations.append(output)
        
        return activations, z_values, output
    
    def backward_propagation(self, X, y_true, activations, z_values, output):
        """
        反向传播
        
        Args:
            X: 输入数据
            y_true: 真实标签（one-hot编码）
            activations: 前向传播中的激活值
            z_values: 前向传播中的z值
            output: 网络输出
            
        Returns:
            weight_gradients: 权重梯度
            bias_gradients: 偏置梯度
        """
        m = X.shape[0]
        weight_gradients = []
        bias_gradients = []
        
        # 输出层的梯度
        delta = output - y_true  # 对于softmax+cross_entropy
        
        # 反向计算梯度
        for i in range(self.num_layers - 2, -1, -1):
            # 计算权重和偏置梯度
            dw = np.dot(activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            weight_gradients.insert(0, dw)
            bias_gradients.insert(0, db)
            
            # 计算前一层的delta（如果不是输入层）
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * \
                        self.relu_derivative(z_values[i-1])
        
        return weight_gradients, bias_gradients
    
    def update_parameters(self, weight_gradients, bias_gradients):
        """更新权重和偏置"""
        for i in range(self.num_layers - 1):
            self.weights[i] -= self.learning_rate * weight_gradients[i]
            self.biases[i] -= self.learning_rate * bias_gradients[i]
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
        """
        训练神经网络
        
        Args:
            X_train: 训练数据
            y_train: 训练标签（one-hot编码）
            X_val: 验证数据
            y_val: 验证标签
            epochs: 训练轮数
            batch_size: 批大小
            
        Returns:
            train_losses: 训练损失历史
            val_accuracies: 验证精度历史
        """
        train_losses = []
        val_accuracies = []
        
        m = X_train.shape[0]
        
        for epoch in range(epochs):
            # 随机打乱数据
            indices = np.random.permutation(m)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]
            
            # Mini-batch梯度下降
            for i in range(0, m, batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]
                
                # 前向传播
                activations, z_values, output = self.forward_propagation(X_batch)
                
                # 反向传播
                weight_grads, bias_grads = self.backward_propagation(
                    X_batch, y_batch, activations, z_values, output
                )
                
                # 更新参数
                self.update_parameters(weight_grads, bias_grads)
            
            # 计算训练损失
            _, _, train_output = self.forward_propagation(X_train)
            train_loss = self.cross_entropy_loss(y_train, train_output)
            train_losses.append(train_loss)
            
            # 计算验证精度
            _, _, val_output = self.forward_propagation(X_val)
            val_pred = np.argmax(val_output, axis=1)
            val_true = np.argmax(y_val, axis=1)
            val_acc = accuracy_score(val_true, val_pred)
            val_accuracies.append(val_acc)
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs} - "
                      f"损失: {train_loss:.4f} - "
                      f"验证精度: {val_acc:.4f}")
        
        return train_losses, val_accuracies
    
    def predict(self, X):
        """预测"""
        _, _, output = self.forward_propagation(X)
        return np.argmax(output, axis=1)


def main():
    """主程序：使用鸢尾花数据集演示神经网络"""
    
    print("="*60)
    print("神经网络算法实现 - 鸢尾花分类")
    print("="*60)
    
    # 加载数据
    print("\n1. 加载数据...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    print(f"   - 数据集大小: {X.shape[0]}样本")
    print(f"   - 特征数: {X.shape[1]}")
    print(f"   - 类别数: {len(np.unique(y))}")
    
    # 分割数据
    print("\n2. 分割数据...")
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.2, random_state=42
    )
    
    print(f"   - 训练集: {X_train.shape[0]}样本")
    print(f"   - 验证集: {X_val.shape[0]}样本")
    print(f"   - 测试集: {X_test.shape[0]}样本")
    
    # 数据标准化
    print("\n3. 数据标准化...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)
    
    # 转换标签为one-hot编码
    def to_one_hot(y, num_classes):
        one_hot = np.zeros((y.shape[0], num_classes))
        one_hot[np.arange(y.shape[0]), y] = 1
        return one_hot
    
    y_train_oh = to_one_hot(y_train, 3)
    y_val_oh = to_one_hot(y_val, 3)
    y_test_oh = to_one_hot(y_test, 3)
    
    # 创建神经网络
    print("\n4. 创建神经网络...")
    # 网络结构: 输入层(4) -> 隐藏层(8) -> 隐藏层(6) -> 输出层(3)
    nn = NeuralNetwork(
        layer_sizes=[4, 8, 6, 3],
        learning_rate=0.01,
        random_state=42
    )
    print("   - 网络结构: 4 -> 8 -> 6 -> 3")
    print("   - 学习率: 0.01")
    print("   - 激活函数: ReLU (隐藏层), Softmax (输出层)")
    
    # 训练模型
    print("\n5. 训练模型...")
    train_losses, val_accuracies = nn.train(
        X_train, y_train_oh,
        X_val, y_val_oh,
        epochs=100,
        batch_size=16
    )
    
    # 测试模型
    print("\n6. 评估模型...")
    y_pred = nn.predict(X_test)
    y_true = np.argmax(y_test_oh, axis=1)
    
    test_accuracy = accuracy_score(y_true, y_pred)
    print(f"   - 测试精度: {test_accuracy:.4f}")
    
    # 混淆矩阵
    conf_matrix = confusion_matrix(y_true, y_pred)
    print("\n   混淆矩阵:")
    print(f"   {conf_matrix}")
    
    # 可视化
    print("\n7. 保存可视化图表...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # 训练损失
    axes[0].plot(train_losses, label='训练损失')
    axes[0].set_xlabel('轮数')
    axes[0].set_ylabel('损失')
    axes[0].set_title('训练过程中的损失')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 验证精度
    axes[1].plot(val_accuracies, label='验证精度', color='green')
    axes[1].set_xlabel('轮数')
    axes[1].set_ylabel('精度')
    axes[1].set_title('验证过程中的精度')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/pr/Public/workspace/Python/Demo/neural_network_results.png', dpi=100)
    print("   - 图表已保存到: neural_network_results.png")
    
    print("\n" + "="*60)
    print("训练完成！")
    print("="*60)


if __name__ == "__main__":
    main()
