
import random
import pygame
import os
import json

pygame.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Rocks")

# Load the high scores from a file
if os.path.isfile('scores.json'):
    with open('scores.json', 'r') as f:
        high_scores = json.load(f)
else:
    high_scores = []

# Set up the fonts
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('./font/12Bold', 40)
RANK_FONT = pygame.font.SysFont('./font/12Bold', 30)

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the player
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_SPEED = 10
player_img = pygame.image.load('fighter3.png')
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - PLAYER_HEIGHT - 10

# Set up the rock
ROCK_WIDTH, ROCK_HEIGHT = 50, 50
ROCK_SPEED = 5
rock_img = pygame.image.load('rock01.png')
rock_img = pygame.transform.scale(rock_img, (ROCK_WIDTH, ROCK_HEIGHT))
rock_x = random.randint(0, WIDTH - ROCK_WIDTH)
rock_y = -ROCK_HEIGHT

# Set up the clock
clock = pygame.time.Clock()

# Set up the score
score = 0

def draw_window():
    WIN.fill(WHITE)
    # Draw the player
    WIN.blit(player_img, (player_x, player_y))
    # Draw the rock
    WIN.blit(rock_img, (rock_x, rock_y))
    # Draw the score
    score_label = SCORE_FONT.render(f"Score: {score}", 1, BLACK)
    WIN.blit(score_label, (10, 10))
    # Draw the high scores
    for i, high_score in enumerate(high_scores):
        rank_label = RANK_FONT.render(f"{i + 1}.", 1, BLACK)
        WIN.blit(rank_label, (10, 50 + i * 30))
        score_label = RANK_FONT.render(f"{high_score}", 1, BLACK)
        WIN.blit(score_label, (50, 50 + i * 30))

    pygame.display.update()

def update_rock_position():
    global rock_x, rock_y, score
    rock_y += ROCK_SPEED
    if rock_y > HEIGHT:
        # The rock fell off the screen, reset its position
        rock_x = random.randint(0, WIDTH - ROCK_WIDTH)
        rock_y = -ROCK_HEIGHT
        score += 1
        # Add the score to the high scores and save to file
        high_scores.append(score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:5]  # Only keep the top 5 scores
        with open('scores.json', 'w') as f:
            json.dump(high_scores, f)

def move_player(keys_pressed):
    global player_x
    if keys_pressed[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys_pressed[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH