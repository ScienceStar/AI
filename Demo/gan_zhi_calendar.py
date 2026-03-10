import tkinter as tk
from tkinter import messagebox
import math
import time
import threading

class GanZhiCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("干支纪年轮盘")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # 定义天干和地支
        self.tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 1900年是庚子年
        self.base_year = 1900
        self.base_gan_index = 6  # 庚
        self.base_zhi_index = 0  # 子
        
        self.current_year = 2024
        self.gan_angle_offset = 0
        self.zhi_angle_offset = 0
        self.is_rotating = False
        
        self.setup_ui()
        self.init_wheel_angles()
        
    def setup_ui(self):
        """设置UI界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(pady=15)
        
        title_label = tk.Label(title_frame, text="干支纪年同心圆轮盘", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack()
        
        # 输入框架
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="输入年份:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.year_entry = tk.Entry(input_frame, font=("Arial", 13), width=15)
        self.year_entry.pack(side=tk.LEFT, padx=5)
        self.year_entry.insert(0, "2024")
        self.year_entry.bind("<Return>", lambda e: self.on_search())  # 按回车键搜索
        
        tk.Button(input_frame, text="查询", font=("Arial", 12), command=self.on_search, 
                 bg="#4CAF50", fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        
        # 轮盘画布
        self.canvas = tk.Canvas(self.root, width=550, height=400, bg="white", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(pady=15)
        
        # 信息显示框架
        info_frame = tk.Frame(self.root, bg="#f0f0f0")
        info_frame.pack(pady=12)
        
        tk.Label(info_frame, text="年份: ", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.year_label = tk.Label(info_frame, text="2024年", font=("Arial", 13, "bold"), 
                                   bg="#f0f0f0", fg="#2196F3")
        self.year_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(info_frame, text="天干: ", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.gan_label = tk.Label(info_frame, text="甲", font=("Arial", 14, "bold"), 
                                 bg="#f0f0f0", fg="#FF9800")
        self.gan_label.pack(side=tk.LEFT, padx=3)
        
        tk.Label(info_frame, text="地支: ", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.zhi_label = tk.Label(info_frame, text="子", font=("Arial", 14, "bold"), 
                                 bg="#f0f0f0", fg="#2196F3")
        self.zhi_label.pack(side=tk.LEFT, padx=3)
        
        tk.Label(info_frame, text="纪年: ", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.gan_zhi_label = tk.Label(info_frame, text="甲子年", font=("Arial", 14, "bold"), 
                                      bg="#f0f0f0", fg="#FF5722")
        self.gan_zhi_label.pack(side=tk.LEFT, padx=3)
        
        # 快速按钮
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=8)
        
        tk.Button(button_frame, text="2024", font=("Arial", 10), command=lambda: self.quick_search(2024)).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="2025", font=("Arial", 10), command=lambda: self.quick_search(2025)).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="2012龙", font=("Arial", 10), command=lambda: self.quick_search(2012)).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="1998虎", font=("Arial", 10), command=lambda: self.quick_search(1998)).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="1900庚子", font=("Arial", 10), command=lambda: self.quick_search(1900)).pack(side=tk.LEFT, padx=2)
        
        self.draw_concentric_wheels()
        
    def init_wheel_angles(self):
        """初始化轮盘角度"""
        gan_index, zhi_index = self.get_gan_zhi_index(2024)
        self.gan_angle_offset = gan_index * 36  # 10个天干，每个占36度
        self.zhi_angle_offset = zhi_index * 30  # 12个地支，每个占30度
    
    def get_gan_zhi_index(self, year):
        """根据年份获取天干和地支的索引"""
        gap = year - self.base_year
        gan_index = (self.base_gan_index + gap) % 10
        zhi_index = (self.base_zhi_index + gap) % 12
        return gan_index, zhi_index
    
    def draw_concentric_wheels(self):
        """绘制同心圆轮盘"""
        self.canvas.delete("all")
        
        center_x, center_y = 275, 200
        outer_radius = 140  # 外圆半径（地支）
        inner_radius = 80   # 内圆半径（天干）
        
        # 绘制最外圆（装饰）
        self.canvas.create_oval(center_x - outer_radius, center_y - outer_radius,
                               center_x + outer_radius, center_y + outer_radius,
                               outline="#333333", width=2)
        
        # 绘制地支圆环
        outer_ring_radius = outer_radius - 20
        self.canvas.create_oval(center_x - outer_ring_radius, center_y - outer_ring_radius,
                               center_x + outer_ring_radius, center_y + outer_ring_radius,
                               outline="#2196F3", width=2)
        
        # 绘制12个地支（外圆）
        for i in range(12):
            angle = (i * 30 + self.zhi_angle_offset) * math.pi / 180
            
            # 外圆上的位置
            x1 = center_x + outer_radius * math.cos(angle)
            y1 = center_y + outer_radius * math.sin(angle)
            
            # 内环上的位置
            x2 = center_x + outer_ring_radius * math.cos(angle)
            y2 = center_y + outer_ring_radius * math.sin(angle)
            
            # 绘制分隔线
            self.canvas.create_line(x1, y1, x2, y2, fill="#90CAF9", width=1)
            
            # 绘制地支文字
            text_x = center_x + (outer_radius + outer_ring_radius) / 2 * math.cos(angle)
            text_y = center_y + (outer_radius + outer_ring_radius) / 2 * math.sin(angle)
            zhi = self.di_zhi[i]
            self.canvas.create_text(text_x, text_y, text=zhi, font=("Arial", 12, "bold"), 
                                   fill="#1565C0")
        
        # 绘制内圆（天干外圈）
        self.canvas.create_oval(center_x - inner_radius, center_y - inner_radius,
                               center_x + inner_radius, center_y + inner_radius,
                               outline="#FF9800", width=2)
        
        # 绘制10个天干（内圆）
        inner_text_radius = inner_radius - 15
        for i in range(10):
            angle = (i * 36 + self.gan_angle_offset) * math.pi / 180
            
            # 外圆上的位置（内圆周）
            x1 = center_x + inner_radius * math.cos(angle)
            y1 = center_y + inner_radius * math.sin(angle)
            
            # 内圆文字位置
            x2 = center_x + inner_text_radius * math.cos(angle)
            y2 = center_y + inner_text_radius * math.sin(angle)
            
            # 绘制分隔线
            self.canvas.create_line(x1, y1, x2, y2, fill="#FFD699", width=1)
            
            # 绘制天干文字
            gan = self.tian_gan[i]
            self.canvas.create_text(x1, y1, text=gan, font=("Arial", 11, "bold"), 
                                   fill="#FF6F00", anchor="center")
        
        # 绘制中心圆（天干中心）
        center_r = 25
        self.canvas.create_oval(center_x - center_r, center_y - center_r,
                               center_x + center_r, center_y + center_r,
                               fill="#FFD700", outline="#FFA500", width=2)
        
        # 绘制中心点
        self.canvas.create_oval(center_x - 5, center_y - 5,
                               center_x + 5, center_y + 5,
                               fill="#333333")
        
        # 绘制指针（顶部）
        pointer_x = center_x
        pointer_y = center_y - outer_radius - 10
        self.canvas.create_polygon(pointer_x - 8, pointer_y + 15,
                                  pointer_x + 8, pointer_y + 15,
                                  pointer_x, pointer_y,
                                  fill="#FF0000", outline="#CC0000", width=2)
    
    def rotate_wheels(self, target_gan_index, target_zhi_index, steps=80):
        """轮盘转动动画"""
        if self.is_rotating:
            return
        
        self.is_rotating = True
        
        # 天干转动参数（每个36度）
        target_gan_angle = target_gan_index * 36
        full_rotations_gan = 3
        total_angle_gan = full_rotations_gan * 360 + target_gan_angle
        
        # 地支转动参数（每个30度）
        target_zhi_angle = target_zhi_index * 30
        full_rotations_zhi = 4
        total_angle_zhi = full_rotations_zhi * 360 + target_zhi_angle
        
        step_angle_gan = total_angle_gan / steps
        step_angle_zhi = total_angle_zhi / steps
        
        for step in range(steps + 1):
            self.gan_angle_offset = (step_angle_gan * step) % 360
            self.zhi_angle_offset = (step_angle_zhi * step) % 360
            self.draw_concentric_wheels()
            self.root.update()
            time.sleep(0.008)
        
        self.is_rotating = False
    
    def on_search(self):
        """搜索按钮点击处理"""
        try:
            year = int(self.year_entry.get())
            if year < 1900 or year > 2100:
                messagebox.showwarning("输入错误", "请输入1900-2100年之间的年份")
                return
            self.quick_search(year)
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的年份数字")
    
    def quick_search(self, year):
        """快速查询"""
        gan_index, zhi_index = self.get_gan_zhi_index(year)
        gan = self.tian_gan[gan_index]
        zhi = self.di_zhi[zhi_index]
        gan_zhi = gan + zhi
        
        self.current_year = year
        
        # 更新标签
        self.year_label.config(text=f"{year}年")
        self.gan_label.config(text=gan)
        self.zhi_label.config(text=zhi)
        self.gan_zhi_label.config(text=f"{gan_zhi}年")
        
        # 在线程中启动转动动画
        threading.Thread(target=self.rotate_wheels, args=(gan_index, zhi_index), daemon=True).start()


def main():
    root = tk.Tk()
    app = GanZhiCalendar(root)
    root.mainloop()


if __name__ == "__main__":
    main()

