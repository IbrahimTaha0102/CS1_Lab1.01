# Tower Defense Lab
version =  "February 12th 2025"
author = "Ibrahim Taha"

# view my flint sessions here:
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/a78216cd-da43-44c0-8b4a-9f7235235e87
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/868a8eeb-79c5-45a6-9cd5-6777d5575873
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/c627152f-9f56-43ea-b45f-08a299dbf89f


import pygame
import random
import sys
import os
import time

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()  # Initialize the sound mixer

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tower Defense Game')

# Colors set up (used later)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load images and sound
current_dir = os.path.dirname(os.path.abspath(__file__))
ryan_img_path = os.path.join(current_dir, 'Ryan.png') # Photo of Ryan
cochran_img_path = os.path.join(current_dir, 'Mr. Cochran.png') # Photo of Mr. Cochran
gong_sound_path = os.path.join(current_dir, 'asian-gong-music.mp3') # Audio

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

# Shooter properties
shooter_x = WIDTH // 2
shooter_y = HEIGHT - 60
shooter_speed = 5
bullets = []


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


# Falling object properties (aka photo of Ryan)
falling_objects = []
falling_speed = 2

# Game variables
score = 0
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
auto_shooting = False
auto_shooting_end_time = 0

# Add a timer for automatic shooting
SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SHOOT_EVENT, 300)


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


def shoot_bullet(x, y):
    bullets.append(Bullet(x, y))


def update_bullets():
    for bullet in bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullets.remove(bullet)


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


def display_auto_shoot_message():
    message = font.render("Auto Shoot for 7 seconds", True, YELLOW)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.delay(1000)


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


# Main game loop
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game
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
pygame.mixer.quit()
pygame.quit()