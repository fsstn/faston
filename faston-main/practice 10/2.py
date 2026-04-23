import pygame
import random
import sys
import psycopg2

# ==== PostgreSQL Setup ====
conn = psycopg2.connect(
    host="localhost",
    database="phonebook",
    user="postgres",
    port="5432",
    password="abilkosha"
)
cur = conn.cursor()

def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS "User" (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS user_score (
        score_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES "User"(user_id),
        level INT NOT NULL,
        score INT NOT NULL
    );
    """)
    conn.commit()

def get_user_id(username):
    cur.execute("SELECT user_id FROM \"User\" WHERE username = %s", (username,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        cur.execute("INSERT INTO \"User\" (username) VALUES (%s) RETURNING user_id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

def insert_user_score(user_id, level, score):
    cur.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
    conn.commit()

def show_current_level(username):
    cur.execute("""
    SELECT level FROM user_score 
    INNER JOIN "User" ON user_score.user_id = "User".user_id 
    WHERE "User".username = %s ORDER BY score_id DESC LIMIT 1
    """, (username,))
    row = cur.fetchone()
    if row:
        print(f"Welcome back, {username}! Your current level is: {row[0]}")
    else:
        print(f"Welcome, {username}! New player.")

# ==== Pygame Setup ====
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 100)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# ==== Classes ====
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.alive = True

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        if not self.alive:
            return
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
            new_head in self.positions):
            self.alive = False
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.__init__()

    def draw(self, surface):
        for segment in self.positions:
            pygame.draw.rect(surface, self.color,
                             pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE,
                             pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE), 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.value = 1
        self.spawn_time = pygame.time.get_ticks()
        self.disappear_time = 5000
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake_positions:
                self.position = new_position
                break
        self.value = random.randint(1, 3)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, snake_positions):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.disappear_time:
            self.randomize_position(snake_positions)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE,
                         pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 1)

# ==== Helpers ====
def draw_text(surface, text, x, y, size=36, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def game_over_screen(score, level, user_id):
    screen.fill(DARK_BLUE)
    draw_text(screen, "You DIED", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 50, WHITE)
    draw_text(screen, f"YOUR SCORE: {score}", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 40, WHITE)
    draw_text(screen, "     Press SPACE to restart or ESC to exit",
              SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 30, WHITE)
    pygame.display.update()

    insert_user_score(user_id, level, score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    conn.close()
                    sys.exit()

# ==== Main Game Loop ====
def game_loop(username):
    user_id = get_user_id(username)
    while True:
        snake = Snake()
        food = Food()
        score = 0
        level = 1
        clock = pygame.time.Clock()

        while snake.alive:
            screen.fill(BLACK)
            snake.handle_keys()
            snake.move()

            if snake.get_head_position() == food.position:
                snake.length += 1
                score += food.value
                food.randomize_position(snake.positions)
                if score % 3 == 0:
                    level += 1

            food.update(snake.positions)
            snake.draw(screen)
            food.draw(screen)

            draw_text(screen, f"Score: {score}", 10, 10)
            draw_text(screen, f"Level: {level}", 10, 40)
            draw_text(screen, f"Food Value: {food.value}", 10, 70)

            pygame.display.update()
            clock.tick(8 + level)

        game_over_screen(score, level, user_id)

# ==== Entry Point ====
def main():
    create_tables()
    username = input("Enter your username: ")
    show_current_level(username)
    game_loop(username)

if __name__ == "__main__":
    main()