import pygame 
import os
import time
import random
from pygame.locals import *
pygame.font.init()

WIDTH, HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Empire Invaders")

# def centerElement(element):
#     return WIDTH // 2 - element.get_width() // 2

# Load images
BOBA = pygame.transform.scale(pygame.image.load("assets/boba.png"), (60, 60))
BOMBER = pygame.transform.scale(pygame.image.load("assets/bomber.png"), (60, 60))
TIE = pygame.transform.scale(pygame.image.load("assets/tie.png"), (40, 40))
STAR_DESTROYER = pygame.transform.scale(pygame.image.load("assets/starDestroyer.png"), (680, 158))
# Main character
ANAKIN = pygame.transform.scale(pygame.image.load("assets/anakin.png"), (60, 60))

# Lasers
RED_LASER = pygame.transform.scale(pygame.image.load("assets/redlaser.png"), (5, 15)) # Millenium falcon
STARFIGHTER_LASER = pygame.transform.scale(pygame.image.load("assets/laserStarfighter.png"), (5, 15)) # Anakin - Obi Wan
TIE_LASER = pygame.transform.scale(pygame.image.load("assets/laserTie.png"), (5, 15)) # Tie 
XWING_LASER = pygame.transform.scale(pygame.image.load("assets/laserXwing.png"), (5, 15)) # X-Wing
BOMBER_LASER = pygame.transform.scale(pygame.image.load("assets/laserBomber.png"), (5, 15))
STAR_DESTROYER_LASER = pygame.transform.scale(pygame.image.load("assets/greenlaser.png"), (5, 15))

# Background
BACKGROUND = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x 
        self.y = y 
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel 
    
    def offscreen(self, height):
        return self.y < height and self.y >= 0

    def collision(self, object):
        return collide(object, self)

def collide(obj1, obj2):
    pass

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.lasers_image = None
        self.lasers = []
        self.cooldown_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = ANAKIN
        self.lasers_image = STARFIGHTER_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health 

class Enemy(Ship):
    TYPE_MAP = {
        "boba": (BOBA, RED_LASER, 100),
        "bomber": (BOMBER, BOMBER_LASER, 200),
        "tie": (TIE, TIE_LASER, 150)
    }

    def __init__(self, x, y, type, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.lasers_image, self.max_health = self.TYPE_MAP[type]
        self.mask = pygame.mask.from_surface(self.ship_image)
    def move(self, vel):
        self.y += vel

class Star_Destroyer(Ship):
    def __init__(self, x=10, y=10, health=1000):
        super().__init__(x, y, health)
        self.ship_image = STAR_DESTROYER
        self.lasers_image = STARFIGHTER_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health 

def main():
    run = True  
    FPS = 60
    velocity = 4
    level = 0
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 35)
    lost_font = pygame.font.SysFont("comicsans", 50)

    player = Player(300, 600)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    lost = False
    lost_count = 0

    def redraw_window():
        WINDOW.blit(BACKGROUND, (0,0))  
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 0))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        if level == 50:
            sd = Star_Destroyer()
            sd.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("Long live the Empire.", 1, (255, 0, 0))
            WINDOW.blit(lost_label, (WIDTH//2 - lost_label.get_width() // 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
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
                if level <= 10:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), "tie")
                    enemies.append(enemy)
                else:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["boba", "bomber", "tie", "tie", "tie", "tie"]))
                    enemies.append(enemy)
            if level % 5 == 0:
                boba = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), "boba")
                enemies.append(boba)
            if level % 3 == 0:
                bomber = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), "bomber")
                enemies.append(bomber)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - velocity > 0:
            player.x -= velocity
        if keys[pygame.K_RIGHT] and player.x + velocity + player.get_width() < WIDTH:
            player.x += velocity
        if keys[pygame.K_UP] and player.y - velocity > 0:
            player.y -= velocity
        if keys[pygame.K_DOWN] and player.y + velocity + player.get_height() < HEIGHT:
            player.y += velocity
        
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
    
main()