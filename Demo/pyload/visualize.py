import matplotlib.pyplot as plt


def plot_trend(times, areas, predicted=None):
    """
    可视化多边形面积趋势

    :param times: 时间序列，如 [2020, 2021, 2022]
    :param areas: 面积序列，如 [12.0, 15.0, 18.0]
    :param predicted: (future_time, future_area) 可选预测点
    """

    plt.figure(figsize=(8, 5))

    # 历史趋势
    plt.plot(times, areas, marker="o", linestyle="-", label="Historical Area")

    # 预测点
    if predicted:
        future_time, future_area = predicted
        plt.scatter(
            future_time,
            future_area,
            marker="x",
            s=100,
            label="Predicted Area"
        )

    plt.xlabel("Time")
    plt.ylabel("Area")
    plt.title("Polygon Area Trend Analysis")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()