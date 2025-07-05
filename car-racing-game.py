# Car Racing Game
# Author: Vinay
# Email: vinay.nani919@gmail.com

import pygame
import random
import os
from time import sleep
from pathlib import Path

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ROAD_WIDTH = 360
CAR_WIDTH, CAR_HEIGHT = 49, 100
ENEMY_COUNT = 3
SCORE_INCREMENT = 1
FONT_NAME = "comicsansms"
WHITE, BLACK, GRAY, GREEN, RED, BLUE, YELLOW, DARK_BLUE, LIGHT_YELLOW = (
    (255, 255, 255), (0, 0, 0), (50, 50, 50), (0, 255, 0),
    (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 51, 102), (255, 255, 153)
)

# Init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

# Road track
ROAD_X_START = SCREEN_WIDTH // 2 - ROAD_WIDTH // 2
TRACKS = [ROAD_X_START + i * (ROAD_WIDTH // 5) for i in range(5)]

# Paths
root_path = str(Path(__file__).parent)
img_dir = os.path.join(root_path, "img")

# Assets
car_img = pygame.image.load(os.path.join(img_dir, "car.png"))
road_bg = pygame.image.load(os.path.join(img_dir, "back_ground.jpg"))
start_bg = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "start_bg.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
play_icon = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "pause_icon.jpg")), (30, 30))
enemy_imgs = [pygame.image.load(os.path.join(img_dir, f"enemy_car_{i+1}.png")) for i in range(ENEMY_COUNT)]

pause = False

class PlayerCar:
    def __init__(self):
        self.image = car_img
        self.track_index = 2
        self.x = TRACKS[self.track_index]
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 20
        self.move_step = 10

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.x > ROAD_X_START:
            self.x -= self.move_step

    def move_right(self):
        if self.x + CAR_WIDTH < ROAD_X_START + ROAD_WIDTH:
            self.x += self.move_step

    def move_up(self):
        if self.y > 0:
            self.y -= self.move_step

    def move_down(self):
        if self.y + CAR_HEIGHT < SCREEN_HEIGHT:
            self.y += self.move_step

class EnemyCar:
    used_tracks = []

    def __init__(self, img):
        self.image = img
        self.reset()

    def reset(self):
        available_tracks = list(set(TRACKS) - set(EnemyCar.used_tracks))
        if not available_tracks:
            EnemyCar.used_tracks.clear()
            available_tracks = TRACKS[:]
        self.x = random.choice(available_tracks)
        EnemyCar.used_tracks.append(self.x)
        self.y = random.randint(-600, -100)
        self.speed = 2

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def collides_with(self, player):
        return (
            player.y < self.y + CAR_HEIGHT and
            player.y + CAR_HEIGHT > self.y and
            player.x + CAR_WIDTH > self.x and
            player.x < self.x + CAR_WIDTH
        )

def draw_background(bg_y):
    screen.blit(road_bg, (ROAD_X_START, bg_y))
    screen.blit(road_bg, (ROAD_X_START, bg_y - SCREEN_HEIGHT))

def draw_score(score):
    font = pygame.font.SysFont("lucidaconsole", 20)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

def show_message(text):
    font = pygame.font.SysFont(FONT_NAME, 64, True)
    render = font.render(text, True, RED)
    screen.blit(render, ((SCREEN_WIDTH - render.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
    pygame.display.update()
    sleep(1)

def home_screen():
    screen.blit(start_bg, (0, 0))
    font = pygame.font.SysFont(FONT_NAME, 54, True)
    title = font.render("Car Racing Game", True, GREEN)
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 100))

    play_button = pygame.Rect((SCREEN_WIDTH // 2 - 100, 300, 200, 50))
    pygame.draw.rect(screen, DARK_BLUE, play_button, border_radius=10)
    screen.blit(play_icon, (play_button.x + 10, play_button.y + 10))
    font = pygame.font.SysFont(FONT_NAME, 30, True)
    screen.blit(font.render("Play", True, WHITE), (play_button.x + 50, play_button.y + 10))

    font_small = pygame.font.SysFont("lucidaconsole", 16)
    screen.blit(font_small.render("Done by: Vinay", True, LIGHT_YELLOW), (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 40))
    screen.blit(font_small.render("vinay.nani919@gmail.com", True, LIGHT_YELLOW), (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 20))

    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def restart_screen(score):
    screen.blit(start_bg, (0, 0))
    font = pygame.font.SysFont(FONT_NAME, 48, True)
    msg = font.render("Game Over!", True, RED)
    screen.blit(msg, ((SCREEN_WIDTH - msg.get_width()) // 2, 100))

    # ✅ Green colored message
    tagline = pygame.font.SysFont(FONT_NAME, 26, True).render("Play again and have fun!", True, GREEN)
    screen.blit(tagline, ((SCREEN_WIDTH - tagline.get_width()) // 2, 180))

    restart_button = pygame.Rect((SCREEN_WIDTH // 2 - 100, 300, 200, 50))
    pygame.draw.rect(screen, DARK_BLUE, restart_button, border_radius=10)
    screen.blit(play_icon, (restart_button.x + 10, restart_button.y + 10))
    font = pygame.font.SysFont(FONT_NAME, 30, True)
    screen.blit(font.render("Restart", True, WHITE), (restart_button.x + 50, restart_button.y + 10))

    font_small = pygame.font.SysFont("lucidaconsole", 16)
    screen.blit(font_small.render("Done by: Vinay", True, LIGHT_YELLOW), (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 60))
    screen.blit(font_small.render("vinay.nani919@gmail.com", True, LIGHT_YELLOW), (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 40))

    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_loop():
    global pause
    player = PlayerCar()
    enemies = []
    bg_y = 0
    score = 0
    running = True

    while running:
        screen.fill(GRAY)
        bg_y += 5 if not pause else 0
        if bg_y >= SCREEN_HEIGHT:
            bg_y = 0

        draw_background(bg_y)
        draw_score(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause

        keys = pygame.key.get_pressed()
        if not pause:
            if keys[pygame.K_LEFT]: player.move_left()
            if keys[pygame.K_RIGHT]: player.move_right()
            if keys[pygame.K_UP]: player.move_up()
            if keys[pygame.K_DOWN]: player.move_down()

            if len(enemies) < ENEMY_COUNT and score > len(enemies) * 500:
                enemies.append(EnemyCar(enemy_imgs[len(enemies) % len(enemy_imgs)]))

            for enemy in enemies:
                enemy.update()

            for enemy in enemies:
                if enemy.collides_with(player):
                    show_message("Game Over!")
                    restart_screen(score)
                    return

        player.draw()
        for enemy in enemies:
            enemy.draw()

        if not pause:
            score += SCORE_INCREMENT
            for e in enemies:
                if score < 2000:
                    e.speed = 2
                elif score < 6000:
                    e.speed = 4
                elif score < 12000:
                    e.speed = 6
                elif score < 20000:
                    e.speed = 8
                else:
                    e.speed = 10

        pygame.display.update()
        clock.tick(60)

# Entry Point
if __name__ == "__main__":
    while True:
        home_screen()
        game_loop()
