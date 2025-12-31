import numpy as np
import matplotlib.pyplot as plt

# 参数
n_petals = 6  # 花瓣数
theta = np.linspace(0, 2 * np.pi, 1000)

# 玫瑰曲线公式 r = cos(k * theta)
k = n_petals / 2
r = np.cos(k * theta)

# 极坐标绘图
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, polar=True)
ax.plot(theta, r, color='magenta', linewidth=2)
ax.fill_between(theta, 0, r, color='pink', alpha=0.3)

# 美化
ax.set_title("Beautiful Flower", fontsize=16)
ax.set_yticklabels([])  # 隐藏半径刻度
ax.set_xticklabels([])  # 隐藏角度刻度

plt.show()