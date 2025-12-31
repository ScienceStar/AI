def polygon_area(points):
    """
    Shoelace Formula
    points: [(x1,y1),(x2,y2),...]
    """
    area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2