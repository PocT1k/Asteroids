import pygame
import math
import time
from utils import WIDTH, HEIGHT, ORANGE, BLUE
from laser import shoot_laser

class Ship:
    def __init__(self, number):

        self.number = number
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)

        if number == 0:
            pygame.draw.polygon(self.image, ORANGE, [(0, 40), (25, 0), (50, 40)])  #оранжевый
            self.start = WIDTH * 0.2, HEIGHT * 0.2
            self.keysPlayer = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_e]
        elif number == 1:
            pygame.draw.polygon(self.image, BLUE, [(0, 40), (25, 0), (50, 40)])  #синий
            self.start = WIDTH * 0.8, HEIGHT * 0.8
            self.rect = self.image.get_rect(center=(self.start))
            self.keysPlayer = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RCTRL]
        self.rect = self.image.get_rect(center=(self.start))

        self.angle = 0
        self.speed = 5
        # self.lives = 3
        self.hp = 3
        self.invincible_until = 0
        self.last_laser_time = 0
        self.laser_cooldown = 0.2
        self.shots_left = 30  # Максимальное количество выстрелов
        self.reload_time = 2  # Время перезарядки в секундах (2 секунды)
        self.is_reloading = False
        self.reload_start_time = 0
        self.is_respawning = False
        self.respawn_start_time = 0
        self.respawn_delay = 3  # Время воскрешения в секундах
        self.death_screen_time = 2  # Задержка экрана смерти в секундах
        # self.invincible_until = time.time() + 1

    def update(self, keys):
        # Если игрок возрождается
        if self.is_respawning:
            if time.time() - self.respawn_start_time >= self.respawn_delay:
                self.is_respawning = False
                self.hp = 3  # Восстановление ХП
                self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Возвращение к стартовой позиции
                self.invincible_until = time.time() + 1  # Небольшая неуязвимость после воскрешения
            return  # Не выполняем дальнейшее обновление во время воскрешения

        # Управление игроком
        if keys[self.keysPlayer[0]]:
            self.angle += 5
        if keys[self.keysPlayer[1]]:
            self.angle -= 5
        if keys[self.keysPlayer[2]]:
            self.rect.x += int(self.speed * math.cos(math.radians(self.angle)))
            self.rect.y -= int(self.speed * math.sin(math.radians(self.angle)))
        if keys[self.keysPlayer[3]]:
            self.rect.x -= int(self.speed * math.cos(math.radians(self.angle)))
            self.rect.y += int(self.speed * math.sin(math.radians(self.angle)))

        self.rect.x %= WIDTH
        self.rect.y %= HEIGHT

        # Проверка на перезарядку
        if self.is_reloading:
            if time.time() - self.reload_start_time >= self.reload_time:
                self.is_reloading = False
                self.shots_left = 30

    def take_damage(self):
        """Уменьшает ХП при получении урона."""
        if self.hp > 0:
            self.hp -= 1
            if self.hp <= 0:
                self.lives -= 1
                if self.lives > 0:
                    self.is_respawning = True
                    self.respawn_start_time = time.time() + self.death_screen_time  # Учитываем задержку экрана смерти
                else:
                    # Если жизней больше нет, просто отображаем экран смерти
                    self.is_respawning = True
                    self.respawn_start_time = time.time() + self.death_screen_time

    def shoot_laser(self):
        if self.shots_left > 0 and not self.is_reloading:
            # Стрельба из вершины треугольника
            tip_x = self.rect.centerx + 25 * math.cos(math.radians(self.angle))
            tip_y = self.rect.centery - 25 * math.sin(math.radians(self.angle))
            shoot_laser(tip_x, tip_y, self.angle, self.number)
            self.shots_left -= 1
            self.last_laser_time = time.time()
        elif self.shots_left <= 0 and not self.is_reloading:
            self.is_reloading = True
            self.reload_start_time = time.time()

    def draw(self, screen):
        if not self.is_respawning:
            rotated_image = pygame.transform.rotate(self.image, self.angle - 90)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            current_time = time.time()
            if current_time > self.invincible_until:
                screen.blit(rotated_image, new_rect.topleft)
            else:
                if int(current_time * 10) % 2 == 0:
                    screen.blit(rotated_image, new_rect.topleft)
        elif self.is_respawning:
            # Отображение экрана смерти
            death_text = pygame.font.Font(None, 72).render("Вы умерли", True, (255, 0, 0))
            text_rect = death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(death_text, text_rect)

        # Отображение оставшихся выстрелов
        shots_text = pygame.font.Font(None, 24).render(f"Shots: {self.shots_left}", True, (255, 255, 255))
        screen.blit(shots_text, (self.rect.centerx - 15, self.rect.centery + 50))

        # Отображение ХП корабля
        hp_text = pygame.font.Font(None, 24).render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (self.rect.centerx - 15, self.rect.centery + 70))

    def reset(self):
        time.sleep(0.5)
        """Сбрасывает состояние корабля после смерти."""
        self.hp = 3  # Восстановление полного запаса ХП
        self.rect = self.image.get_rect(center=(self.start))  # Возвращение на стартовую позицию
        self.angle = 0  # Сброс угла поворота
        self.invincible_until = time.time() + 1  # Кратковременная неуязвимость
        self.is_reloading = False  # Сброс состояния перезарядки
        self.shots_left = 30  # Полный боезапас
