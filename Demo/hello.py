
def bucket_sort(arr, bucket_count=None):
    """对数字列表进行桶排序，返回新排序列表（不就地修改）。
    bucket_count 默认取 len(arr)，也可以指定为更小/更大值以调整性能。
    """
    if not arr:
        return []

    n = len(arr)
    if bucket_count is None:
        bucket_count = max(1, n)

    min_val, max_val = min(arr), max(arr)
    if min_val == max_val:
        return arr.copy()

    # 初始化桶
    buckets = [[] for _ in range(bucket_count)]

    # 将元素分配到桶中
    span = max_val - min_val
    for x in arr:
        idx = int((x - min_val) / span * (bucket_count - 1))
        buckets[idx].append(x)

    # 排序并合并（这里用内置 sort；也可用插入排序优化小桶）
    result = []
    for b in buckets:
        b.sort()
        result.extend(b)
    return result

if __name__ == "__main__":
    a = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51, 0.68]
    assert bucket_sort(a) == sorted(a)

    b = [3, -1, 7, 4, 2, 2, -5]
    assert bucket_sort(b) == sorted(b)

    print("示例排序：", bucket_sort(a))
    print("整数排序：", bucket_sort(b))