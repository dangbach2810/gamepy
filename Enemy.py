from Ship import Ship
from Laser import Laser
import pygame
import os

# Load images Enemy
Enemy1 = pygame.image.load(os.path.join("assets", "enemy1.png"))
Enemy2 = pygame.image.load(os.path.join("assets", "enemy2.png"))
Enemy3 = pygame.image.load(os.path.join("assets", "enemy3.png"))
#Laser of Enemy
new_width = 30
new_height = 30
Laser_E1 = pygame.image.load(os.path.join("assets", "laser_enemy.png"))
Laser_E2 = pygame.image.load(os.path.join("assets", "laser_enemy.png"))
Laser_E3 = pygame.image.load(os.path.join("assets", "laser_enemy.png"))

Laser_E1 = pygame.transform.scale(Laser_E1, (new_width, new_height))
Laser_E2 = pygame.transform.scale(Laser_E2, (new_width, new_height))
Laser_E3 = pygame.transform.scale(Laser_E3, (new_width, new_height))
class Enemy(Ship):
    COLOR_MAP = {
        "Enemy1": (Enemy1, Laser_E1),
        "Enemy2": (Enemy2, Laser_E2),
        "Enemy3": (Enemy3, Laser_E3)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 35, self.y + 45, self.laser_img, 7)
            self.lasers.append(laser)
            self.cool_down_counter = 1