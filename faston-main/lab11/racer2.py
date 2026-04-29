"""
Practice 11 – Game 1: Racer
Extensions from Practice 8:
  1. Randomly generating coins with different weights on the road
  2. Increase the speed of Enemy when the player earns N coins
  3. Commented code throughout
"""

import pygame
import random
import sys

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
SCREEN_W, SCREEN_H = 480, 700   # Window size in pixels
FPS               = 60          # Frames per second cap

# Road boundaries (the playable lane area)
ROAD_LEFT  = 80
ROAD_RIGHT = 400

# Colours (R, G, B)
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GREY       = (80,  80,  80)
DARK_GREY  = (50,  50,  50)
YELLOW     = (255, 220, 0)
RED        = (220, 40,  40)
BLUE       = (30,  120, 255)
GREEN      = (50,  200, 80)
ORANGE     = (255, 160, 0)
SILVER     = (192, 192, 192)

# Enemy speed‑up settings
COINS_PER_SPEEDUP = 5          # Every 5 coins earned → enemy gets faster
SPEEDUP_AMOUNT    = 0.5        # How many px/frame faster each time

# Coin weight definitions: (label, score_value, colour, spawn_weight)
# spawn_weight controls how often this coin type appears (higher = rarer chance)
COIN_TYPES = [
    {"label": "BRONZE", "value": 1, "colour": (180, 100, 30), "weight": 60},
    {"label": "SILVER", "value": 2, "colour": SILVER,         "weight": 30},
    {"label": "GOLD",   "value": 3, "colour": YELLOW,         "weight": 10},
]

# ──────────────────────────────────────────────
# HELPER – weighted random choice
# ──────────────────────────────────────────────
def weighted_choice(items):
    """Return one item from `items` using its 'weight' key as probability."""
    total   = sum(i["weight"] for i in items)
    roll    = random.randint(1, total)
    running = 0
    for item in items:
        running += item["weight"]
        if roll <= running:
            return item
    return items[-1]  # fallback

# ──────────────────────────────────────────────
# CLASSES
# ──────────────────────────────────────────────

class PlayerCar:
    """The car controlled by the player."""
    WIDTH  = 40
    HEIGHT = 70

    def __init__(self):
        # Start centred on the road
        self.rect  = pygame.Rect(
            (ROAD_LEFT + ROAD_RIGHT) // 2 - self.WIDTH // 2,
            SCREEN_H - self.HEIGHT - 20,
            self.WIDTH, self.HEIGHT
        )
        self.colour = BLUE
        # Instance variable so it can grow when the game speeds up
        self.speed  = 5

    def update(self, keys):
        """Move left/right based on arrow‑key or WASD input."""
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > ROAD_LEFT:
            self.rect.x -= int(self.speed)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < ROAD_RIGHT:
            self.rect.x += int(self.speed)

    def draw(self, surface):
        """Draw the player car as a simple rectangle with details."""
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)
        # Windshield
        wshield = pygame.Rect(self.rect.x + 5, self.rect.y + 8, self.WIDTH - 10, 18)
        pygame.draw.rect(surface, (180, 220, 255), wshield, border_radius=3)
        # Wheels
        for wx, wy in [(self.rect.x - 5, self.rect.y + 8),
                       (self.rect.right - 5, self.rect.y + 8),
                       (self.rect.x - 5, self.rect.bottom - 22),
                       (self.rect.right - 5, self.rect.bottom - 22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 10, 14), border_radius=3)


class EnemyCar:
    """An oncoming enemy car that travels downward."""
    WIDTH  = 40
    HEIGHT = 70

    def __init__(self, base_speed):
        # Random lane position
        self.rect = pygame.Rect(
            random.randint(ROAD_LEFT, ROAD_RIGHT - self.WIDTH),
            -self.HEIGHT,
            self.WIDTH, self.HEIGHT
        )
        self.colour = random.choice([RED, GREEN, ORANGE, (150, 50, 200)])
        # Speed may vary slightly per enemy for variety
        self.speed  = base_speed + random.uniform(-0.3, 0.3)

    def update(self):
        """Move the enemy downward each frame."""
        self.rect.y += self.speed

    def is_off_screen(self):
        """Returns True when the car has passed the bottom of the screen."""
        return self.rect.top > SCREEN_H

    def draw(self, surface):
        """Draw the enemy car."""
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)
        wshield = pygame.Rect(self.rect.x + 5, self.rect.y + 8, self.WIDTH - 10, 18)
        pygame.draw.rect(surface, (255, 230, 180), wshield, border_radius=3)
        for wx, wy in [(self.rect.x - 5, self.rect.y + 8),
                       (self.rect.right - 5, self.rect.y + 8),
                       (self.rect.x - 5, self.rect.bottom - 22),
                       (self.rect.right - 5, self.rect.bottom - 22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 10, 14), border_radius=3)


