import serial
import pygame
import random
import math

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
pygame.mixer.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Axis Drift Enhanced v1.0")

# -----------------------------
# Colors
# -----------------------------
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# -----------------------------
# Character setup
# -----------------------------
BASE_CHARACTER_SIZE = 25
MAX_CHARACTER_SIZE = 80
MIN_CHARACTER_SIZE = 15
character_size = BASE_CHARACTER_SIZE
CHARACTER_COLOR = RED
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
CHARACTER_SPEED = 8

# -----------------------------
# Game state
# -----------------------------
score = 0
lives = 3
game_state = "playing"  # "playing", "win", "lose"
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# -----------------------------
# Collectibles and obstacles
# -----------------------------
collectibles = []
obstacles = []
COLLECTIBLE_SIZE = 15
OBSTACLE_SIZE = 20

def create_collectible():
    return {
        'x': random.randint(COLLECTIBLE_SIZE, WIN_WIDTH - COLLECTIBLE_SIZE),
        'y': random.randint(COLLECTIBLE_SIZE, WIN_HEIGHT - COLLECTIBLE_SIZE),
        'color': GREEN
    }

def create_obstacle():
    return {
        'x': random.randint(OBSTACLE_SIZE, WIN_WIDTH - OBSTACLE_SIZE),
        'y': random.randint(OBSTACLE_SIZE, WIN_HEIGHT - OBSTACLE_SIZE),
        'color': PURPLE
    }

# Create initial collectibles and obstacles
for _ in range(5):
    collectibles.append(create_collectible())
for _ in range(3):
    obstacles.append(create_obstacle())

# -----------------------------
# Audio setup (using built-in sounds)
# -----------------------------
def create_tone(frequency, duration, sample_rate=22050):
    """Create a simple tone"""
    frames = int(duration * sample_rate)
    arr = []
    for i in range(frames):
        wave = 32767 * math.sin(2 * math.pi * frequency * i / sample_rate)
        arr.append([int(wave), int(wave)])
    return pygame.sndarray.make_sound(pygame.array.array('h', arr))

# Create sound effects
collect_sound = create_tone(440, 0.2)  # A note
hit_sound = create_tone(220, 0.3)      # Lower A note
grow_sound = create_tone(660, 0.15)    # Higher tone
shrink_sound = create_tone(330, 0.15)  # Lower tone
win_sound = create_tone(523, 0.5)      # C note
lose_sound = create_tone(196, 0.8)     # G note

# -----------------------------
# Serial setup
# -----------------------------
try:
    arduino_serial = serial.Serial('/dev/ttyACM0', 9600)
    serial_connected = True
except:
    print("Arduino not connected. Using keyboard controls.")
    serial_connected = False

# -----------------------------
# Helper functions
# -----------------------------
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def check_collision(obj_x, obj_y, obj_size, char_x, char_y, char_size):
    return distance(obj_x, obj_y, char_x, char_y) < (obj_size + char_size)

def draw_hud():
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    size_text = font.render(f"Size: {character_size}", True, WHITE)
    
    win.blit(score_text, (10, 10))
    win.blit(lives_text, (10, 50))
    win.blit(size_text, (10, 90))

def draw_instructions():
    if not serial_connected:
        inst_text = font.render("Use WASD to move, Space to grow, Shift to shrink", True, WHITE)
        win.blit(inst_text, (10, WIN_HEIGHT - 30))

# -----------------------------
# Game loop setup
# -----------------------------
clock = pygame.time.Clock()
running = True
last_collectible_spawn = 0
spawn_delay = 3000  # 3 seconds

