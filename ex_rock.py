import pygame
import random

# Initialize Pygame
pygame.init()

# Set the size of the window
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Rock Rain")

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Define the font for the score
font = pygame.font.Font(None, 36)

# Set the frame rate
clock = pygame.time.Clock()
FPS = 60

# Load the rock image
rock_image = pygame.image.load("rock01.png").convert_alpha()

# Create an empty list for the rocks
rocks = []

# Create a variable to keep track of the score
score = 0

# Main game loop
game_running = True
while game_running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Create a new rock every 50 frames
    if len(rocks) < 10:
        if random.randint(0, 50) == 0:
            rock_x = random.randint(0, window_size[0] - rock_image.get_width())
            rock_y = -rock_image.get_height()
            rock_speed = random.randint(1, 5)
            rocks.append((rock_x, rock_y, rock_speed))

    # Update the position of the rocks
    for i, rock in enumerate(rocks):
        rock_x, rock_y, rock_speed = rock
        rock_y += rock_speed
        rocks[i] = (rock_x, rock_y, rock_speed)

        # Remove the rock if it goes off the bottom of the screen
        if rock_y > window_size[1]:
            rocks.pop(i)

    # Draw the background
    screen.fill(BLACK)

    # Draw the rocks
    for rock in rocks:
        rock_x, rock_y, rock_speed = rock
        screen.blit(rock_image, (rock_x, rock_y))

    # Draw the score
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Increase the score for every rock that goes off the bottom of the screen
    for rock in rocks:
        if rock[1] > window_size[1]:
            score += 1

    # Wait for the next frame
    clock.tick(FPS)

# Quit Pygame
pygame.quit()