import pygame

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
GREY = (155, 155, 155)
ORANGE = (237,118,14)
BLUE = (15,15,235)
YELLOW = (255, 255, 0)

FPS = 60

clock = pygame.time.Clock()

# Глобальные переменные
lasers = []
asteroids = []
MAX_ASTEROIDS = 8
