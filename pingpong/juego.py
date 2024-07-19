import pygame
import pygame_gui
import sys
import random
from math import *

pygame.init()

# Cargar el sonido
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

#Color del fondo y otros objetos

background = (51, 60, 135)  
white = (236, 240, 241)
red = (203, 67, 53)
blue = (52, 152, 219)
yellow = (244, 208, 63)
dark_red = (178, 34, 34)
dark_blue = (0, 0, 139)

top = white
bottom = white
left = white
right = white

margin = 4

scoreLeft = 0
scoreRight = 0
maxScore = 20
playerName = "Jugador"

font = pygame.font.SysFont("Arial", 30)
largeFont = pygame.font.SysFont("Arial", 60)
smallFont = pygame.font.SysFont("Arial", 20)

# Cargar la imagen de la pelota
ball_image = pygame.image.load("pelota.png")
ball_image = pygame.transform.scale(ball_image, (20, 20))  # Ajustar al tamaño de la pelota (20x20)

# Dibuja el límite del tablero
def boundary():
    global top, bottom, left, right
    pygame.draw.rect(display, left, (0, 0, margin, height))
    pygame.draw.rect(display, top, (0, 0, width, margin))
    pygame.draw.rect(display, right, (width-margin, 0, margin, height))
    pygame.draw.rect(display, bottom, (0, height - margin, width, margin))

    l = 25
    # Dibuja una línea discontinua
    dash_length = 14
    gap_length = 7
    for y in range(12, height - 20, dash_length + gap_length):
        pygame.draw.rect(display, white, (width / 2 - margin / 2, y, margin, dash_length))

# Definición de la clase de la Pala  
class Paddle:
    def __init__(self, position):
        self.w = 10
        self.h = self.w*8
        self.paddleSpeed = 6
            
        if position == -1:
            self.x = 1.5*margin
            self.color = dark_red  # Color rojo fuerte para la paleta izquierda
        else:
            self.x = width - 1.5*margin - self.w
            self.color = blue  # Color azul oscuro para la paleta derecha
            
        self.y = height/2 - self.h/2

    # Mostrar la pala
    def show(self):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))

    # Movimiento de la pala
    def move(self, ydir):
        self.y += self.paddleSpeed*ydir
        if self.y < 0:
            self.y -= self.paddleSpeed*ydir
        elif self.y + self.h> height:
            self.y -= self.paddleSpeed*ydir

    # Movimiento de la IA
    def ai_move(self, ball):
        if ball.y < self.y + self.h/2:
            self.move(-1)
        elif ball.y > self.y + self.h/2:
            self.move(1)

leftPaddle = Paddle(-1)
rightPaddle = Paddle(1)

