import pygame
import math
import time
from utils import lasers, WIDTH, HEIGHT, YELLOW


def checkCollisionAsteroid(ship, asteroids, current_time):
    # Проверка столкновений с астероидами
    if current_time > ship.invincible_until:
        for asteroid in asteroids:
            dist = math.hypot(ship.rect.centerx - asteroid['pos'][0], ship.rect.centery - asteroid['pos'][1])
            if dist < asteroid['radius']:
                ship.hp -= 1
                ship.invincible_until = current_time + 1

                if ship.hp <= 0:
                    #if ship.lives > 0:
                    ship.reset()

    # Проверка на стрельбу
    if pygame.key.get_pressed()[ship.keysPlayer[4]] and time.time() - ship.last_laser_time > ship.laser_cooldown:
        ship.shoot_laser()

    for laser in lasers:
        if laser['num'] == ship.number:
            continue
        dist = math.hypot(laser['pos'][0] - ship.rect.centerx, laser['pos'][1] - ship.rect.centery)
        if dist < 30:
            lasers.remove(laser)  # Удаление лазера после попадания
            ship.hp -= 1
            ship.invincible_until = current_time + 1
            if ship.hp <= 0:
                ship.reset()

def checkCollisionShips(ship1, ship2, current_time):
    if current_time > ship1.invincible_until and current_time > ship2.invincible_until:
        dist = math.hypot(ship1.rect.centerx - ship2.rect.centerx, ship1.rect.centery - ship2.rect.centery)
        if dist < 30:
            ship1.hp -= 1
            ship2.hp -= 1
            ship1.invincible_until = current_time + 1
            ship2.invincible_until = current_time + 1

            if ship1.hp <= 0:
                ship1.reset()
            if ship2.hp <= 0:
                ship2.reset()


def update_lasers():
    for laser in lasers[:]:
        laser['pos'][0] += laser['vel'][0]
        laser['pos'][1] += laser['vel'][1]
        if not (0 <= laser['pos'][0] <= WIDTH and 0 <= laser['pos'][1] <= HEIGHT):
            lasers.remove(laser)

def draw_lasers(screen):
    for laser in lasers:
        pygame.draw.circle(screen, (255, 255, 0), (int(laser['pos'][0]), int(laser['pos'][1])), 3)

def shoot_laser(x, y, angle, number):
    speed = 10
    dx = speed * math.cos(math.radians(angle))
    dy = -speed * math.sin(math.radians(angle))
    lasers.append({'pos': [x, y], 'vel': [dx, dy], 'num': number})
