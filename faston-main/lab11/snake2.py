"""
Practice 11 – Game 2: Snake
Extensions from Practice 8:
  1. Randomly generating food with different weights (values)
  2. Foods which disappear after a timer
  3. Commented code throughout
"""

import pygame
import random
import sys

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
CELL        = 20           # Size of each grid cell in pixels
COLS        = 30           # Number of columns in the grid
ROWS        = 28           # Number of rows (play area)
SCREEN_W    = COLS * CELL  # 600
SCREEN_H    = ROWS * CELL + 50  # +50 for HUD strip at top
HUD_H       = 50           # Height of the score bar at top
FPS         = 10           # Snake moves this many times per second

# Direction vectors
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

# Colours (R, G, B)
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
BG          = (30,  30,  30)    # grid background
GRID_LINE   = (45,  45,  45)    # subtle grid lines
SNAKE_HEAD  = (0,   210, 80)    # bright green head
SNAKE_BODY  = (0,   160, 60)    # darker green body
SNAKE_EYE   = (255, 255, 255)
RED         = (220, 50,  50)
YELLOW      = (255, 220, 0)
ORANGE      = (255, 140, 0)
PURPLE      = (180, 60,  200)
SILVER      = (192, 192, 192)

# ──────────────────────────────────────────────
# FOOD TYPES
# Each entry: label, score value, colour, spawn weight, lifetime (frames)
# Lower lifetime → food disappears faster
# ──────────────────────────────────────────────
FOOD_TYPES = [
    {"label": "Apple",   "value": 1, "colour": RED,    "weight": 50, "lifetime": None },  # never disappears
    {"label": "Orange",  "value": 2, "colour": ORANGE, "weight": 30, "lifetime": 50   },  # ~5 s at FPS 10
    {"label": "Grape",   "value": 3, "colour": PURPLE, "weight": 15, "lifetime": 30   },  # ~3 s
    {"label": "Star",    "value": 5, "colour": YELLOW, "weight": 5,  "lifetime": 20   },  # ~2 s (rare!)
]

MAX_FOOD_ON_SCREEN = 4    # Maximum simultaneous food items

# ──────────────────────────────────────────────
# HELPER – weighted random choice
# ──────────────────────────────────────────────
def weighted_choice(items):
    """Select an item from `items` list proportionally by its 'weight' key."""
    total   = sum(i["weight"] for i in items)
    roll    = random.randint(1, total)
    running = 0
    for item in items:
        running += item["weight"]
        if roll <= running:
            return item
    return items[-1]

# ──────────────────────────────────────────────
# CLASSES
# ──────────────────────────────────────────────

