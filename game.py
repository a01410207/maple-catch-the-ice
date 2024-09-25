import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maple Catch the Ice!")

# Player properties
player_size = 100  # Size of the player image
player_pos = [
    screen_width // 2,
    screen_height - player_size - 30,
]  # Lower the cat's position by adjusting the Y-coordinate

# Load and scale the player image
cat_image = pygame.image.load("assets/maple.png").convert_alpha()
cat_image = pygame.transform.scale(cat_image, (player_size, player_size))

# Get player image dimensions
player_width, player_height = cat_image.get_size()

# Ice cube properties
ice_size = 50
ice_color = (0, 191, 255)  # Blue color for ice cubes

# Colors
background_color = (200, 225, 227)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Set up font for score display and game over text
font = pygame.font.SysFont("monospace", 35)
game_over_font = pygame.font.SysFont("monospace", 75)

# Global game variables (initialize here to avoid issues with scoping)
player_pos = []
ice_list = []
score = 0
ice_speed = 4  # Increase the speed of the falling ice cubes
missed_ice_count = 0  # Track the number of missed ice cubes


# Function to reset game variables
def reset_game():
    global player_pos, ice_list, score, ice_speed, missed_ice_count
    player_pos = [
        screen_width // 2,
        screen_height - player_size - 30,
    ]  # Reset the cat's lower position
    ice_list = []
    score = 0
    ice_speed = 4  # Set the speed of the ice cubes
    missed_ice_count = 0  # Reset the missed ice count


# Function to set ice cube falling speed based on score
def set_level(score, ice_speed):
    if score < 20:
        ice_speed = 4  # Faster falling speed for ice cubes
    elif score < 40:
        ice_speed = 6
    elif score < 60:
        ice_speed = 8
    else:
        ice_speed = 10
    return ice_speed


# Function to adjust ice drop rate based on a difficulty level from 1 (rare) to 10 (frequent)
def set_ice_drop_rate(level):
    # Convert level to a probability value. Higher levels drop more frequently.
    min_level = 1
    max_level = 10
    level = max(min(level, max_level), min_level)  # Clamp the value between 1 and 10
    return (11 - level) * 0.01  # As the level increases, delay decreases


# Function to drop new ice cubes based on the current drop rate
def drop_ice(ice_list, drop_rate):
    delay = random.random()
    if len(ice_list) < 3 and delay < drop_rate:
        x_pos = random.randint(0, screen_width - ice_size)
        y_pos = 0
        ice_list.append([x_pos, y_pos])


# Function to draw ice cubes
def draw_ice(ice_list):
    for ice_pos in ice_list:
        pygame.draw.rect(
            screen, ice_color, (ice_pos[0], ice_pos[1], ice_size, ice_size)
        )


# Function to update ice cube positions
def update_ice_positions(ice_list):
    global missed_ice_count
    for idx, ice_pos in enumerate(ice_list):
        if 0 <= ice_pos[1] < screen_height:
            ice_pos[1] += ice_speed
        else:
            # If ice cube reaches the bottom, increment missed ice count and remove the ice cube
            missed_ice_count += 1
            ice_list.pop(idx)


# Function to detect collisions (player catching ice cubes)
def detect_collision(ice_pos, player_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    p_width = player_width
    p_height = player_height

    i_x = ice_pos[0]
    i_y = ice_pos[1]
    i_size = ice_size

    if (
        (i_x < p_x + p_width)
        and (i_x + i_size > p_x)
        and (i_y < p_y + p_height)
        and (i_y + i_size > p_y)
    ):
        return True
    return False


# Function to check for collisions between player and ice cubes
def collision_check(ice_list, player_pos):
    for ice_pos in ice_list:
        if detect_collision(ice_pos, player_pos):
            return True
    return False


# Function to display Game Over message and Play Again prompt
def show_game_over():
    screen.fill(background_color)

    # Center "Game Over" text dynamically
    game_over_text = "Game Over!"
    game_over_label = game_over_font.render(game_over_text, True, (255, 0, 0))
    game_over_label_width = game_over_font.size(game_over_text)[0]
    game_over_x_pos = (screen_width - game_over_label_width) // 2

    # Create black play again text and center it
    play_again_text = "¿Jugar de nuevo? (Y/N)"
    play_again_label = font.render(
        play_again_text, True, (0, 0, 0)
    )  # Change text color to black

    # Center the play again text dynamically
    play_again_label_width = font.size(play_again_text)[0]
    play_again_x_pos = (screen_width - play_again_label_width) // 2

    # Display the Game Over and Play Again prompt
    screen.blit(game_over_label, (game_over_x_pos, screen_height // 2 - 100))
    screen.blit(play_again_label, (play_again_x_pos, screen_height // 2 + 50))

    pygame.display.update()

    # Wait for the player's response
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Restart the game
                    waiting_for_input = False
                    reset_game()
                if event.key == pygame.K_n:  # Exit the game
                    pygame.quit()
                    sys.exit()


# Main game loop
def game_loop(ice_drop_level):
    global score, ice_speed, ice_list, missed_ice_count
    drop_rate = set_ice_drop_rate(
        ice_drop_level
    )  # Get the drop rate based on the level
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_width:
            player_pos[0] += 10

        # Fill the screen with background color
        screen.fill(background_color)

        # Drop ice cubes
        drop_ice(ice_list, drop_rate)

        # Update ice cube positions and check if any were missed
        update_ice_positions(ice_list)

        # Adjust ice cube speed based on score
        ice_speed = set_level(score, ice_speed)

        # Check for ice cubes caught by the player
        if collision_check(ice_list, player_pos):
            # Increase the score when an ice cube is caught
            score += 1
            # Remove the caught ice cube
            ice_list = [
                ice for ice in ice_list if not detect_collision(ice, player_pos)
            ]

        # Draw ice cubes
        draw_ice(ice_list)

        # Draw the player image
        screen.blit(cat_image, (player_pos[0], player_pos[1]))

        # Display the score in black
        text = "Score: " + str(score)
        label = font.render(text, True, (0, 0, 0))  # Change text color to black
        screen.blit(label, (screen_width - 200, screen_height - 40))

        # Check if the player missed 3 ice cubes
        if missed_ice_count >= 3:
            show_game_over()

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clock.tick(30)


# Start the game loop with ice drop rate level (1-10)
reset_game()
game_loop(ice_drop_level=3)  # Set the drop level from 1 (rare) to 10 (frequent)