class Coin:
    """A collectible coin with a weight-based score value."""
    RADIUS = 12

    def __init__(self, speed):
        # Pick a random coin type using weighted probability
        self.ctype  = weighted_choice(COIN_TYPES)
        self.colour = self.ctype["colour"]
        self.value  = self.ctype["value"]   # score awarded on collection
        self.label  = self.ctype["label"]
        self.speed  = speed                 # falls at same speed as enemies
        self.rect   = pygame.Rect(
            random.randint(ROAD_LEFT + self.RADIUS, ROAD_RIGHT - self.RADIUS),
            -self.RADIUS * 2,
            self.RADIUS * 2, self.RADIUS * 2
        )

    def update(self):
        """Move coin downward each frame."""
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > SCREEN_H

    def draw(self, surface):
        """Draw the coin as a filled circle with a small label."""
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(surface, self.colour, (cx, cy), self.RADIUS)
        pygame.draw.circle(surface, BLACK, (cx, cy), self.RADIUS, 2)
        # Print coin value in the centre
        font_s = pygame.font.SysFont("arial", 11, bold=True)
        txt    = font_s.render(str(self.value), True, BLACK)
        surface.blit(txt, txt.get_rect(center=(cx, cy)))


class Road:
    """Scrolling road background."""
    STRIPE_W = 8
    STRIPE_H = 40
    GAP      = 30

    def __init__(self):
        self.offset = 0          # vertical scroll offset
        self.speed  = 4          # matches overall game feel

    def update(self):
        """Scroll the road markings downward."""
        self.offset = (self.offset + self.speed) % (self.STRIPE_H + self.GAP)

    def draw(self, surface):
        # Road surface
        pygame.draw.rect(surface, DARK_GREY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_H))
        # Edge lines
        pygame.draw.line(surface, YELLOW, (ROAD_LEFT, 0),  (ROAD_LEFT, SCREEN_H),  4)
        pygame.draw.line(surface, YELLOW, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_H), 4)
        # Centre dashes
        cx = (ROAD_LEFT + ROAD_RIGHT) // 2
        y  = -self.STRIPE_H + self.offset
        while y < SCREEN_H:
            pygame.draw.rect(surface, WHITE, (cx - self.STRIPE_W // 2, y, self.STRIPE_W, self.STRIPE_H))
            y += self.STRIPE_H + self.GAP


# ──────────────────────────────────────────────
# GAME STATE
# ──────────────────────────────────────────────

class RacerGame:
    """Main game controller."""

    ENEMY_BASE_SPEED  = 3.0   # starting speed for enemies (px/frame)
    SPAWN_ENEMY_EVERY = 90    # frames between enemy spawns
    SPAWN_COIN_EVERY  = 60    # frames between coin spawns

    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Racer – Practice 11")
        self.clock   = pygame.time.Clock()
        self.font    = pygame.font.SysFont("arial", 22, bold=True)
        self.big_font= pygame.font.SysFont("arial", 48, bold=True)
        self.reset()

    def reset(self):
        """Initialise / restart all game variables."""
        self.player       = PlayerCar()
        self.road         = Road()
        self.enemies      = []
        self.coins        = []
        self.score        = 0             # total score from coins
        self.coins_total  = 0             # total coins ever collected
        self.enemy_speed  = self.ENEMY_BASE_SPEED
        self.frame        = 0             # frame counter for spawning
        self.running      = True
        self.game_over    = False
        # Track the last speedup threshold to know when next one fires
        self.next_speedup = COINS_PER_SPEEDUP

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

    # ── Event handling ─────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset()               # restart on R key
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    # ── Update logic ───────────────────────────

    def _update(self):
        self.frame += 1
        keys = pygame.key.get_pressed()

        # Update road scroll
        self.road.update()

        # Update player
        self.player.update(keys)

        # Spawn a new enemy car at regular intervals
        if self.frame % self.SPAWN_ENEMY_EVERY == 0:
            self.enemies.append(EnemyCar(self.enemy_speed))

        # Spawn a new coin at regular intervals
        if self.frame % self.SPAWN_COIN_EVERY == 0:
            self.coins.append(Coin(self.enemy_speed))

        # Update enemies and check collisions
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
            elif self.player.rect.colliderect(enemy.rect):
                # Collision → game over
                self.game_over = True

        # Update coins and check collection
        for coin in self.coins[:]:
            coin.update()
            if coin.is_off_screen():
                self.coins.remove(coin)
            elif self.player.rect.colliderect(coin.rect):
                # Collect coin: add its weighted value to score
                self.score       += coin.value
                self.coins_total += 1
                self.coins.remove(coin)

                # Check whether it's time to increase speed (based on NUMBER of
                # coins collected, not score points — every N coins triggers it)
                if self.coins_total >= self.next_speedup:
                    self.enemy_speed  += SPEEDUP_AMOUNT
                    # Road scroll also speeds up so the player car feels faster too
                    self.road.speed   += SPEEDUP_AMOUNT
                    # Player lateral speed grows slightly so dodging stays fair
                    self.player.speed += 0.3
                    self.next_speedup += COINS_PER_SPEEDUP

    # ── Drawing ────────────────────────────────

    def _draw(self):
        # Background (grass areas)
        self.screen.fill(GREEN)

        # Road and lane markings
        self.road.draw(self.screen)

        # Draw all coins
        for coin in self.coins:
            coin.draw(self.screen)

        # Draw all enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw player on top
        self.player.draw(self.screen)

        # ── HUD ──
        self._draw_hud()

        # ── Game‑over overlay ──
        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self):
        """Draw score, coin count, player speed, and enemy speed in the HUD."""
        # Semi-transparent HUD background
        hud = pygame.Surface((230, 100), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 140))
        self.screen.blit(hud, (5, 5))

        # Coins = number collected (triggers speed-up every N)
        # Score = weighted points total (bronze×1, silver×2, gold×3)
        coins_txt = self.font.render(f"Coins : {self.coins_total}  →  {self.next_speedup}", True, SILVER)
        score_txt = self.font.render(f"Score : {self.score}", True, YELLOW)
        espd_txt  = self.font.render(f"Enemy : {self.enemy_speed:.1f} px/f", True, (255, 100, 100))
        pspd_txt  = self.font.render(f"You   : {self.player.speed:.1f} px/f", True, (100, 200, 255))

        self.screen.blit(coins_txt, (10, 8))
        self.screen.blit(score_txt, (10, 30))
        self.screen.blit(espd_txt,  (10, 52))
        self.screen.blit(pspd_txt,  (10, 74))

        # Coin type legend (bottom-right)
        lx, ly = SCREEN_W - 150, SCREEN_H - 80
        for ct in COIN_TYPES:
            pygame.draw.circle(self.screen, ct["colour"], (lx + 10, ly + 8), 8)
            pygame.draw.circle(self.screen, BLACK,        (lx + 10, ly + 8), 8, 1)
            lbl = self.font.render(f"{ct['label']} +{ct['value']}", True, ct["colour"])
            self.screen.blit(lbl, (lx + 24, ly))
            ly += 24

    def _draw_game_over(self):
        """Overlay showing final score and restart instructions."""
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        go_txt   = self.big_font.render("GAME OVER", True, RED)
        sc_txt   = self.font.render(f"Final Score: {self.score}", True, YELLOW)
        rest_txt = self.font.render("Press  R  to Restart   |   ESC to Quit", True, WHITE)

        self.screen.blit(go_txt,   go_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 50)))
        self.screen.blit(sc_txt,   sc_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 10)))
        self.screen.blit(rest_txt, rest_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 50)))


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    game = RacerGame()
    game.run()