# Definir la clase de la pelota
class Ball:
    def __init__(self, color):
        self.r = 20
        self.x = width/2 - self.r/2
        self.y = height/2 -self.r/2
        self.color = color
        self.angle = random.randint(-75, 75)
        if random.randint(0, 1):
            self.angle += 180
        
        self.speed = 8
        self.initial_speed = 8
        self.last_point_time = pygame.time.get_ticks()  # Tiempo del último punto
        self.ball_speed_increase_rate = 0.009  # Tasa de aumento de velocidad de la pelota

    # Mostrar la pelota
    def show(self):
        display.blit(ball_image, (self.x, self.y))

    # Movimiento de la pelota
    def move(self):
        global scoreLeft, scoreRight
        self.x += self.speed*cos(radians(self.angle))
        self.y += self.speed*sin(radians(self.angle))
        if self.x + self.r > width - margin:
            scoreLeft += 1
            score_sound.play()
            self.resetBall()
            pygame.time.wait(1500)  # Espera 1.5 segundos antes de mover la pelota nuevamente
        if self.x < margin:
            scoreRight += 1
            score_sound.play()
            self.resetBall()
            pygame.time.wait(1500)  # Espera 1.5 segundos antes de mover la pelota nuevamente
        if self.y < margin:
            self.angle = - self.angle
        if self.y + self.r  >=height - margin:
            self.angle = - self.angle

        # Aumenta la velocidad gradualmente si no hay puntos después de 10 segundos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_point_time > 10000:  # Han pasado más de 10 segundos desde el último punto
            self.speed += self.ball_speed_increase_rate

    # Restablecer la posición y dirección de la pelota
    def resetBall(self):
        self.x = width/2 - self.r/2
        self.y = height/2 -self.r/2
        self.angle = random.randint(-75, 75)
        if random.randint(0, 1):
            self.angle += 180
        self.speed = self.initial_speed  # Reinicia la velocidad de la pelota
        self.last_point_time = pygame.time.get_ticks()  # Actualiza el tiempo del último punto

    # Comprobar y reflejar la pelota cuando golpea la paleta.
    def checkForPaddle(self):
        if self.x < width/2:
            if leftPaddle.x < self.x < leftPaddle.x + leftPaddle.w:
                if leftPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r< leftPaddle.y + 10:
                    self.angle = -45
                    pong_sound.play()
                if leftPaddle.y + 10 < self.y < leftPaddle.y + 20 or leftPaddle.y + 10 < self.y + self.r< leftPaddle.y + 20:
                    self.angle = -30
                    pong_sound.play()
                if leftPaddle.y + 20 < self.y < leftPaddle.y + 30 or leftPaddle.y + 20 < self.y + self.r< leftPaddle.y + 30:
                    self.angle = -15
                    pong_sound.play()
                if leftPaddle.y + 30 < self.y < leftPaddle.y + 40 or leftPaddle.y + 30 < self.y + self.r< leftPaddle.y + 40:
                    self.angle = -10
                    pong_sound.play()
                if leftPaddle.y + 40 < self.y < leftPaddle.y + 50 or leftPaddle.y + 40 < self.y + self.r< leftPaddle.y + 50:
                    self.angle = 10
                    pong_sound.play()
                if leftPaddle.y + 50 < self.y < leftPaddle.y + 60 or leftPaddle.y + 50 < self.y + self.r< leftPaddle.y + 60:
                    self.angle = 15
                    pong_sound.play()
                if leftPaddle.y + 60 < self.y < leftPaddle.y + 70 or leftPaddle.y + 60 < self.y + self.r< leftPaddle.y + 70:
                    self.angle = 30
                    pong_sound.play()
                if leftPaddle.y + 70 < self.y < leftPaddle.y + 80 or leftPaddle.y + 70 < self.y + self.r< leftPaddle.y + 80:
                    self.angle = 45
                    pong_sound.play()
        else:
            if rightPaddle.x + rightPaddle.w > self.x  + self.r > rightPaddle.x:
                if rightPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r< leftPaddle.y + 10:
                    self.angle = -135
                    pong_sound.play()
                if rightPaddle.y + 10 < self.y < rightPaddle.y + 20 or rightPaddle.y + 10 < self.y + self.r< rightPaddle.y + 20:
                    self.angle = -150
                    pong_sound.play()
                if rightPaddle.y + 20 < self.y < rightPaddle.y + 30 or rightPaddle.y + 20 < self.y + self.r< rightPaddle.y + 30:
                    self.angle = -165
                    pong_sound.play()
                if rightPaddle.y + 30 < self.y < rightPaddle.y + 40 or rightPaddle.y + 30 < self.y + self.r< rightPaddle.y + 40:
                    self.angle = 170
                    pong_sound.play()
                if rightPaddle.y + 40 < self.y < rightPaddle.y + 50 or rightPaddle.y + 40 < self.y + self.r< rightPaddle.y + 50:
                    self.angle = 190
                    pong_sound.play()
                if rightPaddle.y + 50 < self.y < rightPaddle.y + 60 or rightPaddle.y + 50 < self.y + self.r< rightPaddle.y + 60:
                    self.angle = 165
                    pong_sound.play()
                if rightPaddle.y + 60 < self.y < rightPaddle.y + 70 or rightPaddle.y + 60 < self.y + self.r< rightPaddle.y + 70:
                    self.angle = 150
                    pong_sound.play()
                if rightPaddle.y + 70 < self.y < rightPaddle.y + 80 or rightPaddle.y + 70 < self.y + 80:
                    self.angle = 135
                    pong_sound.play()

# Mostrar el Marcador
def showScore():
    leftScoreText = font.render(f"PUNTAJE DE {playerName}: " + str(scoreLeft), True, red)
    rightScoreText = font.render("PUNTAJE DE LA CO : " + str(scoreRight), True, blue)

    display.blit(leftScoreText, (3*margin, 3*margin))
    display.blit(rightScoreText, (width/2 + 3*margin, 3*margin))

