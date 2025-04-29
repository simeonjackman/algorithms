from gturtle import *
import random
import copy

makeTurtle()
hideTurtle()

# Konfiguration
colors = ["blue", "gray", "yellow"] # Farben für das Problem
max_containers = 3 # Maximale Container pro Farbe
slot_count = 3 # Minimale Anzahl Stellplätze
manual_try = True # Manueller Versuch

# Knotenklasse zur Speicherung von Position und Pfadkosten
class Node:
    def __init__(self, stacks, parent=None, g=0, h=0, f=0):
        self.stacks = stacks # die Stapel in diesem Zustand
        self.parent = parent # von welchem Knoten man gekommen ist
        self.g = g # Kosten vom Start bis zum Knoten
        self.h = 0 # Schätzung vom Knoten bis zum Ziel
        self.f = 0 # Bewertungsfunktion des Knoten (üblicherweise in Abhängigkeit von g und h)

def initialize_containers():
    slots = max(len(colors),slot_count) # Anzahl Stellplätze für Container
    containers = []
    for color in colors:
        count = random.randint(1, max_containers) # Container zufällig generieren
        containers.extend([color] * count)
    random.shuffle(containers) # Stapel mischen
    stacks = [containers[:len(containers)//2], containers[len(containers)//2:]] # Container aufteilen
    for i in range(slots-2):
        stacks.append([]) # Container auf Stellplätzen (Slots) aufstapeln
    return stacks

# Die Container auf den Stellplätzen zeichnen
def draw_stacks(stacks):
    clear()
    length = int(200 / len(stacks))
    setPenWidth(5)
    setFontSize(20)
    for i, stack in enumerate(stacks):
        setPenColor("black")
        penUp()
        moveTo(i * length, -210)
        penDown()
        right(90)
        forward(length-10)
        left(90)
        penUp()
        for j, c in enumerate(stack):
            setPenColor(c)
            penUp()
            moveTo(i * length, j * length - 200)
            penDown()
            drawRect(length)
        pu()
        moveTo(i * length + 5, -235)
        label(i)
 
# Einen Container zeichnen           
def drawRect(length):
    repeat(4):
        forward(length-10)
        right(90)

# Führt einen Zug aus
def move_container(stacks, src, dest):
    new_stacks = list(stacks) # Liste kopieren
    if legal_move(stacks, src, dest):
        container = new_stacks[src].pop()
        new_stacks[dest].append(container)
    return new_stacks

# Prüft, ob ein Zug möglich ist
def legal_move(stacks, src, dest):
    # Container an der gleichen Position abgelegt
    if src == dest: 
        return False
    # Falls Start oder Ziel ungültig
    if  src < 0 or src > len(stacks) - 1 or dest < 0 or dest > len(stacks) - 1:
        return False
    # Falls kein Container an dieser Position.
    if not stacks[src]: 
        return False
    return True
    
def legal_moves(stacks):
    moves = []
    for s in range(0,len(stacks)):
        for d in range(0,len(stacks)):
            if legal_move(stacks,s,d):
                moves.append((s,d))
    return moves
            
# Überprüft, ob auf jedem Stellplatz nur eine Farbe liegt
def is_sorted(stacks):
    for stack in stacks:
        if len(stack) > 0 and len(set(stack)) > 1:
            return False
    return True
    
def search(start_state):
    print("Beginne Suche...")
    counter = 0
    queue = [start_state]
    visited = set() # Welche Zustände wir bereits gesehen haben
    while queue:
        if counter % 1000 == 0:
            print(str(counter) + " Zustände durchsucht...")
        if counter > 5000:
            print("Suche aufgegeben...")
            break
        current = queue.pop() # hier wird ein neuer Zustand gewählt
        visited.add(repr(current.stacks))
        # Wir zählen wie viele Zustände wir durchsuchen haben
        counter = counter + 1 
        # Hier wird der Pfad zum Ziel rekursiv rekonstruiert wenn man am Ziel ist.
        if is_sorted(current.stacks):
            path = []
            while current:
                path.append(current.stacks)
                current = current.parent
            return path[::-1], counter
        moves = legal_moves(current.stacks)
        for move in moves:
            src, dest = move # Zug in Ursprung und Ziel aufteilen
            new_stacks = copy.deepcopy(current.stacks)
            new_stacks = move_container(new_stacks, src, dest)
            if(repr(new_stacks) in visited):
                continue
            # Hier können Sie eine Heuristik definieren
            heuristic_value = 0
            queue.append(Node(new_stacks,current,h=heuristic_value))
        # Mit dieser Funktion können Sie die Liste der noch nicht besuchten Knoten sortieren:
        # queue.sort(key=lambda n: n.h)
    return [], counter # Kein Pfad gefunden
            
stacks = list(initialize_containers()) # Wir initialisieren den Startzustand
start_state = Node(copy.deepcopy(stacks)) # Wir beginnen mit dem Startzustand
draw_stacks(stacks)
if manual_try:
    manual_count = 0
    while not is_sorted(stacks):
        manual_count = manual_count + 1
        print(repr(legal_moves(stacks)))
        src = int(input("Von welchem Platz soll ein Container bewegt werden?"))
        dest = int(input("Wohin soll er bewegt werden?"))
        stacks = move_container(stacks, src, dest)
        draw_stacks(stacks)
        delay(1000)
    print("Herzlichen Glückwunsch! Alle Container sind sortiert.")
    print("Ziel in " + str(manual_count) + " manuellen Schritten erreicht!")
draw_stacks(stacks)
path, counter = search(start_state)
if len(path) == 0:
    print("Keine Lösung gefunden...")
else:
    print("Ziel in " + str(len(path)-1) + " Schritten erreicht")
    print(str(counter) + " Zustände durchsucht")
    print("Weg zum Ziel:")
    for step in path:
        print(str(step))
        draw_stacks(step)
        delay(1000)