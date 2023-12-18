WIDTH, HEIGHT = 600, 650
class Ship:
    COOLDOWN = 20  # tốc độ ra đạn

    def __init__(self, x, y, health=200):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.armor = 0
        self.armor_status = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.movebot(vel)
            if laser.off_screen(WIDTH, HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if obj.armor_status == 1:
                    obj.armor -= 50
                    if obj.armor <= 0:
                        obj.armor_status = 0
                else:
                    obj.health -= 50
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self, event):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img, event, 7)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()