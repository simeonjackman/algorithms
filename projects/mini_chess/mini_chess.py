from gturtle import *
import random

makeTurtle()
hideTurtle()

# Spiel Konfiguration

width = 3 # Breite des Spielfeldes
height = 3 # Höhe des Spielfeldes
grid_size = 60 # Wie gross das Brett gezeichnet werden sollte

pieces = {}
for x in range(width):
    # "A" ist der Spieler (Weiss)
    pieces[(x,0)] = "A"
    # "B" ist der Computer (Schwarz)
    pieces[(x,height-1)] = "B"

# Spielfeld erstellen
def draw_grid():
    penUp()
    setPenColor("gray")
    for x in range(0, width):
        for y in range(0, height):
            moveTo(x * grid_size, y * grid_size)
            dot(grid_size/2)

# Koordinaten einzeichnen
def draw_coordinates():
    penUp()
    setFontSize(20)
    for x in range(0, width):
        moveTo(x * grid_size - 20, -50)
        label("x="+str(x))
    for y in range(0, height):
        moveTo(-70, grid_size*y-5)
        label("y="+str(y))

# Figuren auf das Brett zeichnen
def draw_pieces():
    for (x, y), piece in pieces.items():
        moveTo(x * grid_size, y * grid_size)
        if piece == "B":
            setPenColor("black")
        else:
            setPenColor("white")
        dot(0.4*grid_size)

# Prüft, welche Züge legal sind
def is_valid_move(piece, x1, y1, x2, y2):
    if piece == "A":
        return (y2 == y1 + 1 and x2 == x1) and (x2, y2) not in pieces or (y2 == y1 + 1 and abs(x2 - x1) == 1 and (x2, y2) in pieces and pieces[(x2, y2)] == "B")
    if piece == "B":
        return (y2 == y1 - 1 and x2 == x1) and (x2, y2) not in pieces or (y2 == y1 - 1 and abs(x2 - x1) == 1 and (x2, y2) in pieces and pieces[(x2, y2)] == "A")
    return False

def possible_moves(player, selected_piece=None):
    available_moves = []
    for (x1, y1), piece in pieces.items():
        if piece == player:
            if  selected_piece and (x1 != selected_piece[0] or y1 != selected_piece[1]):
                continue
            for dx in [-1, 0, 1]:
                if player == "A":
                    x2, y2 = x1 + dx, y1 + 1
                else:
                    x2, y2 = x1 + dx, y1 - 1
                if is_valid_move(player, x1, y1, x2, y2):
                    available_moves.append((x1, y1, x2, y2))
    return available_moves

# Berechnet, welche Figuren der Spieler Bewegen kann
def possible_pieces(player):
    available_pieces = []
    for (x1, y1), piece in pieces.items():
        if piece == player:
            available_pieces.append((x1,y1))
    return available_pieces

# Wählt den Zug für den Gegner zufällig
def computer_move():
    available_moves = possible_moves("B")
    if available_moves:
        x1, y1, x2, y2 = random.choice(available_moves)
        del pieces[(x1, y1)]
        pieces[(x2, y2)] = "B"

# Prüft, ob ein Spieler gewonnen hat
def check_winner():
    if any(y == height-1 for (x, y), piece in pieces.items() if piece == "A"):
        print("Spieler gewinnt!")
        return True
    if any(y == 0 for (x, y), piece in pieces.items() if piece == "B"):
        print("Computer gewinnt!")
        return True
    return False
    
def print_moves(player):
    moves = possible_moves(player)
    print("Mögliche Züge:")
    for (x1,y1,x2,y2) in moves:
        print("Von x=" + str(x1) +  " y=" + str(y1) + " nach x=" + str(x2) + " y=" + str(y2))

# Wählt den Zug des Spielers, hier müssen Sie Anpassungen vornehmen
def player_move():
    while True:
        # Fragen, welche Figur gespielt werden soll
        try:
            # Welche Figur?
            x1, y1 = int(input("x-Koordinate deiner Figur: " + str(possible_pieces("A")))), int(input("y-Koordinate deiner Figur: "+ str(possible_pieces("A"))))
            # Wohin soll Sie gespielt werden?
            x2, y2 = int(input("x-Zielkoordinate: " + str(possible_moves("A",(x1,y1))))), int(input("y-Zielkoordinate: " + str(possible_moves("A",(x1,y1)))))
        except ValueError:
            print("Geben Sie etwas ein")
            continue
        # Prüfen, ob der Zug legal ist
        if (x1, y1) in pieces and pieces[(x1, y1)] == "A" and is_valid_move("A", x1, y1, x2, y2):
            # Zug ausführen
            del pieces[(x1, y1)]
            pieces[(x2, y2)] = "A"
            break
        else:
            # Falls Zug ungültig
            print("Ungültiger Zug. Versuch es erneut.")
            delay(1000)

# Startzustand zeichnen
draw_coordinates()
draw_grid()
draw_pieces()
print("Startzustand: " + str(pieces))

# Spiel ausführen bis es einen Sieger gibt
while True:
    print_moves("A")
    player_move()
    draw_grid()
    draw_pieces()
    # Prüfen, ob jemand gewonnen hat
    if check_winner():
        break
    delay(1000)
    computer_move()
    draw_grid()
    draw_pieces()
    if check_winner():
        break