# Menu de Game Over
def gameOverMenu(winner_text):
    manager = pygame_gui.UIManager((width, height))

    winner_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width / 2 - 100, height / 2 - 150), (200, 50)),
                                               text=winner_text,
                                               manager=manager)
    
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width / 2 - 100, height / 2 + 20), (200, 50)),
                                               text='Salir',
                                               manager=manager)
    
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == replay_button: # type: ignore
                    reset()
                    is_running = False
                if event.ui_element == exit_button:
                    close()
            manager.process_events(event)

        manager.update(time_delta)
        display.fill(background)
        manager.draw_ui(display)

        pygame.display.update()

def gameOver():
    if scoreLeft == maxScore or scoreRight == maxScore:
        winner_text = "GANASTE!" if scoreLeft == maxScore else "GANÓ LA IA!"
        gameOverMenu(winner_text)

def reset():
    global scoreLeft, scoreRight
    scoreLeft = 0
    scoreRight = 0
    leftPaddle.__init__(-1)
    rightPaddle.__init__(1)
    Ball.resetBall()

def close():
    pygame.quit()
    sys.exit()

def board():
    loop = True
    leftChange = 0
    rightChange = 0
    ball = Ball(yellow)
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    Pause() # type: ignore
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_w:
                    leftChange = -1
                if event.key == pygame.K_s:
                    leftChange = 1
                if event.key == pygame.K_UP:
                    rightChange = -1
                if event.key == pygame.K_DOWN:
                    rightChange = 1
            if event.type == pygame.KEYUP:
                leftChange = 0
                rightChange = 0
        
        leftPaddle.move(leftChange)
        rightPaddle.ai_move(ball)
        ball.move()
        ball.checkForPaddle() 
        
        display.fill(background)
        showScore()

        ball.show()
        leftPaddle.show()
        rightPaddle.show()

        boundary()

        gameOver()
        
        pygame.display.update()
        clock.tick(60)

    # Definir la clase del Menu Principal
def menu():
    manager = pygame_gui.UIManager((width, height))

    welcome_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((width / 2 - 200, height / 2 - 200), (400, 100)),
        text="Bienvenido al juego del PingPong",
        manager=manager,
        object_id="#welcome_label"
    )

    name_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((width / 2 - 100, height / 2 - 100), (200, 40)),
        manager=manager
    )

    next_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width / 2 - 75, height / 2 - 30), (150, 50)),
        text='Siguiente',
        manager=manager
    )

    points_10_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width / 2 - 75, height / 2 + 50), (150, 50)),
        text='10 puntos',
        manager=manager,
        visible=0  # Oculto inicialmente
    )

    points_15_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width / 2 - 75, height / 2 + 100), (150, 50)),
        text='15 puntos',
        manager=manager,
        visible=0  # Oculto inicialmente
    )

    points_20_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width / 2 - 75, height / 2 + 150), (150, 50)),
        text='20 puntos',
        manager=manager,
        visible=0  # Oculto inicialmente
    )

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width / 2 - 75, height / 2 + 250), (150, 50)),
        text='Iniciar el juego',
        manager=manager,
        visible=0  # Oculto inicialmente
    )

    selected_score = 10  # Valor predeterminado
    playerName = "Jugador"

    is_running = True
    input_phase = True  # Controla si estamos en la fase de entrada de nombre

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if input_phase and event.ui_element == next_button:
                    playerName = name_input.get_text()
                    input_phase = False
                    points_10_button.show()
                    points_15_button.show()
                    points_20_button.show()
                    start_button.show()
                    next_button.hide()
                    name_input.hide()
                if not input_phase:
                    if event.ui_element == points_10_button:
                        selected_score = 10
                    if event.ui_element == points_15_button:
                        selected_score = 15
                    if event.ui_element == points_20_button:
                        selected_score = 20
                    if event.ui_element == start_button:
                        global maxScore
                        maxScore = selected_score
                        is_running = False

            manager.process_events(event)

        manager.update(time_delta)
        display.fill(background)
        manager.draw_ui(display)

        pygame.display.update()

    return playerName

playerName = menu()
board()
