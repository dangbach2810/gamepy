import pygame
class Item:
    def __init__(self, x, y, img, effect):
        self.x = x
        self.y = y
        self.img = img
        self.effect = effect
        self.speed = 50
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def get_height(self):
        return self.img.get_height()
