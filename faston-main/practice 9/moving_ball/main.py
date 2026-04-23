import pygame
import sys
from ball import Ball

WIDTH, HEIGHT = 500, 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()

ball = Ball()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -ball.step, WIDTH, HEIGHT)

            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.step, WIDTH, HEIGHT)

            elif event.key == pygame.K_LEFT:
                ball.move(-ball.step, 0, WIDTH, HEIGHT)

            elif event.key == pygame.K_RIGHT:
                ball.move(ball.step, 0, WIDTH, HEIGHT)

    # фон
    screen.fill((255, 255, 255))

    # шар
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(144)