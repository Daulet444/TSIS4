# simple_snake.py - Pure Snake Game
import pygame
import random
import sys

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_SIZE = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE//2, GRID_SIZE//2)]
        self.direction = (1, 0)
        self.grow = False
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
    def eat(self):
        self.grow = True
        
    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.position = self.get_random_position(snake_body)
        
    def get_random_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if pos not in snake_body:
                return pos

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    screen.fill(BLACK)
    text1 = font.render("GAME OVER", True, RED)
    text2 = font.render(f"Score: {score}", True, WHITE)
    text3 = font.render("Press R to restart or Q to quit", True, WHITE)
    
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 20))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 20))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0
    speed = 10
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
        
        # Move snake
        snake.move()
        
        # Check collision
        if snake.check_collision():
            if game_over_screen(score):
                # Restart game
                snake = Snake()
                food = Food(snake.body)
                score = 0
                speed = 7
            else:
                running = False
            continue
        
        # Eat food
        if snake.body[0] == food.position:
            snake.eat()
            score += 10
            food = Food(snake.body)
            # Increase speed every 50 points
            if score % 50 == 0:
                speed += 2
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        
        # Draw food
        pygame.draw.rect(screen, RED, (food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        show_score(score)
        pygame.display.flip()
        
        # Control speed
        clock.tick(speed)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()