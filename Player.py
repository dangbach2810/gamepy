from Ship import Ship
from Laser import Laser
import pygame
import os
# Load images Player
PlayerLv1 = pygame.image.load(os.path.join("assets", "tank_red_1.png"))
PlayerLv2 = pygame.image.load(os.path.join("assets", "tank_red_2.png"))
PlayerLv3 = pygame.image.load(os.path.join("assets", "tank_red_3.png"))
Laser_Player = pygame.image.load(os.path.join("assets", "laser_red.png"))
Laser_Player = pygame.transform.scale(Laser_Player, (30, 30))
pygame.mixer.init()
#Sound
laser_sound = pygame.mixer.Sound("assets/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
WIDTH, HEIGHT = 600, 650
class Player(Ship):
    count = 0
    def __init__(self, x, y, health=200):
        super().__init__(x, y, health)
        self.ship_img = PlayerLv1
        self.laser_img = Laser_Player
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.level = 1
        self.score = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:

            laser.move()
            if laser.off_screen(WIDTH, HEIGHT):
                self.lasers.remove(laser)

            else:

                for obj in objs[:]:
                    if laser.collision(obj):
                        self.score += 10
                        self.count += 1
                        if self.count >= 3 and self.level < 3:
                            if self.health < 200:
                                self.health += (200 - self.health)*0.8
                            self.level += 1
                            self.count = 0

                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

                        explosion_sound.play()

    def draw(self, window):
        if self.level == 2:
            self.ship_img = PlayerLv2
        elif self.level == 3:
            self.ship_img = PlayerLv3
        super().draw(window)
        self.healthbar(window)

    def shoot(self, target):
        if self.cool_down_counter == 0:
            for i in range(self.level):
                player_center = self.get_center()
                laser = Laser(player_center[0]+i*20, player_center[1], self.laser_img, 7)
                laser.set_target((target[0]+i*20,target[1]))
                self.lasers.append(laser)
                laser_sound.play()
            self.cool_down_counter = 1

    def get_center(self):
        return self.x + 10 + self.ship_img.get_width() // 8, self.y-20 + self.ship_img.get_height() // 8

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))
        font = pygame.font.SysFont(None, 28)  # Chọn font và kích thước
        level_text = font.render(f"{self.level}", True, (255,255,255))  # Tạo đối tượng văn bản
        window.blit(level_text, (self.x - level_text.get_width(), self.y + self.ship_img.get_height() + 5))
