from gturtle import *
import random
import copy

makeTurtle()
hideTurtle()

# Konfiguration
colors = ["black","red"] # Farben für das Spiel
max_cards = 3 # Anzahl Karten pro Farbe
slot_count = 4 # Minimale Anzahl Plätze
manual_try = True # Manueller Versuch

# Knotenklasse zur Speicherung von Position und Pfadkosten
class Node:
    def __init__(self, stacks, parent=None, g=0, h=0, f=0):
        self.stacks = stacks # die Stapel in diesem Zustand
        self.parent = parent # von welchem Knoten man gekommen ist
        self.g = g # Kosten vom Start bis zum Knoten
        self.h = 0 # Schätzung vom Knoten bis zum Ziel
        self.f = 0 # Bewertungsfunktion des Knoten (üblicherweise in Abhängigkeit von g und h)

def initialize_cards():
    slots = max(len(colors),slot_count) # Anzahl Plätze für Karten
    cards = []
    for color in colors:
        for i in range(max_cards):
            cards.append((color,i))
    random.shuffle(cards) # Stapel mischen
    stacks = [cards[:len(cards)//2], cards[len(cards)//2:]] # Karten aufteilen
    for i in range(slots-2):
        stacks.append([]) # Karten auf Plätzen (Slots) aufstapeln
    return stacks

# Die Karten auf den Plätzen zeichnen
def draw_stacks(stacks):
    clear()
    length = int(180 / len(stacks))
    setPenWidth(5)
    for i, stack in enumerate(stacks):
        setPenColor("black")
        penUp()
        moveTo(i * length, -210)
        penDown()
        right(90)
        forward(length-10)
        left(90)
        penUp()
        for j, (card_color,card_value) in enumerate(stack):
            drawCard(i * length, j * length - 200, card_value, card_color, length)
        pu()
        moveTo(i * length + 5, -235)
        setFontSize(20)
        label(i)
 
# Eine Karten zeichnen           
def drawCard(x, y, value, color, length):
    moveTo(x + length/2 - 13, y + length / 2 - 15)
    setPenColor(color)
    setFontSize(30)
    label(value)
    pu()
    moveTo(x, y)
    forward((length-10)/4)
    pd()
    repeat(4):
        forward((length-10)/2)
        rightArc((length-10)/4,90)
    pu()

# Führt einen Zug aus
def move_card(stacks, src, dest):
    new_stacks = list(stacks) # Liste kopieren
    if legal_move(stacks, src, dest):
        card = new_stacks[src].pop()
        new_stacks[dest].append(card)
    return new_stacks

# Prüft, ob ein Zug möglich ist
def legal_move(stacks, src, dest):
    # Karte an der gleichen Position abgelegt
    if src == dest: 
        return False
    # Falls Start oder Ziel ungültig
    if  src < 0 or src > len(stacks) - 1 or dest < 0 or dest > len(stacks) - 1:
        return False
    # Falls keine Karte an dieser Position.
    if not stacks[src]: 
        return False
    # Falls eine Karte auf dem Zielstapel, müssen wir den Zug genauer prüfen
    if stacks[dest]:
        # Farbe muss gleich sein
        if not stacks[src][-1][0] == stacks[dest][-1][0]:
            return False
        # Zahl im Ziel muss grösser sein
        if stacks[src][-1][1] > stacks[dest][-1][1]:
            return False
    return True
    
def legal_moves(stacks):
    moves = []
    for s in range(0,len(stacks)):
        for d in range(0,len(stacks)):
            if legal_move(stacks,s,d):
                moves.append((s,d))
    return moves
            
# Überprüft, ob auf jedem Platz nur eine Farbe liegt
def is_sorted(stacks):
    for stack in stacks:
        # Leere Stapel werden übersprungen
        if len(stack) == 0:
            continue
        stack_color = stack[0][0]
        for i,card in enumerate(stack):
            # Der ganze Stapel muss die gleiche Farbe haben
            if card[0] != stack_color:
                return False
            # Die Kartenwerte müssen nach oben kleiner werden
            if card[1] != max_cards - i - 1:
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
        if counter > 4000:
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
            new_stacks = move_card(new_stacks, src, dest)
            if(repr(new_stacks) in visited):
                continue
            # Hier können Sie eine Heuristik definieren
            heuristic_value = 0
            queue.append(Node(new_stacks,current,h=heuristic_value))
        # Mit dieser Funktion können Sie die Liste der noch nicht besuchten Knoten sortieren:
        # queue.sort(key=lambda n: n.h)
    return [], counter # Kein Pfad gefunden
            
stacks = list(initialize_cards()) # Wir initialisieren den Startzustand
start_state = Node(copy.deepcopy(stacks)) # Wir beginnen mit dem Startzustand
if manual_try:
    draw_stacks(stacks)
    manual_count = 0
    while not is_sorted(stacks):
        manual_count = manual_count + 1
        print(repr(legal_moves(stacks)))
        src = int(input("Von welchem Platz soll eine Karte genommen werden?"))
        dest = int(input("Wohin soll Sie gelegt werden?"))
        stacks = move_card(stacks, src, dest)
        draw_stacks(stacks)
        delay(1000)
    print("Herzlichen Glückwunsch! Alle Karten sind sortiert.")
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