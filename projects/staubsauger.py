import random
import copy
from gturtle import *

# Turtle zum Zeichnen verstecken
makeTurtle()
hideTurtle()

# Konfiguration

# Raumgrösse (rows mal cols)
rows, cols = 4, 4 # Hier kann der Raum grösser gemacht werden
dirt_count = 3 # Wieviel dreck rumliegt
enable_obstacles = False # Ob es auch "Möbel" im Zimmer haben sollte (auf True setzen)

# Knotenklasse zur Speicherung von Position und Pfadkosten
class Node:
    def __init__(self, x, y, parent=None, g=0, h=0, d={}):
        self.x, self.y = x, y # x und y Position des Zustands
        self.parent = parent # von welchem Knoten man gekommen ist
        self.d = d # Welcher dreck gesammelt wurde
        self.g = g # Kosten vom Start bis zum Knoten
        self.h = h # Schätzung vom Knoten bis zum Ziel

# Funktion für um zufälligen Dreck zu erzeugen
def generate_dirt():
    dirt = set()
    while len(dirt) < dirt_count:
        x, y = random.randint(0, cols-1), random.randint(0, cols-1)
        if (x, y) not in [(0, 0), (cols - 1, rows - 1)]:
            dirt.add((x, y))
    return dirt
    
dirt = generate_dirt() # hier werden die Hindernisse generiert

# Startposition festlegen
start = Node(0, 0, d=dirt)
    
# Funktion für um zufällige Hindernisse zu erzeugen (extra)
obstacles = set()
def generate_obstacles():
    while len(obstacles) < (rows*cols)/4:
        x, y = random.randint(0, cols), random.randint(0, cols)
        if (x, y) not in [(0, 0), (cols - 1, rows - 1),dirt]:
            obstacles.add((x, y))
    return obstacles

# Möbel nur generieren, falls Option eingeschaltet ist
if enable_obstacles:
    obstacles = generate_obstacles() # hier werden die Hindernisse generiert (extra)

# Zeichne das Schachbrett in jedem Schritt (extra)
def draw_board(current=None, offset=0, path=[]):
    cell_size = int(180/cols)
    for y in range(rows):
        for x in range(cols):
            setPos(-100 + (cols + 1) * cell_size * offset + x * cell_size, -100 + y * cell_size)
            if (x, y) == (0, 0):
                setFillColor("green")
            elif (x, y) in path:
                setFillColor("blue")
            elif (x, y) in obstacles:
                setFillColor("black")
            elif (x, y) in dirt:
                setFillColor("brown")
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

# Hier können Sie eine Heuristik definieren
def heuristic(x,y,dirt):
    heuristic_value = 0
    return heuristic_value

# Ihre Suche
def search(start):
    print("Beginne Suche...")
    counter = 0
    queue = [start] # Wir beginnen mit dem Startzustand A1 (0,0)
    visited = set() # Welche Zustände wir bereits gesehen haben
    while queue:
        current = queue.pop() # hier wird das Element von der Schlange genommen
        counter = counter + 1 # Wir zählen wie viele Zustände wir durchsuchen
        visited.add((current.x, current.y)) # Wenn wir einen Zustand untersuchen, fügen wir ihn zu visited hinzu
        draw_board(current,0)
        # Wir haben eine Lösung gefunden, wenn wir keinen Deck mehr haben
        if len(current.d) == 0:
            # Hier wird der Pfad zum Ziel rekursiv rekonstruiert wenn alles sauber ist.
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1], counter

        # Hier werden neue Zustände der Warteschlange hinzugefügt
        for dx, dy in [(-1, 0), (-1,-1), (-1,1), (1, 0), (1,1), (1,-1), (0, -1), (0, 1)]:
            x, y = current.x + dx, current.y + dy
            # Hier wird überprüft, ob der neue Zustand in die Warteschlange kommt
            if x < 0 or x >= cols or y < 0 or y >= rows:
                # Zustand ist nicht auf dem Spielbrett
                continue
            # Hier können Sie eine Heuristik definieren
            heuristic_value = 0
            if (x, y) in visited:
                continue
            if (x, y) in obstacles:
                # Zustand ist ein Hindernis
                continue
            if (x, y) in current.d:
                # Zustand ist Dreck, wir haben also ein Dreck gesaugt
                # Der Dreck wird entfernt
                updated_dirt = copy.deepcopy(current.d)
                updated_dirt.remove((x,y))
                # Neuer Zustand mit einem Dreck weniger
                queue.append(Node(x, y, current, g=current.g + 1, h=heuristic(x,y,updated_dirt), d=updated_dirt))
                continue
            else: 
                # Neuer Zustand mit gleich viel Dreck
                queue.append(Node(x, y, current, g=current.g + 1, h=heuristic(x,y,current.d), d=current.d))
        # Mit dieser Funktion können Sie die Liste der noch nicht besuchten Knoten sortieren:
        # queue.sort(key=lambda n: n.h)
    return [], counter


print("Lösung von Ihrem Suchalgorithmus:")
path, counter = search(start)
print(str(counter) + " Zustände durchsucht")
if len(path) == 0:
    print("Keine Lösung gefunden...")
else:    
    draw_board(None,-1) # Ursprungssituation zeichnen
    draw_board(None,0,path) # Lösung zeichnen
    print(path)
    print("Ziel in " + str(len(path) - 1) + " Schritten erreicht")