# Tower Defense Lab
version =  "February 12th 2025"
author = "Ibrahim Taha"

# view my flint sessions here:
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/a78216cd-da43-44c0-8b4a-9f7235235e87
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/868a8eeb-79c5-45a6-9cd5-6777d5575873
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/c627152f-9f56-43ea-b45f-08a299dbf89f

# Required Library Imports
# Import necessary Python libraries for game development
# pygame: Main game library
# random: For generating random numbers
# sys: For system operations
# os: For file/directory operations
# time: For timing functions
import pygame
import random
import sys
import os
import time

# Define game window dimensions and create the game window
# Set the game's title in the window bar
WIDTH, HEIGHT = 800, 600

# Lines 27-32: Color Definitions
# Define RGB color tuples used throughout the game
# Colors include WHITE, BLACK, BLUE, GREEN, and YELLOW
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Asset Loading
# Set up file paths and load game assets (images and sounds)
# Includes error handling for missing files
# Scales images to appropriate sizes
# Sets up sound volume
current_dir = os.path.dirname(os.path.abspath(__file__))
ryan_img_path = os.path.join(current_dir, 'Ryan.png') # Photo of Ryan
cochran_img_path = os.path.join(current_dir, 'Mr. Cochran.png') # Photo of Mr. Cochran
gong_sound_path = os.path.join(current_dir, 'asian-gong-music.mp3') # Audio

# Shooter setup
# Initialize shooter (Mr. Cochran) properties
# Position, speed, and bullet list
shooter_speed = 5
falling_speed = 2

# Bullet Class Definition
# Definition of the bullet class with properties and methods
# Includes initialization, movement, drawing, and screen boundary checking
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 20
        self.radius = 3
        self.active = True

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return self.y < -20

# Function to display score and game over messages
def handle_score(screen, score, game_over, font, WIDTH, HEIGHT, WHITE):
    if not game_over:
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        game_over_text = font.render('Game Over!', True, WHITE)
        final_score_text = font.render(f'Final Score: {score}', True, WHITE)
        restart_text = font.render('Press R to Restart', True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

# Function to create new falling objects with random positions
# Handles special border cases and auto-shooting states
def create_falling_object():
    x = random.randint(0, WIDTH - 80)
    if auto_shooting:
        border_color = None  # No special Ryans during auto-shoot
    else:
        if random.random() < 0.25:  # 25% chance for green border
            border_color = 'green'  # Only green, no more red
        else:
            border_color = None
    falling_objects.append({
        'x': x,
        'y': -80,
        'border_color': border_color,
        'during_auto_shoot': auto_shooting
    })

# Functions to create and update bullets
def shoot_bullet(x, y):
    bullets.append(Bullet(x, y))

def update_bullets():
    for bullet in bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullets.remove(bullet)

# Function to stop all currently playing sounds
def stop_all_sounds():
    pygame.mixer.stop()  # Stops all playing sounds

# Function to check for collisions between bullets and falling objects
# Handles scoring and special effects
def check_collision():
    global score, game_over, auto_shooting, auto_shooting_end_time
    for bullet in bullets[:]:
        if bullet.active:
            for obj in falling_objects[:]:
                bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius,
                                          bullet.radius * 2, bullet.radius * 2)
                obj_rect = pygame.Rect(obj['x'], obj['y'], 80, 80)

                if bullet_rect.colliderect(obj_rect):
                    # Play gong sound on collision
                    gong_sound.play()

                    if obj['border_color'] == 'green':
                        auto_shooting = True
                        auto_shooting_end_time = time.time() + 7
                        for falling_obj in falling_objects:
                            falling_obj['during_auto_shoot'] = True

                    falling_objects.remove(obj)
                    bullets.remove(bullet)
                    score += 1
                    break

# Function to display the auto-shoot activation message
def display_auto_shoot_message():
    message = font.render("Auto Shoot for 7 seconds", True, YELLOW)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.delay(1000)

# Handles automatic shooting mechanics
# Targets closest falling object or shoots randomly
def auto_shoot():
    global shooter_x, shooter_y
    if falling_objects:
        # Target the Ryan closest to the ground
        closest_objects = sorted(falling_objects, key=lambda obj: obj['y'], reverse=True)
        target = closest_objects[0]
        shooter_x = target['x'] + 40  # Center on target
        shooter_y = HEIGHT - 100
        shoot_bullet(shooter_x, shooter_y - 25)
    else:
        # If no targets, shoot from random position
        shooter_x = random.randint(50, WIDTH - 50)
        shooter_y = HEIGHT - 100
        shoot_bullet(shooter_x, shooter_y)
