import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parchís")

# Colores y fuentes
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
font = pygame.font.Font(None, 36)

# Tamaño de las celdas
cell_size = 40

def draw_board(screen):
    for row in range(15):
        for col in range(15):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, (200, 200, 200), (x, y, cell_size, cell_size), 1)
            # Dibujar propiedades especiales (ej: salidas)
            if Tablero[row][col]["tipo"] == "salida":
                pygame.draw.circle(screen, (255, 255, 0), (x + cell_size//2, y + cell_size//2), 10)

def draw_pieces(screen):
    for ficha in Fichas:
        row, col = ficha["pos"]
        x = col * cell_size + cell_size // 2
        y = row * cell_size + cell_size // 2
        color = {
            "Rojo": RED,
            "Verde": GREEN,
            "Azul": BLUE,
            "Naranja": ORANGE
        }[ficha["color"]]
        pygame.draw.circle(screen, color, (x, y), cell_size // 3)

def Dados(Color, Modo):
    if Modo == 1:
        input("Presione enter para lanzar los dados...")
        Dado_1 = random.randint(1, 6)
        Dado_2 = random.randint(1, 6)
        print("El resultado de los dados es: ", Dado_1, Dado_2)
    elif Modo == 2:
        Dado_1 = int(input("Ingrese el valor del primer dado: "))
        Dado_2 = int(input("Ingrese el valor del segundo dado: "))

    Fcarcel = []
    for i in Fichas:
        if Color in i:
            Fcarcel.append(i)

    if (Dado_1 == 5 or Dado_2 == 5 or Dado_1 + Dado_2 == 5) and len(Fcarcel) != 0:
        Regla_1 = [True, Fcarcel]
        if Dado_1 == 5 and Dado_2 == 5:
            Regla_1.append(2)
        elif Dado_2 == 5:
            Regla_1.append(1)
        elif Dado_1 == 5:
            Regla_1.append(0)
        else:
            Regla_1.append(3)
    else:
        Regla_1 = [False, Fcarcel, 4]

    return [Dado_1, Dado_2, Regla_1, Color]

def bloq():
    Bloqueos = []
    for n in Tablero:
        if len(n[2]) != 0 and len(n[3]) != 0:
            Bloqueos.append(Tablero.index(n))
    return Bloqueos

def C_vacia(Casilla):
    if len(Tablero[Casilla][2]) == 0 and len(Tablero[Casilla][3]) == 0:
        return 2
    elif len(Tablero[Casilla][2]) == 0:
        return 2
    else:
        return 3

def mov_f(Turno, Dobles, UF):
    if Dobles == 3:
        for i in Tablero:
            if UF in i:
                Fichas.append(i.pop(i.index(UF)))
                print("Sacaste 3 pares seguidos, la ultima ficha que moviste va a la carcel")
                i.append([])
                return []
    F = 0
    for i in Fichas:
        if Turno[-1] in i:
            F += 1
            if F == 4:
                print(f"Todas las fichas del color {Turno[-1]}, están en la carcel")
                return []
    if len(Turno) <= 2:
        return []
    if Turno[0] == 0 and Turno[1] == 0:
        print("No hay movimientos disponibles")
        return []
    T = True
    while T:
        Num = 3
        if len(Turno) == 4:
            while Num not in (0, 1):
                Num = int(input(f"¿Qué resultado del dado quiere utilizar?¿{Turno[0]} (Escribe 0) o {Turno[1]} (Escribe 1)?"))
            dado = Turno.pop(Num)
        elif len(Turno) == 3:
            dado = Turno.pop(0)
        elif len(Turno) == 2:
            return DicF[f"Ficha {F} {Turno[-1]}"]

        F = int(input(f"¿Qué ficha desea mover {dado} pasos? (1, 2, 3 o 4)"))
        while F not in (1, 2, 3, 4) or (DicF[f"Ficha {F} {Turno[-1]}"] in Fichas):
            F = int(input(f"La Ficha {F} no está en el tablero o no existe. Ingrese otro número"))
        Ficha = DicF[f"Ficha {F} {Turno[-1]}"]

        for i in Tablero:
            if Ficha in i:
                C0Ficha = Tablero.index(i)
                CFFicha = Tablero.index(i) + dado
                PRestantes = dado
                for n in range(C0Ficha, (CFFicha)):
                    if n + 1 not in bloq():
                        if Tablero[n][Tablero[n].index(Ficha)] == (17 * (Colores.index(Color))):
                            Tablero[n][0][0] = Tablero.pop(Tablero[n][Tablero[n].index(Ficha)])
                            Tablero[n].append([])
                            for a in range(1, PRestantes):
                                Tablero[n][0].insert(Tablero[n][0].index(Ficha), [])
                                Tablero[n][0][a] = Tablero[n].pop(Tablero[n][0].index(Ficha))
                            break
                        else:
                            if n == 67:
                                b = n
                                n = 0
                                Tablero[n][C_vacia(n)] = Tablero[b].pop(Tablero[b].index(Ficha))
                                Tablero[b].append([])
                            elif n > 67:
                                n -= 67
                                Tablero[n + 1][C_vacia(n + 1)] = Tablero[n].pop(Tablero[n].index(Ficha))
                                Tablero[n].append([])
                            else:
                                Tablero[n + 1][C_vacia(n + 1)] = Tablero[n].pop(Tablero[n].index(Ficha))
                                Tablero[n].append([])
                            PRestantes -= 1
                    else:
                        print(f"Hay un bloqueo en la casilla {Tablero.index(i)}")
                        T = False
                        break
                print(f"La ficha {Ficha} ha avanzado {dado} pasos")
                Cap_Fichas(Ficha, CFFicha)
                break
            else:
                for n in Tablero[17 * (Colores.index(Color))][0]:
                    if Ficha in n:
                        C0Ficha = Tablero[17 * (Colores.index(Color))][0].index(n)
                        CFFicha = C0Ficha + dado
                        if CFFicha <= 7:
                            Tablero[17 * (Colores.index(Color))][0][CFFicha] = Tablero[17 * (Colores.index(Color))][0].pop(C0Ficha)
                            Tablero[17 * (Colores.index(Color))][0].insert(C0Ficha, [])
                            if CFFicha == 7:
                                print(f"La ficha {Ficha} ha coronado!")
                                mov_f([10, 0, False, Color])
                        elif CFFicha > 7:
                            print("Para coronar, necesita tener el número exacto de pasos")
                            Turno.insert(0, dado)

def Cap_Fichas(Ficha, c, s=False):
    for x in range(3, 5):
        if s == True:
            if Ficha[0] != Tablero[c][x][0]:
                FichaF = Tablero[c][x]
                Fichas.append(Tablero[c].pop([x]))
                print(f"La ficha {Ficha} ha capturado a la ficha {FichaF}")
                mov_f([20, 0, False, Color])
        else:
            if type(Tablero[c][0]) != int and c in bloq() and Ficha[0] != Tablero[c][x][0]:
                FichaF = Tablero[c][x]
                Fichas.append(Tablero[c].pop([x]))
                print(f"La ficha {Ficha} ha capturado a la ficha {FichaF}")
                mov_f([20, 0, False, Color])
    return

def SFCarcel(n, Turno):
    if n == 0:
        print("Debe sacar una ficha de la carcel")
        for i in range(6, 68, 17):
            if Tablero[i][-3] == Turno[-1]:
                if i in bloq():
                    if Tablero[i][2][0] != Turno[-1] and Tablero[i][3][0] != Turno[-1]:
                        Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                    else:
                        break
                if (len(Tablero[i][2]) > 0 and Tablero[i][2][0] != Turno[-1]) or (len(Tablero[i][3]) > 0 and Tablero[i][3][0] != Turno[-1]):
                    Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                Tablero[i][C_vacia(i)] = Fichas.pop(Fichas.index(Turno[-2][1][0]))
                print(f"La ficha {Turno[-2][1][0]} ha salido de la carcel")
                Turno[0] = 0

    elif n == 1:
        print("Debe sacar una ficha de la carcel")
        for i in range(6, 68, 17):
            if Tablero[i][-3] == Turno[-1]:
                if i in bloq():
                    if Tablero[i][2][0] != Turno[-1] and Tablero[i][3][0] != Turno[-1]:
                        Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                    else:
                        break
                if (len(Tablero[i][2]) > 0 and Tablero[i][2][0] != Turno[-1]) or (len(Tablero[i][3]) > 0 and Tablero[i][3][0] != Turno[-1]):
                    Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                Tablero[i][C_vacia(i)] = Fichas.pop(Fichas.index(Turno[-2][1][0]))
                print(f"La ficha {Turno[-2][1][0]} ha salido de la carcel")
                Turno[1] = 0

    elif n == 2:
        print("Puede sacar dos fichas de la carcel (Debe sacar por lo menos 1)")
        for i in range(6, 68, 17):
            if Tablero[i][-3] == Turno[-1]:
                for n in range(2):
                    if i in bloq():
                        if Tablero[i][2][0] != Turno[-1] and Tablero[i][3][0] != Turno[-1]:
                            Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                        else:
                            break
                    if (len(Tablero[i][2]) > 0 and Tablero[i][2][0] != Turno[-1]) or (len(Tablero[i][3]) > 0 and Tablero[i][3][0] != Turno[-1]):
                        Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                    Tablero[i][C_vacia(i)] = Fichas.pop(Fichas.index(Turno[-2][1][n]))
                    print(f"La ficha {Turno[-2][1][n]} ha salido de la carcel")
                    Turno[0] = 0
                    Turno[1] = 0

    elif n == 3:
        print("Debe sacar una ficha de la carcel")
        for i in range(6, 68, 17):
            if Tablero[i][-3] == Turno[-1]:
                if i in bloq():
                    if Tablero[i][2][0] != Turno[-1] and Tablero[i][3][0] != Turno[-1]:
                        Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                    else:
                        break
                if (len(Tablero[i][2]) > 0 and Tablero[i][2][0] != Turno[-1]) or (len(Tablero[i][3]) > 0 and Tablero[i][3][0] != Turno[-1]):
                    Cap_Fichas(Fichas[Fichas.index(Turno[-2][1][0])], i, True)
                Tablero[i][C_vacia(i)] = Fichas.pop(Fichas.index(Turno[-2][1][0]))
                print(f"La ficha {Turno[-2][1][0]} ha salido de la carcel")
                Turno[0] = 0
                Turno[1] = 0

# Variables globales
Tablero = []
Colores = ["Rojo", "Verde", "Azul", "Naranja"]
Fichas = []
DicF = {}
Modo = None
Color = None

def seleccionar_modo():
    global Modo
    text_jugador = font.render("Modo Jugador (Dados Aleatorios)", True, BLACK)
    text_desarrollador = font.render("Modo Desarrollador (Ingresar Dados)", True, BLACK)
    rect_jugador = text_jugador.get_rect(center=(width//2, height//2 - 50))
    rect_desarrollador = text_desarrollador.get_rect(center=(width//2, height//2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_jugador.collidepoint(event.pos):
                    return 1
                elif rect_desarrollador.collidepoint(event.pos):
                    return 2

        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, rect_jugador)
        pygame.draw.rect(screen, GRAY, rect_desarrollador)
        screen.blit(text_jugador, rect_jugador)
        screen.blit(text_desarrollador, rect_desarrollador)
        pygame.display.flip()

def main():
    global Tablero, Colores, Fichas, DicF, Modo, Color

    Tablero = []
    for row in range(15):
        Tablero.append([])
        for col in range(15):
            if (row, col) in [(0, 0), (0, 14), (14, 0), (14, 14)]:
                Tablero[row].append({"tipo": "salida", "color": Colores[row//4], "fichas": []})
            else:
                Tablero[row].append({"tipo": "normal", "color": None, "fichas": []})

    Fichas = []
    DicF = {}
    for color in Colores:
        for i in range(4):
            Fichas.append({
                "color": color,
                "id": i,
                "pos": (0, 0)
            })

    Modo = seleccionar_modo()
    if Modo is None:
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_board(screen)
        draw_pieces(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()