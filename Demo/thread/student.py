"""
学生成绩管理系统
演示：类、列表、字典、文件操作
"""

import json
import os
from datetime import datetime

class Student:
    """学生类"""
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.scores = {}  # 课程:成绩
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def add_score(self, course, score):
        """添加成绩"""
        if 0 <= score <= 100:
            self.scores[course] = score
            return True
        return False
    
    def get_average(self):
        """计算平均分"""
        if not self.scores:
            return 0
        return sum(self.scores.values()) / len(self.scores)
    
    def to_dict(self):
        """转换为字典（用于存储）"""
        return {
            'name': self.name,
            'student_id': self.student_id,
            'scores': self.scores,
            'created_at': self.created_at
        }

class GradeManager:
    """成绩管理类"""
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = []
        self.load_data()
    
    def add_student(self, name, student_id):
        """添加学生"""
        # 检查学号是否已存在
        if any(s.student_id == student_id for s in self.students):
            print(f"学号 {student_id} 已存在！")
            return False
        
        student = Student(name, student_id)
        self.students.append(student)
        self.save_data()
        print(f"学生 {name} 添加成功！")
        return True
    
    def find_student(self, student_id):
        """查找学生"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def add_score(self, student_id, course, score):
        """添加成绩"""
        student = self.find_student(student_id)
        if student:
            if student.add_score(course, score):
                self.save_data()
                print(f"成绩添加成功：{student.name} - {course}: {score}")
            else:
                print("成绩必须在0-100之间！")
        else:
            print(f"未找到学号为 {student_id} 的学生！")
    
    def show_all_students(self):
        """显示所有学生"""
        if not self.students:
            print("暂无学生数据")
            return
        
        print("\n" + "=" * 60)
        print(f"{'学号':<12} {'姓名':<10} {'课程数':<8} {'平均分':<8} {'注册时间'}")
        print("-" * 60)
        
        for s in self.students:
            avg = s.get_average()
            print(f"{s.student_id:<12} {s.name:<10} {len(s.scores):<8} {avg:<8.2f} {s.created_at}")
        print("=" * 60)
    
    def show_student_detail(self, student_id):
        """显示学生详细信息"""
        student = self.find_student(student_id)
        if not student:
            print(f"未找到学号为 {student_id} 的学生！")
            return
        
        print(f"\n学生信息：{student.name} (学号：{student.student_id})")
        print(f"注册时间：{student.created_at}")
        if student.scores:
            print("\n成绩单：")
            for course, score in student.scores.items():
                print(f"  {course}: {score}")
            print(f"\n平均分：{student.get_average():.2f}")
        else:
            print("暂无成绩记录")
    
    def save_data(self):
        """保存数据到文件"""
        data = [s.to_dict() for s in self.students]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        student = Student(item['name'], item['student_id'])
                        student.scores = item['scores']
                        student.created_at = item['created_at']
                        self.students.append(student)
            except:
                print("数据文件损坏，将创建新文件")

def main():
    """主函数"""
    manager = GradeManager()
    
    while True:
        print("\n" + "=" * 40)
        print("     学生成绩管理系统")
        print("=" * 40)
        print("1. 添加学生")
        print("2. 添加成绩")
        print("3. 查看所有学生")
        print("4. 查看学生详情")
        print("5. 退出系统")
        print("-" * 40)
        
        choice = input("请选择操作 (1-5): ").strip()
        
        if choice == '1':
            name = input("请输入学生姓名: ")
            student_id = input("请输入学号: ")
            manager.add_student(name, student_id)
        
        elif choice == '2':
            student_id = input("请输入学号: ")
            course = input("请输入课程名称: ")
            try:
                score = float(input("请输入成绩: "))
                manager.add_score(student_id, course, score)
            except ValueError:
                print("成绩必须是数字！")
        
        elif choice == '3':
            manager.show_all_students()
        
        elif choice == '4':
            student_id = input("请输入学号: ")
            manager.show_student_detail(student_id)
        
        elif choice == '5':
            print("感谢使用，再见！")
            break
        
        else:
            print("无效选择，请重新输入！")

if __name__ == "__main__":
    main()