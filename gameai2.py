import pygame
import random
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

game_height = 600
game_width = 700

screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("aeroplane saver")
clock = pygame.time.Clock()

class airplane:
    def __init__(self, y, x, image_path, width, height):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, velocity_x, velocity_y):
        self.x += velocity_x
        self.y += velocity_y

class rectangle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def drawrect(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, velocity_x):
        self.rect.x += velocity_x

obstacles = []

airjet1 = airplane(100, 20, ".venv/airplane1.jpg", 100, 60)

running = True
obstacle_time = 0
obstaclevelocity_ = -5
velocity_x = 0
velocity_y = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity_y = -5
                velocity_x = 0
            elif event.key == pygame.K_DOWN:
                velocity_y = 5
                velocity_x = 0
            elif event.key == pygame.K_RIGHT:
                velocity_x = 5
                velocity_y = 0
            elif event.key == pygame.K_LEFT:
                velocity_x = -5
                velocity_y = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                velocity_y = 0
            if event.key == pygame.K_UP:
                velocity_y = 0
            if event.key == pygame.K_LEFT:
                velocity_x = 0
            if event.key == pygame.K_RIGHT:
                velocity_x = 0

    if obstacle_time == 0:
        upper_height = random.randint(45, 175)
        obstacle_gap = random.randint(200, 300)
        lower_height = game_height - upper_height - obstacle_gap

        upper_rect = rectangle(game_width, 0, 20, upper_height, blue)
        lower_rect = rectangle(game_width, game_height - lower_height, 20, lower_height, blue)

        obstacles.append(upper_rect)
        obstacles.append(lower_rect)

        obstacle_time = random.randint(70, 100)
        print(f"New obstacles added: upper_height={upper_height}, lower_height={lower_height}")

    obstacle_time -= 1

    # Move and draw obstacles
    screen.fill(white)  # Fill screen with white before drawing obstacles
    for obstacle in obstacles:
        obstacle.move(obstaclevelocity_)
        obstacle.drawrect(screen)

    # Remove obstacles that have moved off-screen
    obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x > -20]

    # Move the airplane
    airjet1.move(velocity_x, velocity_y)

    # Draw the airplane last
    airjet1.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
