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
FONT_NAME = "arial"
WHITE, BLACK, GRAY, GREEN, RED, DARK_BLUE, LIGHT_YELLOW, DARK_TEXT = (
    (255, 255, 255), (0, 0, 0), (50, 50, 50), (0, 255, 0),
    (255, 0, 0), (0, 51, 102), (255, 255, 153), (33, 33, 33)
)

# Init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

# Road positioning
ROAD_X_START = SCREEN_WIDTH // 2 - ROAD_WIDTH // 2
TRACKS = [ROAD_X_START + i * (ROAD_WIDTH // 5) for i in range(5)]

# Paths
root_path = str(Path(__file__).parent)
img_dir = os.path.join(root_path, "img")

# Assets
car_img = pygame.image.load(os.path.join(img_dir, "car.png"))
road_bg = pygame.image.load(os.path.join(img_dir, "back_ground.jpg"))
start_bg = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "start_bg.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
end_bg = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "end_bg.webp")), (SCREEN_WIDTH, SCREEN_HEIGHT))
enemy_imgs = [pygame.image.load(os.path.join(img_dir, f"enemy_car_{i+1}.png")) for i in range(3)]

pause = False

class PlayerCar:
    def __init__(self):
        self.image = car_img
        self.x = TRACKS[2]
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 20
        self.move_step = 10

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.x - self.move_step >= ROAD_X_START:
            self.x -= self.move_step

    def move_right(self):
        if self.x + CAR_WIDTH + self.move_step <= ROAD_X_START + ROAD_WIDTH:
            self.x += self.move_step

    def move_up(self):
        if self.y > 0:
            self.y -= self.move_step

    def move_down(self):
        if self.y + CAR_HEIGHT < SCREEN_HEIGHT:
            self.y += self.move_step

class EnemyCar:
    used_tracks = []

    def __init__(self, img, speed):
        self.image = img
        self.speed = speed
        self.reset()

    def reset(self):
        available_tracks = list(set(TRACKS) - set(EnemyCar.used_tracks))
        if not available_tracks:
            EnemyCar.used_tracks.clear()
            available_tracks = TRACKS[:]
        self.x = random.choice(available_tracks)
        EnemyCar.used_tracks.append(self.x)
        self.y = random.randint(-600, -100)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset()
            return True
        return False

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

def draw_hud(score, passed):
    font = pygame.font.SysFont("lucidaconsole", 20, bold=True)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Cars Passed: {passed}", True, WHITE), (10, 35))

def show_message(text):
    font = pygame.font.SysFont(FONT_NAME, 64, True)
    render = font.render(text, True, RED)
    screen.blit(render, ((SCREEN_WIDTH - render.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
    pygame.display.update()
    sleep(1)

def center_text_in_button(text, font, rect):
    text_surface = font.render(text, True, WHITE)
    x = rect.x + (rect.width - text_surface.get_width()) // 2
    y = rect.y + (rect.height - text_surface.get_height()) // 2
    screen.blit(text_surface, (x, y))

def home_screen():
    screen.blit(start_bg, (0, 0))
    button_font = pygame.font.SysFont(FONT_NAME, 36, bold=True)

    # Start and Quit buttons at bottom corners
    start_btn = pygame.Rect(40, SCREEN_HEIGHT - 80, 200, 60)
    quit_btn = pygame.Rect(SCREEN_WIDTH - 240, SCREEN_HEIGHT - 80, 200, 60)

    pygame.draw.rect(screen, DARK_BLUE, start_btn, border_radius=10)
    pygame.draw.rect(screen, DARK_BLUE, quit_btn, border_radius=10)

    center_text_in_button("START", button_font, start_btn)
    center_text_in_button("QUIT", button_font, quit_btn)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def restart_screen(score, passed):
    screen.blit(end_bg, (0, 0))

    font = pygame.font.SysFont(FONT_NAME, 48, True)
    label_font = pygame.font.SysFont(FONT_NAME, 28, bold=True)
    tip_font = pygame.font.SysFont(FONT_NAME, 26, True)

    # Centered messages
    game_over_text = font.render("Game Over!", True, RED)
    score_text = label_font.render(f"Score: {score}", True, DARK_TEXT)
    passed_text = label_font.render(f"Cars Passed: {passed}", True, DARK_TEXT)
    tip_text = tip_font.render("Play again and have fun!", True, (255, 140, 0))  # Orange

    screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, 80))
    screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 150))
    screen.blit(passed_text, ((SCREEN_WIDTH - passed_text.get_width()) // 2, 190))
    screen.blit(tip_text, ((SCREEN_WIDTH - tip_text.get_width()) // 2, 250))

    restart_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 60)
    pygame.draw.rect(screen, DARK_BLUE, restart_btn, border_radius=10)
    center_text_in_button("RESTART", pygame.font.SysFont(FONT_NAME, 30, True), restart_btn)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_loop():
    global pause
    player = PlayerCar()
    enemies = []
    bg_y = 0
    score = 0
    passed = 0

    while True:
        screen.fill(GRAY)
        bg_y = (bg_y + 5) % SCREEN_HEIGHT
        draw_background(bg_y)
        draw_hud(score, passed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause

        keys = pygame.key.get_pressed()
        if not pause:
            if keys[pygame.K_LEFT]: player.move_left()
            if keys[pygame.K_RIGHT]: player.move_right()
            if keys[pygame.K_UP]: player.move_up()
            if keys[pygame.K_DOWN]: player.move_down()

            if len(enemies) < 1 or passed >= len(enemies) * 10:
                speed = 2 + (passed // 10)
                enemies.append(EnemyCar(enemy_imgs[len(enemies) % len(enemy_imgs)], speed))

            for enemy in enemies:
                if enemy.update():
                    passed += 1
                    score = passed * 10

            for enemy in enemies:
                if enemy.collides_with(player):
                    show_message("Game Over!")
                    restart_screen(score, passed)
                    return

        player.draw()
        for enemy in enemies:
            enemy.draw()

        pygame.display.update()
        clock.tick(60)

# Entry Point
if __name__ == "__main__":
    while True:
        home_screen()
        game_loop()
