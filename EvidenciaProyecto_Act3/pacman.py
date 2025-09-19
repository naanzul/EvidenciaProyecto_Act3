from random import choice
from turtle import *
from freegames import floor, vector

# Es el puntaje del juego
state = {'score': 0}

# Son los turtles para dibujar el laberinto y el puntaje
path = Turtle(visible=False)
writer = Turtle(visible=False)

# Esta es la dirección inicial de Pacman
aim = vector(5, 0)
pacman = vector(-40, -80)

# Cada fantasma tiene posición y dirección
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# Este es el laberinto
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    """Dibuja un cuadrado de 20x20 en (x, y)"""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for count in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    """Convierte coordenadas (x, y) a índice en tiles"""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return max(0, min(index, len(tiles) - 1))  # protección contra IndexError

def valid(point):
    """Verifica si el punto no está en una pared"""
    index = offset(point)
    if tiles[index] == 0:
        return False
    index = offset(point + 19)
    if tiles[index] == 0:
        return False
    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    """Dibuja el laberinto y las comidas"""
    bgcolor('black')
    path.color('blue')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
    """Mueve Pacman y los fantasmas, actualiza puntaje"""
    writer.undo()
    writer.write(state['score'])
    clear()

    # Movemos a Pacman si el siguiente paso es válido
    if valid(pacman + aim):
        pacman.move(aim)

    # Comprobamos si Pacman come comida
    index = offset(pacman)
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    # Dibujamos a Pacman
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Movemos los fantasmas
    for point, course in ghosts:
        # Fantasmas inteligentes: se acercan a Pacman si está cerca
        if abs(pacman - point) < 80:
            dx = 5 if pacman.x > point.x else -5 if pacman.x < point.x else 0
            dy = 5 if pacman.y > point.y else -5 if pacman.y < point.y else 0
            if valid(point + vector(dx, 0)):
                course.x = dx
            else:
                course.x = 0
            if valid(point + vector(0, dy)):
                course.y = dy
            else:
                course.y = 0
        # Hacemos un movimiento aleatorio si está lejos o chocan
        elif not valid(point + course):
            options = [vector(5, 0), vector(-5, 0), vector(0, 5), vector(0, -5)]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        # Movemos el fantasma si el siguiente paso es válido
        if valid(point + course):
            point.move(course)

        # Dibujamos el fantasma
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    # Verificamos la colisión con Pacman
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return  # termina el juego

    ontimer(move, 100)

def change(x, y):
    """Cambiar dirección de Pacman si es válido"""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

# Configuración de la ventana y controles
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

world()  # Se dibuja el laberinto
move()   # inicia el movimiento
done()



