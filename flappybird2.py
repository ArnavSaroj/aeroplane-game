import pygame
import random

from pygame.time import Clock

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

game_height = 600
game_width = 700

screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Aeroplane Saver")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
font2 = pygame.font.SysFont(None, 25)
background = pygame.image.load(".venv/bgimage.png")
background2 = pygame.transform.scale(background, (game_width, game_height))

pygame.display.update()

class Airplane:
    def __init__(self, y, x, image_paths, width, height):
        self.x = x
        self.y = y
        self.images = [pygame.image.load(img_path) for img_path in image_paths]
        self.images = [pygame.transform.scale(img, (width, height)) for img in self.images]
        self.current_frame = 0
        self.width = width
        self.height = height
        self.animation_speed = 0.1  # Time in seconds for each frame
        self.animation_time = 0

    def draw(self, screen):
        screen.blit(self.images[self.current_frame], (self.x, self.y))

    def move(self, velocity_x, velocity_y):
        self.x += velocity_x
        self.y += velocity_y
        # Clamping
        self.x = max(0, min(self.x, game_width - self.width))
        self.y = max(0, min(self.y, game_height - self.height))

    def update_animation(self, delta_time):
        self.animation_time += delta_time
        if self.animation_time > self.animation_speed:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)


class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def drawrect(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, velocity_x):
        self.rect.x += velocity_x


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])


def screen_text2(textr, color, x, y):
    screen_text = font2.render(textr, True, color)
    screen.blit(screen_text, [x, y])


def welcum():
    running = True
    while running:
        screen.fill(white)
        screen_text2("Welcome to Aeroplane Game!! Press ENTER to continue", red, game_width // 4, game_height // 4)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mainloop()
    clock.tick(30)


def game_over():
    waiting = True
    while waiting:
        screen.fill(red)
        text_screen("GAME OVER!!  Press ENTER to continue", black, game_width // 4, game_height // 4)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    welcum()
    clock.tick(30)


# List of airplane images for animation
airjet1 = Airplane(100, 20, ["bgremovedwingdown1.png", "bgremovedwingstraigth.png", "bgremovedwingup.png"], 100, 60)


def mainloop():
    running = True
    obstacles = []
    obstacle_time = 0
    obstaclevelocity_ = -10
    velocity_x = 0
    velocity_y = 0
    score = 0

    while running:
        delta_time = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    velocity_y = -10
                    velocity_x = 0
                elif event.key == pygame.K_DOWN:
                    velocity_y = 10
                    velocity_x = 0
                elif event.key == pygame.K_RIGHT:
                    velocity_x = 10
                    velocity_y = 0
                elif event.key == pygame.K_LEFT:
                    velocity_x = -10
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
            upper_height = random.randint(70, 150)
            obstacle_gap = random.randint(100, 200)
            lower_height = game_height - upper_height - obstacle_gap

            upper_rect = Rectangle(game_width, 0, 20, upper_height, blue)
            lower_rect = Rectangle(game_width, game_height - lower_height, 20, lower_height, blue)

            obstacles.append(upper_rect)
            obstacles.append(lower_rect)

            obstacle_time = random.randint(25, 40)

        obstacle_time -= 1

        # Remove obstacles that have moved off-screen
        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x > -20]

        # Move the airplane
        airjet1.move(velocity_x, velocity_y)
        airjet1.update_animation(delta_time)

        # Clear the screen and redraw everything
        screen.blit(background2, (0, 0))
        text_screen(f"SCORE={score}", red, 25, 35)

        for obstacle in obstacles:
            if obstacle.rect.x + obstacle.rect.width < airjet1.x:
                score += 10
                obstacle.rect.width = 0

        for obstacle in obstacles:
            obstacle.move(obstaclevelocity_)
            obstacle.drawrect(screen)

        airjet1.draw(screen)

        airplane_rect = pygame.Rect(airjet1.x, airjet1.y, airjet1.width, airjet1.height)

        for obstacle1 in obstacles:
            if airplane_rect.colliderect(obstacle1.rect):
                game_over()

        pygame.display.update()

    pygame.quit()

welcum()
