import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 40
PLAYER_SPEED = 5
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve_passages_from(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[cy + dy][cx + dx] = 0
                maze[ny][nx] = 0
                carve_passages_from(nx, ny)

    maze[1][1] = 0
    carve_passages_from(1, 1)
    return maze

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if not self.collide_with_walls(new_rect):
            self.rect = new_rect

    def collide_with_walls(self, rect):
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    wall_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if rect.colliderect(wall_rect):
                        return True
        return False

# Goal class
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Main game function
def game():
    global maze
    clock = pygame.time.Clock()
    running = True

    # Generate random maze
    maze = generate_maze(SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE)

    # Create player and goal
    player = Player(GRID_SIZE, GRID_SIZE)
    goal = Goal(SCREEN_WIDTH - 2 * GRID_SIZE, SCREEN_HEIGHT - 2 * GRID_SIZE)

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP]:
            player.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN]:
            player.move(0, PLAYER_SPEED)

        # Clear screen
        win.fill(BLACK)

        # Draw maze
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(win, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw player and goal
        win.blit(player.image, player.rect)
        win.blit(goal.image, goal.rect)

        # Check if player reaches the goal
        if player.rect.colliderect(goal.rect):
            print("Congratulations! You reached the goal!")
            running = False

        # Update display
        pygame.display.update()

        # Set the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    game()