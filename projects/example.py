import random
from gturtle import *

# Knotenklasse zur Speicherung von Position und Pfadkosten
class Node:
    def __init__(self, x, y, parent=None):
        self.x, self.y = x, y
        self.parent = parent
        self.g = self.h = self.f = 0

# Schachbrettgrösse (rowsxcols)
rows, cols = 4, 4

# Start- und Endposition festlegen
start = Node(0, 0)
end = Node(cols - 1,rows - 1)

# Zufällige Hindernisse erzeugen
def generate_obstacles():
    obstacles = set()
    while len(obstacles) < (rows*cols)/4:
        x, y = random.randint(0, cols), random.randint(0, cols)
        if (x, y) not in [(0, 0), (cols - 1, rows - 1)]:
            obstacles.add((x, y))
    return obstacles

obstacles = generate_obstacles()

# Manhattan-Distanz als Heuristik
def heuristic(node, end):
    return abs(node.x - end.x) + abs(node.y - end.y)

# Zeichne das Schachbrett in jedem Schritt
def draw_board(current=None, offset=0, path=[]):
    cell_size = int(360/cols)
    for y in range(rows):
        for x in range(cols):
            setPos(-100 + 400 * offset + x * cell_size, -100 + y * cell_size)
            if (x, y) == (0, 0):
                setFillColor("green")
            elif (x, y) == (end.x ,end.y):
                setFillColor("red")
            elif (x, y) in path:
                setFillColor("blue")
            elif (x, y) in obstacles:
                setFillColor("black")
            elif current and (x, y) == (current.x, current.y):
                setFillColor("yellow")
            else:
                setFillColor("white")
            startPath()
            repeat 4:
                forward(cell_size)
                right(90)
            fillPath()
    delay(100)

# Breitensuche
def breadth_first_search(start, end):
    queue = [start]
    visited = set()
    while queue:
        current = queue.pop(0)
        visited.add((current.x, current.y))
        draw_board(current,-1)

        if (current.x, current.y) == (end.x, end.y):
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        for dx, dy in [(-1, 0), (-1,-1), (-1,1), (1, 0), (1,1), (1,-1), (0, -1), (0, 1)]:
            x, y = current.x + dx, current.y + dy
            if 0 <= x < cols and 0 <= y < rows and (x, y) not in obstacles and (x, y) not in visited:
                queue.append(Node(x, y, current))
    return None

# Tiefensuche
def depth_first_search(start, end):
    stack = [start]
    visited = set()
    while stack:
        current = stack.pop()
        visited.add((current.x, current.y))
        draw_board(current,0)

        if (current.x, current.y) == (end.x, end.y):
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        for dx, dy in [(-1, 0), (-1,-1), (-1,1), (1, 0), (1,1), (1,-1), (0, -1), (0, 1)]:
            x, y = current.x + dx, current.y + dy
            if 0 <= x < cols and 0 <= y < rows and (x, y) not in obstacles and (x, y) not in visited:
                stack.append(Node(x, y, current))
    return None

# A*-Algorithmus
def astar(start, end):
    open_list = [start]
    closed_list = set()

    while open_list:
        open_list.sort(key=lambda n: n.f)
        current = open_list.pop(0)
        closed_list.add((current.x, current.y))
        draw_board(current,1)

        if (current.x, current.y) == (end.x, end.y):
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        for dx, dy in [(-1, 0), (-1,-1), (-1,1), (1, 0), (1,1), (1,-1), (0, -1), (0, 1)]:
            x, y = current.x + dx, current.y + dy
            if 0 <= x < cols and 0 <= y < rows and (x, y) not in obstacles and (x, y) not in closed_list:
                neighbor = Node(x, y, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                open_list.append(neighbor)
    return None

# Algorithmen testen
makeTurtle()
hideTurtle()

print("Breitensuche:")
path = breadth_first_search(start, end)
draw_board(None,-1,path)
print(path)

print("Tiefensuche:")
path = depth_first_search(start, end)
draw_board(None,0,path)
print(path)

print("A*-Algorithmus:")
path = astar(start, end)
draw_board(None,1,path)
print(path)

