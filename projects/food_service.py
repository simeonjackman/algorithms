import random
import copy
from gturtle import *

# Turtle zum Zeichnen verstecken
makeTurtle()
hideTurtle()

# Konfiguration

# Kartengrösse (rows mal cols)
rows, cols = 5, 5 # Hier kann der Raum grösser gemacht werden
order_count = 3 # Wieviel essen geliefert werden muss

# Knotenklasse zur Speicherung von Position und Pfadkosten
class Node:
    def __init__(self, x, y, parent=None, g=0, h=0, f=0, o={}):
        self.x, self.y = x, y # x und y Position des Zustands
        self.parent = parent # von welchem Knoten man gekommen ist
        self.o = o # Welche Bestellungen bereits geliefert wurden
        self.g = g # Kosten vom Start bis zum Knoten
        self.h = h # Schätzung vom Knoten bis zum Ziel
        self.f = f # Bewertungsfunktion des Knoten (üblicherweise in Abhängigkeit von g und h)

# Funktion um zufällige Bestellungen zu erzeugen
def generate_orders():
    orders = set()
    while len(orders) < order_count:
        x, y = random.randint(0, cols-1), random.randint(0, rows-1)
        if (x, y) not in [(0, 0), (cols - 1, rows - 1)]:
            orders.add((x, y))
    return orders

orders = generate_orders()
    
# Startposition festlegen, es ist noch keine Bestellung erfüllt
start = Node(0, 0,o=copy.deepcopy(orders))

# Zeichnet das Spielbrett
def draw_board(current=None, offset=0, path=[]):
    cell_size = int(180/cols)
    for y in range(rows):
        for x in range(cols):
            setPos(-100 + (cols + 1) * cell_size * offset + x * cell_size, -100 + y * cell_size)
            if (x, y) == (0, 0):
                setFillColor("green")
            elif (x, y) in path:
                setFillColor("blue")
            elif (x, y) in orders:
                setFillColor("cyan")
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
        # Wir haben eine Lösung gefunden, wenn wir keine Lieferung mehr machen müssen
        if len(current.o) == 0:
            # Hier wird der Pfad zum Ziel rekursiv rekonstruiert wenn alle Lieferungen gemacht wurden ist.
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
            # Feld wurde bereits besucht
            if (x, y) in visited:
                continue
            if (x, y) in current.o:
                # Zustand ist Lieferstandort, wir haben also ein eine Lieferung gemacht
                # Die gemachte Lieferung wird aus der noch zu machenden Lieferung entfernt
                updated_orders = copy.deepcopy(current.o)
                updated_orders.remove((x,y))
                queue.append(Node(x, y, current, g=current.g + 1, h=heuristic_value, o=updated_orders))
                continue
            else: 
                queue.append(Node(x, y, current, g=current.g + 1, h=heuristic_value, o=current.o))
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


