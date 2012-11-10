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
acceleracio = 0.5
ball_radius = 10
ball_vel = [0, 0]
right = True
score1 = 0
score2 = 0
mode = ''

# imatges del fons, el paddle i la ball
ball = 'ball.png'
fons = 'fons.jpg'
paddle = 'pad.jpg'
##fons_init = 'fons_init.png'

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
### fons_init
##fons_init_im = pygame.image.load(fons_init)

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
            paddle1_vel = -acceleracio
        elif event.key == K_s:
            paddle1_vel = acceleracio
        elif event.key == K_UP:
            paddle2_vel = -acceleracio
        elif event.key == K_DOWN:
            paddle2_vel = acceleracio
        # iniciar la parida
        if event.key == K_1:
            init()
            mode = 'cpu'
        elif event.key == K_2:
            init()
            mode = 'two'
        if event.key == K_SPACE and (mode == 'cpu' or mode == 'two') and ball_vel == [0, 0]:
            ball_init(right)        

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
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

# moviment paddle
def update_paddle():
    global paddle1_pos, paddle1_vel, paddle2_pos, paddle2_vel
    paddle2_pos[1] += paddle2_vel
    # mode two players
    if mode == 'two':
        paddle1_pos[1] += paddle1_vel
    # mode cpu
    if mode == 'cpu':
        n = ball_pos[1] - paddle1_pos[1]
        if ball_vel[0] < 0:
            paddle1_pos[1] += 0
        if n >= 0 and ball_vel[0] < 0:
            paddle1_pos[1] += acceleracio
        elif n <= 0 and ball_vel[0] < 0:
            paddle1_pos[1] += -acceleracio

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

# iniciem el programa
init()

# LOOP PRINCIPAL
while True:
    # apagar
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
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

    # dibuixem el fons
    screen.blit(background, (0, 0))
    # dibuixar paddles
    screen.blit(paddle_im, (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT))
    screen.blit(paddle_im, (paddle2_pos[0] - HALF_PAD_WIDTH + 1, paddle2_pos[1] - HALF_PAD_HEIGHT))
    # dibuixar ball
    screen.blit(ball_im, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))

    clock = pygame.time.Clock()
    clock.tick(1000)
    
    pygame.display.update()