while running:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state != "playing":
                # Reset game
                score = 0
                lives = 3
                game_state = "playing"
                character_size = BASE_CHARACTER_SIZE
                x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
                collectibles.clear()
                obstacles.clear()
                for _ in range(5):
                    collectibles.append(create_collectible())
                for _ in range(3):
                    obstacles.append(create_obstacle())

    if game_state == "playing":
        # Movement handling
        moved = False
        
        if serial_connected:
            # Read joystick data from Arduino
            if arduino_serial.in_waiting > 0:
                try:
                    data = arduino_serial.readline().decode().strip().split(',')
                    xValue, yValue, button = map(int, data)

                    # Map joystick values to character movement
                    if xValue < 400:
                        x -= CHARACTER_SPEED
                        moved = True
                    elif xValue > 600:
                        x += CHARACTER_SPEED
                        moved = True

                    if yValue < 400:
                        y -= CHARACTER_SPEED
                        moved = True
                    elif yValue > 600:
                        y += CHARACTER_SPEED
                        moved = True
                    
                    # Button controls character size
                    if button == 1:  # Button pressed
                        if character_size < MAX_CHARACTER_SIZE:
                            character_size += 1
                            grow_sound.play()
                    else:  # Button not pressed
                        if character_size > MIN_CHARACTER_SIZE:
                            character_size -= 1
                            shrink_sound.play()

                except Exception as e:
                    pass
        else:
            # Keyboard controls as fallback
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                x -= CHARACTER_SPEED
                moved = True
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                x += CHARACTER_SPEED
                moved = True
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                y -= CHARACTER_SPEED
                moved = True
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                y += CHARACTER_SPEED
                moved = True
            
            if keys[pygame.K_SPACE]:
                if character_size < MAX_CHARACTER_SIZE:
                    character_size += 1
                    grow_sound.play()
            if keys[pygame.K_LSHIFT]:
                if character_size > MIN_CHARACTER_SIZE:
                    character_size -= 1
                    shrink_sound.play()

        # Set boundaries
        x = max(character_size, min(WIN_WIDTH - character_size, x))
        y = max(character_size, min(WIN_HEIGHT - character_size, y))

        # Check collectible collisions
        for collectible in collectibles[:]:
            if check_collision(collectible['x'], collectible['y'], COLLECTIBLE_SIZE, x, y, character_size):
                collectibles.remove(collectible)
                score += 10
                collect_sound.play()
                # Add new collectible
                collectibles.append(create_collectible())

        # Check obstacle collisions
        for obstacle in obstacles:
            if check_collision(obstacle['x'], obstacle['y'], OBSTACLE_SIZE, x, y, character_size):
                lives -= 1
                hit_sound.play()
                # Move obstacle to new position
                obstacle['x'] = random.randint(OBSTACLE_SIZE, WIN_WIDTH - OBSTACLE_SIZE)
                obstacle['y'] = random.randint(OBSTACLE_SIZE, WIN_HEIGHT - OBSTACLE_SIZE)
                
                if lives <= 0:
                    game_state = "lose"
                    lose_sound.play()

        # Spawn additional obstacles based on score
        if current_time - last_collectible_spawn > spawn_delay:
            if score > 50 and len(obstacles) < 5:
                obstacles.append(create_obstacle())
            if score > 100 and len(obstacles) < 7:
                obstacles.append(create_obstacle())
            last_collectible_spawn = current_time

        # Win condition
        if score >= 200:
            game_state = "win"
            win_sound.play()

    # Draw everything
    win.fill(BLACK)
    
    if game_state == "playing":
        # Draw collectibles
        for collectible in collectibles:
            pygame.draw.circle(win, collectible['color'], 
                             (collectible['x'], collectible['y']), COLLECTIBLE_SIZE)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.circle(win, obstacle['color'], 
                             (obstacle['x'], obstacle['y']), OBSTACLE_SIZE)

        # Draw character
        pygame.draw.circle(win, CHARACTER_COLOR, (x, y), character_size)
        
        # Draw HUD
        draw_hud()
        draw_instructions()
        
    elif game_state == "win":
        win_text = big_font.render("YOU WIN!", True, GREEN)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        
        win.blit(win_text, (WIN_WIDTH//2 - 120, WIN_HEIGHT//2 - 100))
        win.blit(score_text, (WIN_WIDTH//2 - 80, WIN_HEIGHT//2 - 50))
        win.blit(restart_text, (WIN_WIDTH//2 - 90, WIN_HEIGHT//2))
        
    elif game_state == "lose":
        lose_text = big_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        
        win.blit(lose_text, (WIN_WIDTH//2 - 140, WIN_HEIGHT//2 - 100))
        win.blit(score_text, (WIN_WIDTH//2 - 80, WIN_HEIGHT//2 - 50))
        win.blit(restart_text, (WIN_WIDTH//2 - 90, WIN_HEIGHT//2))

    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
if serial_connected:
    arduino_serial.close()
pygame.quit()
