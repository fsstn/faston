"""
Practice 10 – Game 2: Snake
Classic Snake with:
  • Wall (border) collision detection
  • Food placed randomly (never on the snake)
  • Level system – every FOODS_PER_LEVEL foods the level rises
  • Speed increases with each level
  • HUD showing score and level
"""

import pygame
import random
import sys

pygame.init()

# ── Grid & screen constants ───────────────────────────────────────────────────
CELL       = 20          # pixels per grid cell
COLS, ROWS = 30, 25      # grid dimensions
HUD_H      = 50          # header bar height (for score / level)

SCREEN_W = CELL * COLS
SCREEN_H = CELL * ROWS + HUD_H

BASE_FPS        = 8      # snake moves per second at level 1
FPS_PER_LEVEL   = 2      # extra moves/s gained each level
FOODS_PER_LEVEL = 3      # foods needed to advance one level

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK    = (0,   0,   0  )
WHITE    = (255, 255, 255)
DKGREEN  = (0,   140, 0  )
GREEN    = (50,  200, 50 )
RED      = (220, 40,  40 )
YELLOW   = (255, 215, 0  )
GRAY     = (30,  30,  30 )
LT_GRAY  = (60,  60,  60 )
GOLD     = (255, 200, 0  )
BLUE     = (60,  120, 220)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 22, bold=True)
big    = pygame.font.SysFont("Arial", 44, bold=True)

# Cardinal directions as (dx, dy) tuples
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


# ── Food placement helper ─────────────────────────────────────────────────────
def random_food(occupied: set) -> tuple:
    """
    Return a grid cell (col, row) that is not in 'occupied'
    and is not on the border wall.
    """
    while True:
        c = random.randint(1, COLS - 2)
        r = random.randint(1, ROWS - 2)
        if (c, r) not in occupied:
            return (c, r)


# ── Snake class ───────────────────────────────────────────────────────────────
class Snake:
    def __init__(self):
        # Start in the middle of the grid, 3 cells long, moving right
        cx, cy = COLS // 2, ROWS // 2
        self.body      = [(cx, cy), (cx-1, cy), (cx-2, cy)]
        self.direction = RIGHT
        self._queued   = RIGHT    # direction queued from keyboard input
        self._grow     = False    # flag: eat food → grow next move

    # ── Input ─────────────────────────────────────────────────────────────────
    def queue_direction(self, new_dir: tuple):
        """Accept a new direction only if it is not the exact opposite."""
        if new_dir != OPPOSITE.get(self.direction):
            self._queued = new_dir

    # ── Movement ──────────────────────────────────────────────────────────────
    def move(self):
        self.direction = self._queued
        hx, hy = self.body[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])
        self.body.insert(0, new_head)
        if self._grow:
            self._grow = False   # don't remove tail → snake gets longer
        else:
            self.body.pop()

    def eat(self):
        """Call when the head overlaps the food cell."""
        self._grow = True

    # ── Collision checks ──────────────────────────────────────────────────────
    def hit_wall(self) -> bool:
        """True if the head is outside the grid boundaries."""
        hx, hy = self.body[0]
        return not (0 <= hx < COLS and 0 <= hy < ROWS)

    def hit_self(self) -> bool:
        """True if the head overlaps any part of the body."""
        return self.body[0] in self.body[1:]

    # ── Drawing ───────────────────────────────────────────────────────────────
    def draw(self, surface):
        for i, (c, r) in enumerate(self.body):
            x = c * CELL
            y = r * CELL + HUD_H
            col = DKGREEN if i == 0 else GREEN
            pygame.draw.rect(surface, col,
                             (x + 2, y + 2, CELL - 4, CELL - 4),
                             border_radius=4)
            # Eyes on the head segment
            if i == 0:
                pygame.draw.circle(surface, WHITE, (x + 5,  y + 6), 3)
                pygame.draw.circle(surface, WHITE, (x + 14, y + 6), 3)
                pygame.draw.circle(surface, BLACK, (x + 5,  y + 6), 1)
                pygame.draw.circle(surface, BLACK, (x + 14, y + 6), 1)

    @property
    def cells(self) -> set:
        return set(self.body)


