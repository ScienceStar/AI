import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 银河系螺旋臂星系绘制
# -----------------------------
num_stars = 2000
theta = np.random.uniform(0, 4*np.pi, num_stars)
r = np.random.uniform(0.2, 10, num_stars)
spiral_offset = theta * 0.3
x = r * np.cos(theta + spiral_offset)
y = r * np.sin(theta + spiral_offset)

plt.figure(figsize=(10,10))
plt.scatter(x, y, s=1, color="white")  # 普通恒星
plt.gca().set_facecolor("black")

# -----------------------------
# 添加主要恒星
# -----------------------------
num_major_stars = 10
theta_major = np.random.uniform(0, 4*np.pi, num_major_stars)
r_major = np.random.uniform(1, 9, num_major_stars)
x_major = r_major * np.cos(theta_major + theta_major * 0.3)
y_major = r_major * np.sin(theta_major + theta_major * 0.3)

plt.scatter(x_major, y_major, s=50, color="yellow", edgecolors="orange", label="主要恒星")

# -----------------------------
# 行星轨道模拟
# -----------------------------
num_planets = 5
planet_colors = ["red", "blue", "green", "yellow", "cyan"]
radii = np.linspace(1, 5, num_planets)
angles = np.linspace(0, 2*np.pi, 100)

for i, radius in enumerate(radii):
    x_orbit = radius * np.cos(angles)
    y_orbit = radius * np.sin(angles)
    plt.plot(x_orbit, y_orbit, color=planet_colors[i], label=f"Planet {i+1}")

    orbit_length = 2 * np.pi * radius
    period = np.sqrt(radius**3)
    print(f"Planet {i+1}: radius={radius:.2f}, orbit_length={orbit_length:.2f}, period~{period:.2f}")

plt.title("银河系示意图（主要恒星 + 行星轨道）", color="white")
plt.axis("off")
plt.legend()
plt.show()