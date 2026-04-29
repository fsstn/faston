import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()
    
    # Square window to match the clock face
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Mouse Clock")
    
    clock_app = MickeyClock(WIDTH, HEIGHT)
    timer = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock_app.render(screen)
        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()