class Food:
    """A single food item with a score value and optional disappear timer."""

    def __init__(self, occupied_cells):
        """
        Spawn at a random unoccupied grid cell.
        `occupied_cells` – set of (col, row) tuples already in use.
        """
        # Pick food type via weighted random
        ftype         = weighted_choice(FOOD_TYPES)
        self.label    = ftype["label"]
        self.value    = ftype["value"]
        self.colour   = ftype["colour"]
        self.lifetime = ftype["lifetime"]   # None = immortal
        self.age      = 0                   # frames alive

        # Find a free grid cell
        all_cells = {(c, r) for c in range(COLS) for r in range(ROWS)}
        free_cells = list(all_cells - occupied_cells)
        self.pos  = random.choice(free_cells) if free_cells else (COLS // 2, ROWS // 2)

    def update(self):
        """Increment age. Returns True if the food should be removed (expired)."""
        if self.lifetime is not None:
            self.age += 1
            return self.age >= self.lifetime
        return False

    def time_fraction(self):
        """Return fraction of lifetime remaining (1.0 = fresh, 0.0 = about to vanish). None if immortal."""
        if self.lifetime is None:
            return None
        return max(0.0, 1.0 - self.age / self.lifetime)

    def draw(self, surface):
        """Draw food as a coloured circle; fades when nearly expired."""
        col, row = self.pos
        # Pixel position of the cell centre
        px = col * CELL + CELL // 2
        py = row * CELL + CELL // 2 + HUD_H

        # Alpha fading for timed food
        fraction = self.time_fraction()
        if fraction is not None:
            # Create a temporary surface for alpha blending
            surf = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
            alpha = int(80 + 175 * fraction)   # fades from 255 → 80
            r, g, b = self.colour
            pygame.draw.circle(surf, (r, g, b, alpha), (CELL // 2, CELL // 2), CELL // 2 - 2)
            surface.blit(surf, (col * CELL, row * CELL + HUD_H))
            # Timer ring around timed food to show urgency
            ring_colour = (255, 255, 255, alpha)
            pygame.draw.circle(surface, (*WHITE, alpha), (px, py), CELL // 2 - 1, 2)
        else:
            pygame.draw.circle(surface, self.colour, (px, py), CELL // 2 - 2)

        # Show score value on the food
        font_s = pygame.font.SysFont("arial", 11, bold=True)
        txt    = font_s.render(str(self.value), True, WHITE if self.colour != YELLOW else BLACK)
        surface.blit(txt, txt.get_rect(center=(px, py)))


class Snake:
    """The player-controlled snake."""

    def __init__(self):
        # Start in the middle, 3 segments long, facing RIGHT
        mid_col, mid_row = COLS // 2, ROWS // 2
        self.body      = [(mid_col - i, mid_row) for i in range(3)]   # head first
        self.direction = RIGHT
        self.grew      = False   # flag: True when the snake just ate food

    def change_direction(self, new_dir):
        """
        Change direction unless the new direction is directly opposite
        (that would instantly collide with the neck segment).
        """
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.direction = new_dir

    def move(self):
        """Advance the snake one cell in the current direction."""
        head       = self.body[0]
        new_head   = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)   # grow head
        if not self.grew:
            self.body.pop()             # remove tail if we didn't eat
        else:
            self.grew = False           # reset flag

    def head(self):
        return self.body[0]

    def is_dead(self):
        """Check wall collision or self-collision."""
        hx, hy = self.head()
        # Hit a wall
        if not (0 <= hx < COLS and 0 <= hy < ROWS):
            return True
        # Hit its own body (skip head itself)
        if self.head() in self.body[1:]:
            return True
        return False

    def occupied_cells(self):
        """Return set of (col, row) occupied by the snake."""
        return set(self.body)

    def draw(self, surface):
        """Draw every segment; head gets eyes."""
        for i, (col, row) in enumerate(self.body):
            px = col * CELL
            py = row * CELL + HUD_H
            colour = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(surface, colour, (px + 1, py + 1, CELL - 2, CELL - 2), border_radius=4)

        # Eyes on the head
        hx, hy = self.body[0]
        cx = hx * CELL + CELL // 2
        cy = hy * CELL + CELL // 2 + HUD_H
        dx, dy = self.direction
        # Offset eyes perpendicular to direction of travel
        perp = (-dy, dx)
        for side in (+1, -1):
            ex = cx + dx * 4 + perp[0] * side * 4
            ey = cy + dy * 4 + perp[1] * side * 4
            pygame.draw.circle(surface, SNAKE_EYE, (ex, ey), 3)
            pygame.draw.circle(surface, BLACK,     (ex + dx, ey + dy), 1)


# ──────────────────────────────────────────────
# GAME STATE
# ──────────────────────────────────────────────

class SnakeGame:
    """Main game controller for Snake."""

    FOOD_SPAWN_INTERVAL = 25   # frames between food spawn attempts

    def __init__(self):
        pygame.init()
        self.screen   = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Snake – Practice 11")
        self.clock    = pygame.time.Clock()
        self.font     = pygame.font.SysFont("arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.reset()

    def reset(self):
        """Re‑initialise everything for a new game."""
        self.snake     = Snake()
        self.foods     = []          # list of Food objects
        self.score     = 0
        self.frame     = 0
        self.game_over = False
        self.running   = True
        # Spawn the first food immediately
        self._try_spawn_food()

    # ── Main loop ──────────────────────────────

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            if not self.game_over:
                self._update()
            self._draw()
        pygame.quit()
        sys.exit()

    # ── Events ─────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if   event.key in (pygame.K_UP,    pygame.K_w): self.snake.change_direction(UP)
                elif event.key in (pygame.K_DOWN,  pygame.K_s): self.snake.change_direction(DOWN)
                elif event.key in (pygame.K_LEFT,  pygame.K_a): self.snake.change_direction(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d): self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_r and self.game_over: self.reset()
                elif event.key == pygame.K_ESCAPE: self.running = False

    # ── Update ─────────────────────────────────

    def _update(self):
        self.frame += 1

        # Move the snake one step
        self.snake.move()

        # Check if snake died
        if self.snake.is_dead():
            self.game_over = True
            return

        # Check whether snake head lands on any food
        head = self.snake.head()
        for food in self.foods[:]:
            if food.pos == head:
                self.score     += food.value   # weighted score
                self.snake.grew = True         # grow snake on next move
                self.foods.remove(food)

        # Update food timers; remove expired timed food
        for food in self.foods[:]:
            expired = food.update()
            if expired:
                self.foods.remove(food)

        # Periodically try to spawn new food (up to max limit)
        if self.frame % self.FOOD_SPAWN_INTERVAL == 0:
            self._try_spawn_food()

    def _try_spawn_food(self):
        """Spawn a new food item if there's room on screen."""
        if len(self.foods) < MAX_FOOD_ON_SCREEN:
            occupied = self.snake.occupied_cells() | {f.pos for f in self.foods}
            self.foods.append(Food(occupied))

    # ── Draw ───────────────────────────────────

    def _draw(self):
        self.screen.fill(BG)

        # Draw faint grid lines for visibility
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(self.screen, GRID_LINE,
                                 (c * CELL, r * CELL + HUD_H, CELL, CELL), 1)

        # Draw food items
        for food in self.foods:
            food.draw(self.screen)

        # Draw snake
        self.snake.draw(self.screen)

        # HUD
        self._draw_hud()

        # Food legend on right side
        self._draw_legend()

        # Game‑over overlay
        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self):
        """Top status bar with score and snake length."""
        pygame.draw.rect(self.screen, (20, 20, 20), (0, 0, SCREEN_W, HUD_H))
        pygame.draw.line(self.screen, YELLOW, (0, HUD_H), (SCREEN_W, HUD_H), 2)

        score_txt  = self.font.render(f"Score: {self.score}", True, YELLOW)
        length_txt = self.font.render(f"Length: {len(self.snake.body)}", True, WHITE)
        ctrl_txt   = self.small_font.render("Arrows / WASD to move  |  R = restart  |  ESC = quit", True, SILVER)

        self.screen.blit(score_txt,  (10, 12))
        self.screen.blit(length_txt, (200, 12))
        self.screen.blit(ctrl_txt,   (10, HUD_H - 16))

    def _draw_legend(self):
        """Food type legend on the right side of the HUD."""
        x = SCREEN_W - 195
        pygame.draw.rect(self.screen, (20, 20, 20), (x - 5, 0, 200, HUD_H - 18))
        for i, ft in enumerate(FOOD_TYPES):
            lx = x + (i % 2) * 95
            ly = 6 + (i // 2) * 18
            pygame.draw.circle(self.screen, ft["colour"], (lx + 7, ly + 7), 7)
            label = f"{ft['label']} +{ft['value']}"
            if ft["lifetime"]:
                label += f" {ft['lifetime']}f"
            txt = self.small_font.render(label, True, ft["colour"])
            self.screen.blit(txt, (lx + 18, ly))

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        go   = self.big_font.render("GAME OVER", True, RED)
        sc   = self.font.render(f"Score: {self.score}  |  Length: {len(self.snake.body)}", True, YELLOW)
        rst  = self.font.render("Press  R  to Restart   |   ESC to Quit", True, WHITE)

        cx = SCREEN_W // 2
        cy = SCREEN_H // 2
        self.screen.blit(go,  go.get_rect(center=(cx, cy - 50)))
        self.screen.blit(sc,  sc.get_rect(center=(cx, cy + 10)))
        self.screen.blit(rst, rst.get_rect(center=(cx, cy + 50)))


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    game = SnakeGame()
    game.run()