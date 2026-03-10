import math
import heapq
from typing import List, Tuple, Dict, Optional
import re

class PromptBasedPathPlanner:
    """基于提示词的路径规划器"""
    
    def __init__(self, grid_size: Tuple[int, int] = (10, 10)):
        self.width, self.height = grid_size
        self.grid = [[0] * self.width for _ in range(self.height)]  # 0表示可通行
        self.obstacles = []
        self.start = (0, 0)
        self.end = (self.width-1, self.height-1)
        
    def parse_prompt(self, prompt: str) -> Dict:
        """解析用户提示，提取路径规划参数"""
        prompt_lower = prompt.lower()
        params = {
            'start': self.start,
            'end': self.end,
            'avoid_areas': [],
            'prefer_areas': [],
            'algorithm': 'astar',  # 默认使用A*算法
            'optimization': 'shortest'  # 默认最短路径
        }
        
        # 解析起点
        start_match = re.search(r'从\(?(\d+),(\d+)\)?出发|起点[是为]\(?(\d+),(\d+)\)?', prompt)
        if start_match:
            groups = start_match.groups()
            if groups[0] and groups[1]:
                params['start'] = (int(groups[0]), int(groups[1]))
            elif groups[2] and groups[3]:
                params['start'] = (int(groups[2]), int(groups[3]))
        
        # 解析终点
        end_match = re.search(r'到\(?(\d+),(\d+)\)?|终点[是为]\(?(\d+),(\d+)\)?|前往\(?(\d+),(\d+)\)?', prompt)
        if end_match:
            groups = end_match.groups()
            for i in range(0, len(groups), 2):
                if groups[i] and groups[i+1]:
                    params['end'] = (int(groups[i]), int(groups[i+1]))
                    break
        
        # 解析避开区域
        avoid_matches = re.findall(r'避开\(?(\d+),(\d+)\)?|绕过\(?(\d+),(\d+)\)?', prompt)
        for match in avoid_matches:
            for i in range(0, len(match), 2):
                if match[i] and match[i+1]:
                    params['avoid_areas'].append((int(match[i]), int(match[i+1])))
        
        # 解析优先区域
        prefer_matches = re.findall(r'优先经过\(?(\d+),(\d+)\)?|尽量走\(?(\d+),(\d+)\)?', prompt)
        for match in prefer_matches:
            for i in range(0, len(match), 2):
                if match[i] and match[i+1]:
                    params['prefer_areas'].append((int(match[i]), int(match[i+1])))
        
        # 解析算法选择
        if 'dijkstra' in prompt_lower:
            params['algorithm'] = 'dijkstra'
        elif 'bfs' in prompt_lower:
            params['algorithm'] = 'bfs'
        elif '贪心' in prompt_lower or 'greedy' in prompt_lower:
            params['algorithm'] = 'greedy'
        
        # 解析优化目标
        if '最快' in prompt_lower or '时间最短' in prompt_lower:
            params['optimization'] = 'fastest'
        elif '最安全' in prompt_lower or '避开障碍' in prompt_lower:
            params['optimization'] = 'safest'
        elif '风景好' in prompt_lower or '最美' in prompt_lower:
            params['optimization'] = 'scenic'
        
        return params
    
    def setup_grid(self, params: Dict):
        """根据参数设置网格"""
        # 重置网格
        self.grid = [[0] * self.width for _ in range(self.height)]
        
        # 设置障碍物（避开区域）
        for x, y in params['avoid_areas']:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = 1  # 1表示障碍物
                self.obstacles.append((x, y))
        
        # 优先区域设置不同的权重
        self.prefer_weights = {}
        for x, y in params['prefer_areas']:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.prefer_weights[(x, y)] = 0.5  # 更低的花费
    
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """启发式函数（曼哈顿距离）"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """获取相邻可通行节点"""
        x, y = pos
        neighbors = []
        # 4个方向：上、下、左、右
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] == 0:  # 可通行
                    neighbors.append((nx, ny))
        
        return neighbors
    
    def calculate_cost(self, current: Tuple[int, int], next_pos: Tuple[int, int], params: Dict) -> float:
        """计算移动成本"""
        # 基础成本
        base_cost = 1.0
        
        # 优先区域成本更低
        if next_pos in self.prefer_weights:
            base_cost *= self.prefer_weights[next_pos]
        
        # 根据优化目标调整成本
        if params['optimization'] == 'safest':
            # 远离障碍物的成本更低
            for obstacle in self.obstacles:
                dist = self.heuristic(next_pos, obstacle)
                if dist < 2:  # 靠近障碍物
                    base_cost *= (3 - dist)
        
        return base_cost
    
    def astar_search(self, start: Tuple[int, int], end: Tuple[int, int], params: Dict) -> Optional[List[Tuple[int, int]]]:
        """A*算法搜索路径"""
        frontier = [(0, start)]  # 优先队列
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            current = heapq.heappop(frontier)[1]
            
            if current == end:
                break
            
            for next_pos in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.calculate_cost(current, next_pos, params)
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(end, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        # 重建路径
        if end not in came_from:
            return None
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        
        return path
    
    def dijkstra_search(self, start: Tuple[int, int], end: Tuple[int, int], params: Dict) -> Optional[List[Tuple[int, int]]]:
        """Dijkstra算法搜索路径"""
        return self.astar_search(start, end, params)  # 实际上A*当heuristic为0时就是Dijkstra
    
    def bfs_search(self, start: Tuple[int, int], end: Tuple[int, int], params: Dict) -> Optional[List[Tuple[int, int]]]:
        """BFS算法搜索路径"""
        from collections import deque
        
        queue = deque([start])
        came_from = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                break
            
            for next_pos in self.get_neighbors(current):
                if next_pos not in came_from:
                    queue.append(next_pos)
                    came_from[next_pos] = current
        
        # 重建路径
        if end not in came_from:
            return None
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        
        return path
    
    def greedy_search(self, start: Tuple[int, int], end: Tuple[int, int], params: Dict) -> Optional[List[Tuple[int, int]]]:
        """贪心算法搜索路径"""
        current = start
        path = [current]
        visited = {current}
        
        while current != end:
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return None
            
            # 选择距离终点最近的邻居
            next_pos = min(neighbors, key=lambda pos: self.heuristic(pos, end))
            
            if next_pos in visited:  # 避免循环
                return None
            
            path.append(next_pos)
            visited.add(next_pos)
            current = next_pos
        
        return path
    
    def plan_path(self, prompt: str) -> Dict:
        """根据提示词规划路径"""
        # 解析提示词
        params = self.parse_prompt(prompt)
        
        # 设置网格
        self.setup_grid(params)
        
        # 选择算法
        algorithm = params['algorithm']
        start, end = params['start'], params['end']
        
        print(f"📝 解析提示词: {prompt}")
        print(f"  起点: {start}")
        print(f"  终点: {end}")
        print(f"  避开区域: {params['avoid_areas']}")
        print(f"  优先区域: {params['prefer_areas']}")
        print(f"  使用算法: {algorithm}")
        print(f"  优化目标: {params['optimization']}")
        
        # 执行路径搜索
        if algorithm == 'astar':
            path = self.astar_search(start, end, params)
        elif algorithm == 'dijkstra':
            path = self.dijkstra_search(start, end, params)
        elif algorithm == 'bfs':
            path = self.bfs_search(start, end, params)
        elif algorithm == 'greedy':
            path = self.greedy_search(start, end, params)
        else:
            path = self.astar_search(start, end, params)
        
        # 返回结果
        if path:
            distance = len(path) - 1
            return {
                'success': True,
                'path': path,
                'distance': distance,
                'algorithm': algorithm,
                'params': params
            }
        else:
            return {
                'success': False,
                'message': '无法找到可行路径',
                'params': params
            }
    
    def visualize_path(self, result: Dict):
        """可视化路径"""
        if not result['success']:
            print(f"❌ {result['message']}")
            return
        
        path = result['path']
        grid = [['□' for _ in range(self.width)] for _ in range(self.height)]
        
        # 标记障碍物
        for x, y in self.obstacles:
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = '■'
        
        # 标记优先区域
        for (x, y), weight in self.prefer_weights.items():
            if 0 <= x < self.width and 0 <= y < self.height and grid[y][x] == '□':
                grid[y][x] = '★'
        
        # 标记路径
        for i, (x, y) in enumerate(path):
            if i == 0:
                grid[y][x] = '🚩'  # 起点
            elif i == len(path) - 1:
                grid[y][x] = '🏁'  # 终点
            else:
                grid[y][x] = '●'
        
        # 打印网格
        print("\n🗺️  规划路径:")
        print('   ' + ' '.join([str(i).rjust(2) for i in range(self.width)]))
        for y in range(self.height):
            row = [str(y).rjust(2)]
            for x in range(self.width):
                row.append(grid[y][x].rjust(2))
            print(' '.join(row))
        
        print(f"\n📊 路径信息:")
        print(f"  总步数: {result['distance']}")
        print(f"  路径: {' → '.join([f'({x},{y})' for x, y in path])}")
        print(f"  算法: {result['algorithm']}")

# 使用示例
def main():
    planner = PromptBasedPathPlanner(grid_size=(8, 8))
    
    # 示例1：简单路径
    prompt1 = "从(0,0)出发到(7,7)，避开(3,3)和(4,4)"
    result1 = planner.plan_path(prompt1)
    planner.visualize_path(result1)
    
    print("\n" + "="*50 + "\n")
    
    # 示例2：带优先区域的路径
    prompt2 = "从(1,1)到(6,6)，优先经过(3,3)和(4,4)，使用A*算法，最安全路径"
    result2 = planner.plan_path(prompt2)
    planner.visualize_path(result2)
    
    print("\n" + "="*50 + "\n")
    
    # 示例3：不同算法对比
    prompts = [
        "从(0,0)到(7,7)，使用A*算法",
        "从(0,0)到(7,7)，使用贪心算法",
        "从(0,0)到(7,7)，使用BFS算法"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n📌 示例 {i}: {prompt}")
        result = planner.plan_path(prompt)
        planner.visualize_path(result)
        print("-"*30)

if __name__ == "__main__":
    main()