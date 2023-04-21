
import pygame, random
pygame.init()

# Set up the game window
screen_width = 1000
screen_height = 600
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meteorite Rain")

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the fonts
small_font = pygame.font.SysFont("comicsansms", 25)
medium_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

# Set up the meteorites
meteorite_image = pygame.image.load("rock01.png").convert_alpha()
meteorite_list = []

for i in range(10):
    x = random.randrange(0, screen_width)
    y = random.randrange(-600, -50)
    speed = random.randrange(1, 10)
    meteorite_list.append([x, y, speed])

# Set up the clock
clock = pygame.time.Clock()

# Set up the score
score = 0

# Main game loop
game_exit = False
while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

        # Check for the "q" key being pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            meteorite_list = [] # clear the meteorite list

    # Move the meteorites
    for meteorite in meteorite_list:
        meteorite[1] += meteorite[2]
        if meteorite[1] > screen_height:
            meteorite_list.remove(meteorite)
            score += 1

    # Draw the background
    game_display.fill(black)

    # Draw the meteorites
    for meteorite in meteorite_list:
        game_display.blit(meteorite_image, [meteorite[0], meteorite[1]])

    # Draw the score
    score_text = small_font.render("Score: " + str(score), True, white)
    game_display.blit(score_text, [10, 10])

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Clean up the game
pygame.quit()
quit()