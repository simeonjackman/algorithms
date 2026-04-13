from gturtle import *
import random

makeTurtle()
hideTurtle()

# Spiel Konfiguration

# Legt die Breite des Spielfelds in Feldern fest.
width = 3
# Legt die Höhe des Spielfelds in Feldern fest.
height = 3
# Legt die grafische Grösse eines Felds in Pixeln fest.
grid_size = 60

# Speichert das Symbol für den menschlichen Spieler.
PLAYER = "A"
# Speichert das Symbol für den Computergegner.
COMPUTER = "B"
# Ordnet jedem Spieler seine Vorwärtsrichtung auf der y-Achse zu.
DIRECTION = {PLAYER: 1, COMPUTER: -1}
# Ordnet jedem Spieler sein Gegnersymbol zu.
OPPONENT = {PLAYER: COMPUTER, COMPUTER: PLAYER}

# Enthält alle Figurenpositionen als Mapping von Koordinate zu Spieler.
pieces = {(x, 0): PLAYER for x in range(width)}
pieces.update({(x, height - 1): COMPUTER for x in range(width)})


def in_bounds(x, y):
    # Prüft, ob eine Position innerhalb des Spielfelds liegt.
    return 0 <= x < width and 0 <= y < height


def apply_move(x1, y1, x2, y2, piece):
    # Führt einen Zug aus, indem die Figur von Start nach Ziel gesetzt wird.
    del pieces[(x1, y1)]
    pieces[(x2, y2)] = piece

# Spielfeld erstellen
def draw_grid():
    # Zeichnet alle Felder des Spielfelds als graue Punkte.
    penUp()
    setPenColor("gray")
    # Iteriert über alle x-Positionen des Brettes.
    for x in range(width):
        # Iteriert über alle y-Positionen des Brettes.
        for y in range(height):
            moveTo(x * grid_size, y * grid_size)
            dot(grid_size / 2)

# Koordinaten einzeichnen
def draw_coordinates():
    # Zeichnet die x- und y-Koordinaten um das Spielfeld herum.
    penUp()
    setFontSize(20)
    # Iteriert über alle x-Werte für die Beschriftung unten.
    for x in range(width):
        moveTo(x * grid_size - 20, -50)
        label("x=" + str(x))
    # Iteriert über alle y-Werte für die Beschriftung links.
    for y in range(height):
        moveTo(-70, grid_size * y - 5)
        label("y=" + str(y))

# Figuren auf das Brett zeichnen
def draw_pieces():
    # Zeichnet alle Figuren abhängig vom Besitzer in Weiss oder Schwarz.
    for (x, y), piece in pieces.items():
        moveTo(x * grid_size, y * grid_size)
        if piece == COMPUTER:
            setPenColor("black")
        else:
            setPenColor("white")
        dot(0.4 * grid_size)

# Prüft, welche Züge legal sind
def is_valid_move(piece, x1, y1, x2, y2):
    # Prüft, ob ein einzelner Zug für eine Figur regelkonform ist.
    if piece not in DIRECTION or not in_bounds(x2, y2):
        return False

    if y2 != y1 + DIRECTION[piece] or abs(x2 - x1) > 1:
        return False

    # Liest die Figur auf dem Zielfeld oder None, falls das Feld leer ist.
    target = pieces.get((x2, y2))
    if x2 == x1:
        return target is None
    return target == OPPONENT[piece]

def possible_moves(player, selected_piece=None):
    # Sammelt alle gefundenen legalen Züge als Tupel.
    available_moves = []
    # Entpackt jede Figur des Brettes in Koordinate und Besitzer.
    for (x1, y1), piece in pieces.items():
        if piece == player:
            if selected_piece and (x1, y1) != selected_piece:
                continue
            # Definiert den horizontalen Schritt nach links, geradeaus und rechts.
            for dx in (-1, 0, 1):
                # Berechnet die Ziel-x-Koordinate für den aktuellen Versatz.
                x2 = x1 + dx
                # Berechnet die Ziel-y-Koordinate anhand der Laufrichtung.
                y2 = y1 + DIRECTION[player]
                if is_valid_move(player, x1, y1, x2, y2):
                    available_moves.append((x1, y1, x2, y2))
    return available_moves

# Berechnet, welche Figuren der Spieler Bewegen kann
def possible_pieces(player):
    # Gibt alle Positionen der Figuren eines Spielers zurück.
    return [(x1, y1) for (x1, y1), piece in pieces.items() if piece == player]

# Wählt den Zug für den Gegner zufällig
def computer_move():
    # Enthält alle legalen Züge, aus denen der Computer wählen kann.
    available_moves = possible_moves(COMPUTER)
    if available_moves:
        # Entpackt den zufällig gewählten Zug in Start- und Zielkoordinaten.
        x1, y1, x2, y2 = random.choice(available_moves)
        apply_move(x1, y1, x2, y2, COMPUTER)

# Prüft, ob ein Spieler gewonnen hat
def check_winner():
    # Prüft, ob Spieler oder Computer die gegnerische Grundreihe erreicht hat.
    if any(y == height - 1 for (x, y), piece in pieces.items() if piece == PLAYER):
        print("Spieler gewinnt!")
        return True
    if any(y == 0 for (x, y), piece in pieces.items() if piece == COMPUTER):
        print("Computer gewinnt!")
        return True
    return False
    
def print_moves(player):
    # Speichert die aktuell berechneten Züge für die Ausgabe.
    moves = possible_moves(player)
    print("Mögliche Züge:")
    # Entpackt jeden Zug für die formatierte Ausgabe in der Konsole.
    for (x1, y1, x2, y2) in moves:
        print("Von x=" + str(x1) + " y=" + str(y1) + " nach x=" + str(x2) + " y=" + str(y2))


def draw_board():
    # Zeichnet das Brett und danach die Figuren im aktuellen Zustand.
    draw_grid()
    draw_pieces()

# Wählt den Zug des Spielers, hier müssen Sie Anpassungen vornehmen
def player_move():
    # Fragt wiederholt eine gültige Spieler-Eingabe ab und führt den Zug aus.
    while True:
        try:
            # Enthält alle auswählbaren Figuren des Spielers.
            own_pieces = possible_pieces(PLAYER)
            # Speichert die eingegebene x-Startkoordinate der Figur.
            x1 = int(input("x-Koordinate deiner Figur: " + str(own_pieces)))
            # Speichert die eingegebene y-Startkoordinate der Figur.
            y1 = int(input("y-Koordinate deiner Figur: " + str(own_pieces)))

            # Enthält alle legalen Zielzüge der ausgewählten Figur.
            own_moves = possible_moves(PLAYER, (x1, y1))
            # Speichert die eingegebene x-Zielkoordinate.
            x2 = int(input("x-Zielkoordinate: " + str(own_moves)))
            # Speichert die eingegebene y-Zielkoordinate.
            y2 = int(input("y-Zielkoordinate: " + str(own_moves)))
        except ValueError:
            print("Geben Sie etwas ein")
            continue

        if (x1, y1, x2, y2) in possible_moves(PLAYER, (x1, y1)):
            apply_move(x1, y1, x2, y2, PLAYER)
            break

        print("Ungültiger Zug. Versuch es erneut.")
        delay(1000)

# Startzustand zeichnen
draw_coordinates()
draw_board()
print("Startzustand: " + str(pieces))

# Spiel ausführen bis es einen Sieger gibt
while True:
    print_moves(PLAYER)
    player_move()
    draw_board()
    # Prüfen, ob jemand gewonnen hat
    if check_winner():
        break
    delay(1000)
    computer_move()
    draw_board()
    if check_winner():
        break