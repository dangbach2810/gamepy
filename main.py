import pygame
import os
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images Enemy
Enemy1 = pygame.image.load(os.path.join("assets", "enemy1.png"))
Enemy2 = pygame.image.load(os.path.join("assets", "enemy2.png"))
Enemy3 = pygame.image.load(os.path.join("assets", "enemy3.png"))

# Load images Player
PlayerLv1 = pygame.image.load(os.path.join("assets", "tank_red_1.png"))
PlayerLv2 = pygame.image.load(os.path.join("assets", "tank_red_2.png"))
PlayerLv3 = pygame.image.load(os.path.join("assets", "tank_red_3.png"))

# Load images Lasers
new_width = 30
new_height = 30
Laser_E1 = pygame.image.load(os.path.join("assets", "laser_enemy.png"))
Laser_E2 = pygame.image.load(os.path.join("assets", "laser_enemy.png"))
Laser_E3 = pygame.image.load(os.path.join("assets", "laser_enemy.png"))
Laser_Player = pygame.image.load(os.path.join("assets", "laser_red.png"))

Laser_Player = pygame.transform.scale(Laser_Player, (new_width, new_height))
Laser_E1 = pygame.transform.scale(Laser_E1, (new_width, new_height))
Laser_E2 = pygame.transform.scale(Laser_E2, (new_width, new_height))
Laser_E3 = pygame.transform.scale(Laser_E3, (new_width, new_height))

# Item image
HEAL_ITEM_IMG = pygame.image.load(os.path.join("assets", "heal_item.png"))
ARMOR_ITEM_IMG = pygame.image.load(os.path.join("assets", "armor_item.png"))

# Background
BG_Wait = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))
BG_Game = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Button
start_button_img = pygame.image.load(os.path.join("assets", "btn_start.jpg"))
start_button_rect = start_button_img.get_rect(center=(WIDTH / 2, 550))
continue_button_img = pygame.image.load(os.path.join("assets", "btn_continue.jpg"))
continue_button_rect = continue_button_img.get_rect(center=(WIDTH / 2, 550))
option_button_img = pygame.image.load(os.path.join("assets", "btn_option.jpg"))
option_button_rect = option_button_img.get_rect(center=(WIDTH / 2, 650))

# Sound
pygame.mixer.music.load("assets/background.mp3")
laser_sound = pygame.mixer.Sound("assets/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")


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
    

def main(level, lives, health, player_level):
    score = 0
    run = True
    FPS = 60
    level = level -1
    # lives = 5
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1
    
    items = []
    item_vel = 3
    armor = 50
    def create_item():
        x = random.randrange(50, WIDTH - 50)
        y = random.randrange(-1500, -100)
        img = random.choice([HEAL_ITEM_IMG, ARMOR_ITEM_IMG])
        if img == HEAL_ITEM_IMG:
            effect = "heal"
        else:
            effect = "armor"
            
        item = Item(x, y, img, effect)
        items.append(item)


    player_vel = 5
    laser_vel = 5

    player = Player(WIDTH/2, 520)
    player.health = health
    player.level = player_level
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():

        WIN.blit(BG_Game, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {player.score}", 1, (255, 255, 255))
        armor_label = main_font.render(f"Armor: {player.armor}", 1, (255, 255, 255))
        # text = main_font.render("Score: " + str(score), True, "#3333FF")
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (230, 10))
        WIN.blit(armor_label, (10, 50))

        for enemy in enemies:
            enemy.draw(WIN)
        
        for item in items:
            item.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    paused = False
    # screen_paused = False
    while run:
        clock.tick(60)
        redraw_window()

        if lives <= 0 or player.health <= 0:

            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                  random.choice(["Enemy1", "Enemy2", "Enemy3"]))
                    enemies.append(enemy)
        
        if random.randrange(0, 2 * 50) == 1:
            create_item()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("data.txt", "w") as savelevel:
                    savelevel.write(f"{level, lives, player.health, player.level}")
                    savelevel.close()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(event.pos)
                # print(event.pos)


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # Khi nhấn Space, chuyển đổi trạng thái pause
                    # screen_paused = True


        if not paused:
            for laser in player.lasers:
                laser.move()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0:  # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
                player.x += player_vel
            if keys[pygame.K_w] and player.y - player_vel > 0:  # up
                player.y -= player_vel
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
                player.y += player_vel
            # if keys[pygame.K_SPACE]:
            #     pygame.MOUSEBUTTONDOWN

            for enemy in enemies[:]:

                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel, player)
                if random.randrange(0, 2 * 60) == 1:
                    enemy.shoot()
                if collide(enemy, player):
                    if player.armor_status == 1:
                        player.health -= 0
                        player.armor -= 50
                        if player.armor <= 0:
                            player.armor_status = 0
                    else:
                        player.armor_status = 0
                        player.health -= 50
                    enemies.remove(enemy)
                    player.score  += 10

                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)
            player.move_lasers(-laser_vel, enemies)
            
            for item in items[:]:
                item.move(item_vel)
                item.draw(WIN)
                   
                if collide(item, player):
                    if item.effect == "heal":
                        player.health +=20
                        items.remove(item)
                        if player.health >= 200:
                            player.health = 200
                    if item.effect == "armor":
                        player.armor_status = 1
                        player.armor = armor
                        items.remove(item)

        if paused:

            WIN.blit(BG_Wait, ((WIDTH - BG_Wait.get_width()) // 2, (HEIGHT - BG_Wait.get_height()) // 2))
            WIN.blit(continue_button_img, continue_button_rect.topleft)
            pygame.display.update()
            pygame.time.wait(1000)

            continue

        else:
            redraw_window()

        pygame.display.flip()
        pygame.display.update()




pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # -1 để lặp lại nhạc nền
def main_menu():

    run = True
    paused = False
    while run:
        WIN.blit(BG_Wait, (0, 0))
        # WIN.blit(title_text, title_rect.topleft)
        WIN.blit(start_button_img, start_button_rect.topleft)
        # WIN.blit(option_button_img, option_button_rect.topleft)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    main(1, 5, 200, 1)

            elif event.type == pygame.KEYDOWN:
                with open("data.txt", "r") as readData:
                    if readData is not None:
                        # Đọc nội dung từ file
                        content = readData.read()
                        cleaned_content = content.replace('(', '').replace(')', '').replace(' ', '')
                        values = cleaned_content.split(',') #cắt dấu ,
                        level, lives, player_health, player_level = map(int, values)
                        print(f"Level: {level}")
                        print(f"Lives: {lives}")
                        print(f"Player Health: {player_health}")
                        print(f"Player Level: {player_level}")
                        main(level, lives, player_health, player_level)
                        readData.close()

        pygame.display.update()
    pygame.quit()


main_menu()
