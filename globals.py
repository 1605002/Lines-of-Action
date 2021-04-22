import pygame
from constants import *
pygame.init()

screen = pygame.display.set_mode(GAME_SIZE)
background = pygame.image.load("galaxy.png").convert()
font = pygame.font.SysFont(None, 45)

is_ai = [True]
last_move = [-1, -1, -1, -1]
logpy = open("logpy.txt", "w")