# Function that contains the primary game loop and initialization
# Handles the core game mechanics and main loop execution
def main():
    global screen, ryan_img, cochran_img, gong_sound, bullets, falling_objects
    global score, auto_shooting, auto_shooting_end_time, shooter_x, shooter_y, font

    # Initialize the main Pygame engine and sound system
    pygame.init()
    pygame.mixer.init()  # Initialize the sound mixer

    # Define game window dimensions and create the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tower Defense Game')

    # Load game assets
    try:
        ryan_img = pygame.image.load(ryan_img_path)
        ryan_img = pygame.transform.scale(ryan_img, (80, 80))
        cochran_img = pygame.image.load(cochran_img_path)
        cochran_img = pygame.transform.scale(cochran_img, (50, 50))
        gong_sound = pygame.mixer.Sound(gong_sound_path)
        gong_sound.set_volume(0.5)  # Set sound volume to 50%
    except Exception as e:
        print(f"Error loading assets: {e}")
        sys.exit(1)

    # Initialize game state variables
    running = True
    game_over = False
    score = 0
    shooter_x = WIDTH // 2
    shooter_y = HEIGHT - 60
    bullets = []
    falling_objects = []
    auto_shooting = False
    auto_shooting_end_time = 0
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Add a timer for automatic shooting
    SHOOT_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SHOOT_EVENT, 300)

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_all_sounds()  # Stop sounds before quitting
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    stop_all_sounds()  # Stop any lingering sounds
                    falling_objects = []
                    bullets = []
                    score = 0
                    game_over = False
                    auto_shooting = False
            elif event.type == SHOOT_EVENT and not game_over:
                if auto_shooting:
                    auto_shoot()
                else:
                    shoot_bullet(shooter_x, shooter_y - 25)

        # Handle player movement
        keys = pygame.key.get_pressed()
        if not auto_shooting:  # Only allow movement when not auto-shooting
            if keys[pygame.K_LEFT] and shooter_x > 25:
                shooter_x -= shooter_speed
            if keys[pygame.K_RIGHT] and shooter_x < WIDTH - 25:
                shooter_x += shooter_speed
            if keys[pygame.K_UP] and shooter_y > 25:
                shooter_y -= shooter_speed
            if keys[pygame.K_DOWN] and shooter_y < HEIGHT - 25:
                shooter_y += shooter_speed

        if not game_over:
            # Create new Ryans
            if random.random() < 0.02:  # 2% chance each frame
                create_falling_object()

            update_bullets()
            check_collision()

            # Check if auto-shooting should end
            if auto_shooting and time.time() > auto_shooting_end_time:
                auto_shooting = False

            # Update falling Ryans
            for obj in falling_objects[:]:
                obj['y'] += falling_speed
                if obj['y'] > HEIGHT:
                    # Only end game if a normal Ryan that wasn't during auto-shoot reaches bottom
                    if obj['border_color'] is None and not obj.get('during_auto_shoot', False):
                        stop_all_sounds()  # Stop sounds when game ends
                        game_over = True
                    falling_objects.remove(obj)

        # Drawing
        screen.fill(BLACK)
        if not game_over:
            # Draw bullets
            for bullet in bullets:
                bullet.draw(screen)

            # Draw Mr. Cochran
            screen.blit(cochran_img, (shooter_x - 25, shooter_y - 25))

            # Draw Ryans
            for obj in falling_objects:
                screen.blit(ryan_img, (obj['x'], obj['y']))
                if obj['border_color']:
                    border_thickness = 3
                    border_color = GREEN  # Only green borders now
                    pygame.draw.rect(screen, border_color,
                                     (obj['x'], obj['y'], 80, 80), border_thickness)

        # Show auto-shoot message
        if auto_shooting and time.time() < auto_shooting_end_time - 6.9:
            display_auto_shoot_message()

        # Update score and game over message
        handle_score(screen, score, game_over, font, WIDTH, HEIGHT, WHITE)

        pygame.display.flip()
        clock.tick(60)

    # Clean up
    stop_all_sounds()  # Ensure all sounds are stopped before quitting
    pygame.mixer.quit()
    pygame.quit()

# Main entry point
# Executes the game when the script is run directly
if __name__ == '__main__':
    main()