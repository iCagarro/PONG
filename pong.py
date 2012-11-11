#!/usr/bin/python3
# Implementation of classic arcade game Pong

import pygame, sys
from pygame.locals import*
import random

# iniciem el pygame
pygame.init()

# parametres del joc
WIDTH = 600
HEIGHT = 400       
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
acceleracio = 0.01
ball_radius = 10
ball_vel = [0, 0]
right = True
score1 = 0
score2 = 0
mode = ''
t = 0

# imatges del fons, el paddle i la ball
ball = 'ball.png'
fons = 'fons.jpg'
paddle = 'pad.jpg'

# seleccionat el tipus de lletra escriure
font = pygame.font.SysFont("Arial", 20)

# pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# fons
background = pygame.image.load(fons).convert()
# ball
ball_im = pygame.image.load(ball)
# paddle
paddle_im = pygame.image.load(paddle).convert()
# titol de la finestra
pygame.display.set_caption('PONG')

# FUNCIONS
# inicial
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2, ball_pos, ball_vel, mode
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]

# ball inicial
def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right == True:
        x = random.randrange(12, 24) * 0.015
        y = random.randrange(5, 18) * 0.015
        ball_vel = [x, -y]
        return ball_vel
    if right == False:
        x = random.randrange(12, 24) * 0.015
        y = random.randrange(5, 18) * 0.015
        ball_vel = [-x, -y]
        return ball_pos, ball_vel

# apretar tecla
def key_down():
    global paddle1_vel, paddle2_vel, mode
    if event.type == KEYDOWN:
        if event.key == K_w:
            paddle1_vel = -0.5
        elif event.key == K_s:
            paddle1_vel = 0.5
        elif event.key == K_UP:
            paddle2_vel = -0.5
        elif event.key == K_DOWN:
            paddle2_vel = 0.5
        # iniciar la partida
        if event.key == K_1:
            init()
            mode = 'cpu'
        elif event.key == K_2:
            init()
            mode = 'two'
        if event.key == K_SPACE and (mode == 'cpu' or mode == 'two') and ball_vel == [0, 0]:
            ball_init(right)        
        if event.key == K_ESCAPE:
            quit()
            
# aixecar tecla
def key_up():
    global paddle1_vel, paddle2_vel
    if event.type == KEYUP:
        if event.key == K_w:
            paddle1_vel = 0
        elif event.key == K_s:
            paddle1_vel = 0
        elif event.key == K_UP:
            paddle2_vel = 0
        elif event.key == K_DOWN:
            paddle2_vel = 0

# event tecla
def key_handle():
    key_down()
    key_up()

# limits dels paddles
def paddle_limits():
    if paddle1_pos[1] <= (HALF_PAD_HEIGHT - 1):
        paddle1_vel = 0
        paddle1_pos[1] = HALF_PAD_HEIGHT
    if paddle1_pos[1] >= (HEIGHT - HALF_PAD_HEIGHT + 1):
        paddle1_vel = 0
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos[1] <= (HALF_PAD_HEIGHT - 1):
        paddle2_vel = 0
        paddle2_pos[1] = HALF_PAD_HEIGHT
    if paddle2_pos[1] >= (HEIGHT - HALF_PAD_HEIGHT + 1):
        paddle2_vel = 0
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT

# moviment ball
def update_ball():
    global ball_pos, ball_vel
    ball_pos[0] += ball_vel[0] * t
    ball_pos[1] += ball_vel[1] * t

# moviment paddle
def update_paddle():
    global paddle1_pos, paddle1_vel, paddle2_pos, paddle2_vel
    paddle2_pos[1] += paddle2_vel * t
    # mode two players
    if mode == 'two':
        paddle1_pos[1] += paddle1_vel * t
    # mode cpu
    if mode == 'cpu':
        n = ball_pos[1] - paddle1_pos[1]
        if ball_vel[0] < 0:
            paddle1_pos[1] += 0 * t
        if n >= 0 and ball_vel[0] < 0:
            paddle1_pos[1] += 0.5 * t
        elif n <= 0 and ball_vel[0] < 0:
            paddle1_pos[1] += -0.5 * t

# parets
def walls():
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= ball_radius or ball_pos[1] >= (HEIGHT - ball_radius):
        ball_vel[1] = -ball_vel[1]

# ball en contra els paddles
def ball_vs_pads():
    if ball_pos[0] < (PAD_WIDTH + ball_radius) and (ball_pos[1] < (paddle1_pos[1] + HALF_PAD_HEIGHT) and ball_pos[1] > (paddle1_pos[1] - HALF_PAD_HEIGHT)):
        if ball_vel[0] < -120 * 0.015:
            ball_vel[0] = abs(ball_vel[0])
        else:
            ball_vel[0] = abs(ball_vel[0] + ball_vel[0] * 0.1)
    if ball_pos[0] > (WIDTH - PAD_WIDTH - ball_radius) and (ball_pos[1] < (paddle2_pos[1] + HALF_PAD_HEIGHT) and ball_pos[1] > (paddle2_pos[1] - HALF_PAD_HEIGHT)):
        if ball_vel[0] > 120 * 0.015:
            ball_vel[0] = -abs(ball_vel[0])
        else:
            ball_vel[0] = -abs(ball_vel[0] + ball_vel[0] * 0.1) 

# gol
def goal():
    global score1, score2
    if ball_pos[0] < PAD_WIDTH:
        ball_init(True)
        score1 += 1
    if ball_pos[0] > WIDTH - PAD_WIDTH:
        ball_init(False)
        score2 += 1

# render
def render():
    # dibuixem el fons
    screen.blit(background, (0, 0))
    # dibuixar paddles
    screen.blit(paddle_im, (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT))
    screen.blit(paddle_im, (paddle2_pos[0] - HALF_PAD_WIDTH + 1, paddle2_pos[1] - HALF_PAD_HEIGHT))
    # dibuixar ball
    screen.blit(ball_im, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))

    #dibuixar cartells
    text = font.render("1. Mode CPU", 1, (0,0,0))
    screen.blit(text, (50, 50))
    text = font.render("2. Mode dos jugadors", 1, (0,0,0))
    screen.blit(text, (50, 70))
    text = font.render("ESPAI per comencar", 1, (0,0,0))
    screen.blit(text, (50, 90))

def quit():
    pygame.quit()
    sys.exit()

# iniciem el programa
init()

# LOOP PRINCIPAL
while True:
    # rellotge: agafem el temps del principi
    t1 = pygame.time.get_ticks()

    # apagar
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
 
    # posicio de la ball (t)
    update_ball()

    # posicio dels paddles
    update_paddle()

    # paddle limits
    paddle_limits()

    # walls
    walls()

    # ball vs pads
    ball_vs_pads()
    
    # gols
    goal()
    
    # teclat
    key_handle()

    # render
    render()

    # rellotge: agafem el temps del final i definim la variable t
    t2 = pygame.time.get_ticks()
    t = t2 - t1
    
    pygame.display.update()
