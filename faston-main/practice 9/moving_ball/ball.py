import pygame

class Ball:
    def __init__(self):
        self.radius = 25
        self.x = 250
        self.y = 250
        self.step = 20

    def move(self, dx, dy, width, height):
        new_x = self.x + dx
        new_y = self.y + dy

        # проверка границ
        if new_x - self.radius >= 0 and new_x + self.radius <= width:
            self.x = new_x

        if new_y - self.radius >= 0 and new_y + self.radius <= height:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)