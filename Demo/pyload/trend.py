import numpy as np
from sklearn.linear_model import LinearRegression

def analyze_trend(times, areas):
    """
    线性趋势 + 未来预测
    """
    X = np.array(times).reshape(-1, 1)
    y = np.array(areas)

    model = LinearRegression()
    model.fit(X, y)

    trend = model.coef_[0]

    future_time = max(times) + 1
    future_area = model.predict([[future_time]])[0]

    return {
        "trend_slope": trend,
        "future_time": future_time,
        "predicted_area": future_area
    }