import pygame
import random
import time
import math
from ship import Ship
from asteroid import spawn_asteroid, update_asteroids, draw_asteroids, MAX_ASTEROIDS, asteroids
from laser import update_lasers, draw_lasers, lasers, checkCollisionShips, checkCollisionAsteroid
from utils import WIDTH, HEIGHT, BLACK, FPS, clock


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids with Modular Structure")

running = True

# Создание корабля
ship1 = Ship(0)
ship2 = Ship(1)

while running:
    current_time = time.time()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ship1.update(keys)
    ship2.update(keys)

    # Обновление и проверка объектов
    update_lasers()
    if len(asteroids) < MAX_ASTEROIDS:
        spawn_asteroid()
    update_asteroids(ship1)
    update_asteroids(ship2)

    checkCollisionAsteroid(ship1, asteroids, current_time)
    checkCollisionAsteroid(ship2, asteroids, current_time)
    checkCollisionShips(ship1, ship2, current_time)

    # Отрисовка
    screen.fill(BLACK)
    ship1.draw(screen)
    ship2.draw(screen)
    draw_lasers(screen)
    draw_asteroids(screen)

    pygame.display.flip()

pygame.quit()
