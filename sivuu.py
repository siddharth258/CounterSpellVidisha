import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display (full-screen mode)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()  # Get the screen size after setting full screen
pygame.display.set_caption("Simple 2D Game")

# Load images with error handling
def load_image(filename):
    try:
        image = pygame.image.load(filename)
        return image
    except pygame.error as e:
        print(f"Error loading image: {filename} - {e}")
        pygame.quit()
        quit()

background = load_image('bg.png')
player_image = load_image('player.png')
obstacle_image = load_image('evil.png')

# Scale images (optional, you can adjust size if needed)
player_image = pygame.transform.scale(player_image, (80, 80))
obstacle_image = pygame.transform.scale(obstacle_image, (70, 50))

# Scale the background to fit the screen
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Player properties
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 60
player_speed = 5

# Obstacle properties
obstacle_speed = 7
obstacle_frequency = 0.02  # Frequency of obstacles
obstacles = []

# Set up the clock
clock = pygame.time.Clock()

# Font for score and level display
font = pygame.font.SysFont("Arial", 24)
bold_font = pygame.font.SysFont("Arial", 28, bold=True)

# High score file path
high_score_file = 'highscore.txt'

# Load the high score from file
def load_high_score():
    try:
        with open(high_score_file, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # If the file doesn't exist, return 0

# Save the high score to file
def save_high_score(new_high_score):
    with open(high_score_file, 'w') as file:
        file.write(str(new_high_score))

# Level specific difficulty
def adjust_difficulty(level):
    """Increase difficulty as the player progresses through levels."""
    global obstacle_speed, obstacle_frequency
    if level <= 3:
        obstacle_speed = 7 + level
        obstacle_frequency = 0.02 + level * 0.005
    elif level <= 6:
        obstacle_speed = 10 + level
        obstacle_frequency = 0.05 + level * 0.01
    else:
        obstacle_speed = 15 + level
        obstacle_frequency = 0.1 + level * 0.02

# Game over function (modified)
def game_over():
    """Display the Game Over screen and final score/level."""
    high_score = load_high_score()

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    final_level_text = font.render(f"Final Level: {level}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(final_level_text, (WIDTH // 2 - final_level_text.get_width() // 2, HEIGHT // 2 + 30))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return True  # Restart the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# Function for the starting screen
def start_screen():
    """Display the start screen and wait for spacebar press."""
    start_text = font.render("Press Space to Start", True, (255, 255, 255))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Start the game

# Main game loop
def main_game():
    global score, level, player_x, player_y, obstacles
    score = 0
    level = 1
    obstacles = []
    player_x = WIDTH // 2 - 25
    player_y = HEIGHT - 60

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed

        if score >= level * 30:
            level += 1
            adjust_difficulty(level)

        # Create obstacles
        if random.random() < obstacle_frequency:
            obstacle_x = random.randint(0, WIDTH - 50)
            obstacle_y = -50
            obstacles.append([obstacle_x, obstacle_y])

        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        for obstacle in obstacles:
            if (player_x < obstacle[0] + 50 and player_x + 50 > obstacle[0] and player_y < obstacle[1] + 50 and player_y + 50 > obstacle[1]):
                print("Player collided with obstacle!")
                return False  # Collision detected

        # Display the background
        screen.blit(background, (0, 0))
        screen.blit(player_image, (player_x, player_y))

        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # Display score and level
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
 m
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(level_text, (WIDTH - 150, 10))

        # Display the quote in bold when the score reaches 300
        if score >= 300:
            quote_text = bold_font.render("You saved many, but risked your own.", True, (255, 255, 255))
            screen.blit(quote_text, (WIDTH // 2 - quote_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        clock.tick(60)
    return True

# Main execution flow
while True:
    start_screen()
    game_successful = main_game()

    if not game_successful:
        game_over()
        continue

pygame.quit()
