import pygame
import random
import os

# the x-coordinates for the three lanes cars can be in
LANES = [200, 300, 400] 
SPEED_BASE = 5

def load_image(name, width, height):
    # helper to load an image and scale it, with a fallback color if it's missing
    path = os.path.join('assets', 'images', name)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except FileNotFoundError:
        surf = pygame.Surface((width, height))
        surf.fill((255, 0, 255)) 
        return surf

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        # set up the player's car
        super().__init__()
        filename = f"player_{color_name}.png"
        self.image = load_image(filename, 40, 70)
        self.rect = self.image.get_rect(center=(300, 500))
        self.speed = 6
        self.shield_active = False
        self.nitro_active = False
        self.powerup_timer = 0
        self.crashes_allowed = 0

    def update(self):
        # handle player movement with arrow keys
        keys = pygame.key.get_pressed()
        current_speed = self.speed * 1.5 if self.nitro_active else self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.right < 450:
            self.rect.x += current_speed

        # check if powerups have expired
        if (self.nitro_active or self.shield_active) and pygame.time.get_ticks() > self.powerup_timer:
            self.nitro_active = False
            self.shield_active = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        # set up an enemy car in a random lane
        super().__init__()
        self.image = load_image("enemy.png", 40, 70)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        self.speed = SPEED_BASE + (2 if difficulty == "hard" else 0)

    def update(self):
        # move the enemy down and kill it if it goes off screen
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        # set up an obstacle in a random lane
        super().__init__()
        self.image = load_image("obstacle.png", 40, 40)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        # move the obstacle down and kill it if it goes off screen
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        # create a random powerup (nitro, shield, or repair)
        super().__init__()
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        img_name = self.type.lower() + ".png"
        self.image = load_image(img_name, 30, 30)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        # move the powerup down and kill it if it goes off screen
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()