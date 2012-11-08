#!/usr/bin/python2
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
ball_radius = 10
ball_vel = [0, 0]
right = True
score1 = 0
score2 = 0

# imatges del fons, el paddle i la ball
ball = 'ball.png'
fons = 'fons.jpg'
paddle = 'pad.jpg'

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

# funcions
def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right == True:
        x = random.randrange(12, 24) * 0.01
        y = random.randrange(-18, 18) * 0.01
        ball_vel = [x, y]
        return ball_vel
    if right == False:
        x = random.randrange(12, 24) * 0.01
        y = random.randrange(-18, 18) * 0.01
        ball_vel = [-x, y]
        return ball_pos, ball_vel

ball_init(right)

# LOOP PRINCIPAL
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
    # posicio de la ball (t)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # posicio dels paddles
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel

    # paddle limits
    if paddle1_pos[1] < (HALF_PAD_HEIGHT - 1):
        paddle1_vel = 0
        paddle1_pos[1] = HALF_PAD_HEIGHT
    if paddle1_pos[1] > (HEIGHT - HALF_PAD_HEIGHT + 1):
        paddle1_vel = 0
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos[1] < (HALF_PAD_HEIGHT - 1):
        paddle2_vel = 0
        paddle2_pos[1] = HALF_PAD_HEIGHT
    if paddle2_pos[1] > (HEIGHT - HALF_PAD_HEIGHT + 1):
        paddle2_vel = 0
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT

    # walls
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= ball_radius or ball_pos[1] >= (HEIGHT - ball_radius):
        ball_vel[1] = -ball_vel[1]

    # ball vs pads
    if ball_pos[0] <= (PAD_WIDTH + ball_radius) and (ball_pos[1] <= (paddle1_pos[1] + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle1_pos[1] - HALF_PAD_HEIGHT)):
        ball_vel[0] = abs(ball_vel[0] + ball_vel[0] * 0.1)
    if ball_pos[0] >= (WIDTH - PAD_WIDTH - ball_radius) and (ball_pos[1] <= (paddle2_pos[1] + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle2_pos[1] - HALF_PAD_HEIGHT)):
        ball_vel[0] = -abs(ball_vel[0] + ball_vel[0] * 0.1) 

    # gols
    if ball_pos[0] < - ball_radius:
        ball_init(True)
        score1 += 1
    if ball_pos[0] > WIDTH + ball_radius:
        ball_init(False)
        score2 += 1
    
    # teclat
    if event.type == KEYDOWN:
        if event.key == K_w:
            paddle1_vel = -1
        elif event.key == K_s:
            paddle1_vel = 1
        elif event.key == K_UP:
            paddle2_vel = -1
        elif event.key == K_DOWN:
            paddle2_vel = 1
        elif event.key == K_b:
            right = True

    if event.type == KEYUP:
        if event.key == K_w:
            paddle1_vel = 0
        elif event.key == K_s:
            paddle1_vel = 0
        elif event.key == K_UP:
            paddle2_vel = 0
        elif event.key == K_DOWN:
            paddle2_vel = 0

    # dibuixar fons
    screen.blit(background, (0, 0))
    # dibuixar paddles
    screen.blit(paddle_im, (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT))
    screen.blit(paddle_im, (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT))
    # dibuixar ball
    screen.blit(ball_im, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))
    # dibuixar scores

    pygame.display.update()