# ── Food class ────────────────────────────────────────────────────────────────
class Food:
    def __init__(self, occupied: set):
        self.pos = random_food(occupied)   # (col, row)

    def draw(self, surface):
        c, r = self.pos
        cx = c * CELL + CELL // 2
        cy = r * CELL + CELL // 2 + HUD_H
        pygame.draw.circle(surface, RED,  (cx, cy), CELL // 2 - 2)
        # Small shine dot
        pygame.draw.circle(surface, (255, 120, 120), (cx - 3, cy - 3), 3)


# ── HUD and overlay helpers ───────────────────────────────────────────────────
def draw_hud(surface, score: int, level: int, foods_this_level: int):
    """Top bar: score (left), level (centre), foods until next level (right)."""
    pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_W, HUD_H))
    pygame.draw.line(surface, LT_GRAY, (0, HUD_H), (SCREEN_W, HUD_H), 2)

    sc  = font.render(f"Score: {score}", True, WHITE)
    lv  = font.render(f"Level {level}",  True, GOLD)
    nxt = font.render(f"Next ↑: {FOODS_PER_LEVEL - foods_this_level % FOODS_PER_LEVEL}",
                      True, GREEN)
    surface.blit(sc,  (12, HUD_H//2 - sc.get_height()//2))
    surface.blit(lv,  (SCREEN_W//2 - lv.get_width()//2, HUD_H//2 - lv.get_height()//2))
    surface.blit(nxt, (SCREEN_W - nxt.get_width() - 12, HUD_H//2 - nxt.get_height()//2))


def draw_border(surface):
    """Draw the border 'wall' that kills the snake on collision."""
    pygame.draw.rect(surface, LT_GRAY,
                     (0, HUD_H, SCREEN_W, CELL * ROWS), 2)


def draw_overlay(surface, title: str, sub: str = ""):
    """Semi-transparent pause / game-over overlay."""
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    t = big.render(title, True, WHITE)
    surface.blit(t, (SCREEN_W//2 - t.get_width()//2, SCREEN_H//2 - 70))

    if sub:
        s = font.render(sub, True, YELLOW)
        surface.blit(s, (SCREEN_W//2 - s.get_width()//2, SCREEN_H//2))

    hint = font.render("R – restart   Q – quit", True, (180, 180, 180))
    surface.blit(hint, (SCREEN_W//2 - hint.get_width()//2, SCREEN_H//2 + 50))


# ── Main game loop ────────────────────────────────────────────────────────────
def main():
    snake = Snake()
    food  = Food(snake.cells)

    score             = 0
    level             = 1
    total_foods_eaten = 0        # cumulative; used to compute level
    current_fps       = BASE_FPS

    game_over = False

    while True:
        clock.tick(current_fps)

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r: main(); return
                    if event.key == pygame.K_q: pygame.quit(); sys.exit()
                else:
                    # Map arrow keys / WASD to directions
                    if event.key in (pygame.K_UP,    pygame.K_w): snake.queue_direction(UP)
                    if event.key in (pygame.K_DOWN,  pygame.K_s): snake.queue_direction(DOWN)
                    if event.key in (pygame.K_LEFT,  pygame.K_a): snake.queue_direction(LEFT)
                    if event.key in (pygame.K_RIGHT, pygame.K_d): snake.queue_direction(RIGHT)

        # ── Update ────────────────────────────────────────────────────────────
        if not game_over:
            snake.move()

            # Check wall collision (border of the grid)
            if snake.hit_wall():
                game_over = True

            # Check self collision
            elif snake.hit_self():
                game_over = True

            # Check food eaten
            elif snake.body[0] == food.pos:
                snake.eat()
                total_foods_eaten += 1
                score += 10 * level       # more points for higher levels

                # Level-up logic
                new_level = total_foods_eaten // FOODS_PER_LEVEL + 1
                if new_level > level:
                    level       = new_level
                    current_fps = BASE_FPS + (level - 1) * FPS_PER_LEVEL

                # Spawn new food not overlapping the snake
                food = Food(snake.cells)

        # ── Draw ──────────────────────────────────────────────────────────────
        screen.fill(BLACK)
        draw_hud(screen, score, level,
                 total_foods_eaten % FOODS_PER_LEVEL if total_foods_eaten else 0)

        # Draw faint grid lines inside the playing area
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(screen, (20, 20, 20),
                                 (c * CELL, r * CELL + HUD_H, CELL, CELL), 1)

        draw_border(screen)
        food.draw(screen)
        snake.draw(screen)

        if game_over:
            draw_overlay(screen, "GAME OVER",
                         f"Score: {score}   Level: {level}")

        pygame.display.flip()


if __name__ == "__main__":
    main()