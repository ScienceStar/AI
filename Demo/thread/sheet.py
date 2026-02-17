"""
数据分析和可视化示例
需要安装：pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

def generate_sample_data():
    """生成示例数据"""
    np.random.seed(42)
    
    # 生成月份数据
    months = ['1月', '2月', '3月', '4月', '5月', '6月', 
              '7月', '8月', '9月', '10月', '11月', '12月']
    
    # 生成三款产品的月销量
    product_a = np.random.randint(50, 150, 12)
    product_b = np.random.randint(30, 180, 12)
    product_c = np.random.randint(20, 200, 12)
    
    return months, product_a, product_b, product_c

def create_line_chart(months, product_a, product_b, product_c):
    """创建折线图"""
    plt.figure(figsize=(12, 6))
    
    x = np.arange(len(months))
    plt.plot(x, product_a, 'o-', label='产品A', linewidth=2, markersize=8)
    plt.plot(x, product_b, 's-', label='产品B', linewidth=2, markersize=8)
    plt.plot(x, product_c, '^-', label='产品C', linewidth=2, markersize=8)
    
    plt.title('2024年各产品月销量趋势', fontsize=16, pad=20)
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('销量（件）', fontsize=12)
    plt.xticks(x, months, rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('sales_trend.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_bar_chart(months, product_a, product_b, product_c):
    """创建柱状图"""
    plt.figure(figsize=(14, 6))
    
    x = np.arange(len(months))
    width = 0.25
    
    plt.bar(x - width, product_a, width, label='产品A', alpha=0.8)
    plt.bar(x, product_b, width, label='产品B', alpha=0.8)
    plt.bar(x + width, product_c, width, label='产品C', alpha=0.8)
    
    plt.title('2024年各产品月销量对比', fontsize=16, pad=20)
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('销量（件）', fontsize=12)
    plt.xticks(x, months, rotation=45)
    plt.legend()
    
    # 添加数据标签
    for i, v in enumerate(product_a):
        plt.text(i - width, v + 2, str(v), ha='center', va='bottom', fontsize=8)
    for i, v in enumerate(product_b):
        plt.text(i, v + 2, str(v), ha='center', va='bottom', fontsize=8)
    for i, v in enumerate(product_c):
        plt.text(i + width, v + 2, str(v), ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('sales_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_pie_chart():
    """创建饼图（市场份额）"""
    plt.figure(figsize=(8, 8))
    
    # 市场份额数据
    products = ['产品A', '产品B', '产品C', '其他']
    shares = [45, 30, 20, 5]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = (0.05, 0, 0, 0)  # 突出显示产品A
    
    plt.pie(shares, explode=explode, labels=products, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    
    plt.title('2024年市场份额分布', fontsize=16, pad=20)
    plt.axis('equal')  # 确保饼图是圆形
    
    plt.tight_layout()
    plt.savefig('market_share.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_data(product_a, product_b, product_c):
    """数据分析"""
    print("\n" + "=" * 50)
    print("        销售数据分析报告")
    print("=" * 50)
    
    products = {'产品A': product_a, '产品B': product_b, '产品C': product_c}
    
    for name, data in products.items():
        print(f"\n{name}：")
        print(f"  年总销量：{np.sum(data)} 件")
        print(f"  月平均：{np.mean(data):.1f} 件")
        print(f"  最高月销量：{np.max(data)} 件（第{np.argmax(data)+1}月）")
        print(f"  最低月销量：{np.min(data)} 件（第{np.argmin(data)+1}月）")
        print(f"  标准差：{np.std(data):.1f}（波动性）")
    
    # 相关性分析
    correlation_ab = np.corrcoef(product_a, product_b)[0, 1]
    correlation_ac = np.corrcoef(product_a, product_c)[0, 1]
    correlation_bc = np.corrcoef(product_b, product_c)[0, 1]
    
    print("\n" + "-" * 50)
    print("产品相关性分析：")
    print(f"  产品A与产品B：{correlation_ab:.3f}")
    print(f"  产品A与产品C：{correlation_ac:.3f}")
    print(f"  产品B与产品C：{correlation_bc:.3f}")
    
    if abs(correlation_ab) > 0.7:
        print("  产品A和B：强相关")
    elif abs(correlation_ab) > 0.3:
        print("  产品A和B：中等相关")
    else:
        print("  产品A和B：弱相关")

def main():
    """主函数"""
    print("正在生成销售数据...")
    months, product_a, product_b, product_c = generate_sample_data()
    
    # 数据分析
    analyze_data(product_a, product_b, product_c)
    
    print("\n正在生成可视化图表...")
    
    # 创建各种图表
    create_line_chart(months, product_a, product_b, product_c)
    create_bar_chart(months, product_a, product_b, product_c)
    create_pie_chart()
    
    print("\n图表已保存到当前目录！")

if __name__ == "__main__":
    main()