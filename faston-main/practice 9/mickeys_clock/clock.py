import pygame
import sys
from datetime import datetime


WIDTH, HEIGHT = 500, 500
CENTER = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)

MICKEY_PATH = r"C:\Users\Nurali\Documents\nnnp2\pp2\practice 9\mickeys_clock\images\mickeyclock.jpeg"
LEFT_HAND_PATH = r"C:\Users\Nurali\Documents\nnnp2\pp2\practice 9\mickeys_clock\images\m1.png"    
RIGHT_HAND_PATH = r"C:\Users\Nurali\Documents\nnnp2\pp2\practice 9\mickeys_clock\images\m2.png"   

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)


background = pygame.image.load(MICKEY_PATH).convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

right_hand = pygame.image.load(RIGHT_HAND_PATH).convert_alpha()
left_hand = pygame.image.load(LEFT_HAND_PATH).convert_alpha()

# Твои руки на картинках направлены вбок.
# Доворачиваем их так, чтобы в нуле они смотрели вверх (на 12 часов).
right_hand = pygame.transform.rotate(right_hand, 270)    # правая рука -> минуты
left_hand = pygame.transform.rotate(left_hand, 90)     # левая рука -> секунды

# Масштаб под окно
right_hand = pygame.transform.smoothscale(right_hand, (120, 120))
left_hand = pygame.transform.smoothscale(left_hand, (120, 120))

right_hand.set_alpha(255)
left_hand.set_alpha(255)

def blit_rotated(surface, image, angle, center, offset):
    """
    angle — угол в градусах.
    center — центр часов.
    offset — смещение картинки относительно центра часов.
    """
    rotated = pygame.transform.rotozoom(image, -angle, 1)
    rotated_offset = offset.rotate(angle)
    rect = rotated.get_rect(center=center + rotated_offset)
    surface.blit(rotated, rect)
# Эти смещения можно чуть подправить, если руки будут стоять неидеально
minute_offset = pygame.math.Vector2(0, -30)
second_offset = pygame.math.Vector2(0, -35)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # текущее время системы
    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    # углы: минутная и секундная стрелки
    minute_angle = minutes * 6 + seconds * 0.1
    second_angle = seconds * 6

    # рисуем
    screen.blit(background, (0, 0))

    # правая рука = минуты
    blit_rotated(screen, right_hand, minute_angle, CENTER, minute_offset)

    # левая рука = секунды
    blit_rotated(screen, left_hand, second_angle, CENTER, second_offset)

    # текст времени MM:SS
    time_text = font.render(f"{minutes:02}:{seconds:02}", True, (0, 0, 0))
    text_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(time_text, text_rect)

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
sys.exit()