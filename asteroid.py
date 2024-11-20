import random
import pygame
import math
from utils import lasers, WIDTH, HEIGHT, GREY, asteroids


def spawn_asteroid():
    size = random.randint(25, 50)
    speed = max(1, 5 - size // 10)
    asteroid = {
        'pos': [random.randint(0, WIDTH), random.randint(0, HEIGHT)],
        'vel': [random.choice([-speed, speed]), random.choice([-speed, speed])],
        'radius': size,
        'hp': max(1, size // 20)
    }
    asteroids.append(asteroid)


def update_asteroids():
    for asteroid in asteroids:
        asteroid['pos'][0] += asteroid['vel'][0]
        asteroid['pos'][1] += asteroid['vel'][1]
        asteroid['pos'][0] %= WIDTH
        asteroid['pos'][1] %= HEIGHT

        # Проверка столкновений с лазерами
        for laser in lasers:
            dist = math.hypot(laser['pos'][0] - asteroid['pos'][0], laser['pos'][1] - asteroid['pos'][1])
            if dist < asteroid['radius']:
                asteroid['hp'] -= 1  # Уменьшение ХП астероида
                lasers.remove(laser)  # Удаление лазера после попадания
                if asteroid['hp'] <= 0:
                    asteroids.remove(asteroid)  # Удаление астероида, если ХП <= 0
                break  # Лазер может поразить только один астероид


def draw_asteroids(screen):
    for asteroid in asteroids:
        pygame.draw.circle(screen, GREY, asteroid['pos'], asteroid['radius'])
        # Отображение ХП астероида
        hp_text = pygame.font.Font(None, 24).render(str(asteroid['hp']), True, GREY)
        screen.blit(hp_text, (asteroid['pos'][0] - 10, asteroid['pos'][1] - 10))
