import json
import os
from area import polygon_area
from trend import analyze_trend
from visualize import plot_trend

# 获取项目目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "polygons.json")

# 读取 JSON 数据
with open(file_path, "r") as f:
    polygons = json.load(f)

times = []
areas = []

# 遍历多边形数据
for item in polygons:
    times.append(int(item["time"]))
    area = polygon_area(item["points"])
    areas.append(area)
    print(f"Time={item['time']} Area={area}")

# 趋势分析
result = analyze_trend(times, areas)

print("\n=== Trend Analysis ===")
print("Slope (area change rate):", result["trend_slope"])
print("Predicted area in", result["future_time"], ":", result["predicted_area"])

# 可视化
plot_trend(
    times,
    areas,
    predicted=(result["future_time"], result["predicted_area"])
)