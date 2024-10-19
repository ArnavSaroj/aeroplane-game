import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

game_height = 600
game_width = 700

screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Aeroplane Saver")
clock = pygame.time.Clock()

# Airplane class
class Airplane:
    def __init__(self, x, y, image_path, width, height):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, velocity_x, velocity_y):
        self.x += velocity_x
        self.y += velocity_y

# Rectangle obstacle class
class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, velocity_x):
        self.rect.x += velocity_x  # Move the rectangle leftward

# Initialize airplane and obstacles
airjet1 = Airplane(100, 20, ".venv/airplane1.jpg", 100, 60)
obstacles = []
obstacle_velocity = -5  # Obstacles move leftward

# Game variables
running = True
velocity_x = 0
velocity_y = 0
obstacle_timer = 0

# Game loop
while running:
    screen.fill(white)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity_y = -5
            elif event.key == pygame.K_DOWN:
                velocity_y = 5
            elif event.key == pygame.K_RIGHT:
                velocity_x = 5
            elif event.key == pygame.K_LEFT:
                velocity_x = -5
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                velocity_y = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                velocity_x = 0

    # Move the airplane
    airjet1.move(velocity_x, velocity_y)

    # Randomly generate new obstacles
    if obstacle_timer == 0:
        height_upper = random.randint(50, 200)  # Random height for the upper block
        height_gap = random.randint(150, 250)   # Random gap between the two blocks
        height_lower = game_height - height_upper - height_gap  # Height for the lower block

        upper_block = Rectangle(game_width, 0, 20, height_upper, blue)
        lower_block = Rectangle(game_width, game_height - height_lower, 20, height_lower, blue)
        obstacles.append(upper_block)
        obstacles.append(lower_block)

        obstacle_timer = random.randint(90, 120)  # Random time interval between obstacles

    obstacle_timer -= 1

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle.move(obstacle_velocity)
        obstacle.draw(screen)

    # Remove obstacles that have moved off-screen
    obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x > -20]

    # Draw the airplane
    airjet1.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
