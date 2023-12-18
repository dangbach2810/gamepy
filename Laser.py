import pygame
WIDTH, HEIGHT = 600, 650
class Laser:
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.target = None
        self.directionX = 0
        self.direction = []
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def set_target(self, target):
        self.target = target

    def movebot(self, vel):
        self.y += vel

    def move(self):
        if self.target is not None:
            self.direction = [target - pos for pos, target in zip([self.x + 42, self.y + 36], self.target)]
            magnitude = max(1, sum(d ** 2 for d in self.direction) ** 0.5)
            self.direction = [d / magnitude for d in self.direction]
            self.x += self.speed * self.direction[0]
            self.y += self.speed * self.direction[1]
            self.directionX = self.direction[0]
            self.directionY = self.direction[1]
            if magnitude <= self.speed:
                self.target = None

        else:

            self.y -= self.speed
            if self.directionX > 0:
                self.x += self.speed * self.direction[0]
            elif self.directionX < 0:
                self.x -= -(self.speed * self.direction[0])
        if self.off_screen(WIDTH, HEIGHT) or self.x < 0 or self.x > WIDTH:
            self.target = None
    def off_screen(self, width, height):
        return not (0 <= self.x <= width and 0 <= self.y <= height)

    def is_at_target(self):
        return self.target is not None and all(
            abs(pos - target) < self.speed for pos, target in zip([self.x, self.y], self.target))

    def collision(self, obj):
        return collide(self, obj)
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
