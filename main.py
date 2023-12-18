import pygame
import os
import time
import random
from Enemy import Enemy
from Laser import Laser
from Player import Player
from Ship import Ship
from Item import Item
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


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




def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

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
                        values = cleaned_content.split(',')
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
