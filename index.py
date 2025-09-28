import serial
import pygame
import random
import os

# -----------------------------
# Game Config
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
CHARACTER_SIZE = 30
CHARACTER_SPEED = 8
COIN_RADIUS = 15
FPS = 30
TARGET_SCORE = 20  # Win when player collects this many points

# Colors
BLACK = (0, 0, 0)
CHARACTER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 128, 255), (255, 255, 0)]
COIN_COLOR = (255, 215, 0)

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Axis Drift v0.2")
font = pygame.font.Font(None, 36)

# Load sounds
pygame.mixer.init()
coin_sound_path = os.path.join(os.getcwd(), "coin.wav")
try:
    coin_sound = pygame.mixer.Sound(coin_sound_path)
except:
    coin_sound = None
    print("coin.wav not found, sound disabled")

# -----------------------------
# Serial Setup (Arduino)
# -----------------------------
try:
    arduino_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except Exception as e:
    print("Could not connect to Arduino:", e)
    arduino_serial = None

# -----------------------------
# Game Variables
# -----------------------------
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
current_color_index = 0
score = 0

# Coin position
coin_x = random.randint(COIN_RADIUS, WIN_WIDTH - COIN_RADIUS)
coin_y = random.randint(COIN_RADIUS, WIN_HEIGHT - COIN_RADIUS)

# -----------------------------
# Draw Function
# -----------------------------
def draw_window():
    win.fill(BLACK)
    pygame.draw.circle(win, CHARACTER_COLORS[current_color_index], (x, y), CHARACTER_SIZE)
    pygame.draw.circle(win, COIN_COLOR, (coin_x, coin_y), COIN_RADIUS)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (20, 20))
    pygame.display.flip()

# -----------------------------
# Main Game Loop
# -----------------------------
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read sensor data
    if arduino_serial and arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode(errors="ignore").strip().split(',')
            if len(data) == 3:
                xValue, yValue, button = map(int, data)

                # X-axis movement
                if xValue < 400:
                    x -= CHARACTER_SPEED
                elif xValue > 600:
                    x += CHARACTER_SPEED

                # Y-axis movement
                if yValue < 400:
                    y -= CHARACTER_SPEED
                elif yValue > 600:
                    y += CHARACTER_SPEED

                # Button press changes character color (skin switch)
                if button == 1:
                    current_color_index = (current_color_index + 1) % len(CHARACTER_COLORS)

        except ValueError:
            pass

    # Keep character inside screen
    x = max(CHARACTER_SIZE, min(WIN_WIDTH - CHARACTER_SIZE, x))
    y = max(CHARACTER_SIZE, min(WIN_HEIGHT - CHARACTER_SIZE, y))

    # Check for coin collection
    distance = ((x - coin_x) ** 2 + (y - coin_y) ** 2) ** 0.5
    if distance < CHARACTER_SIZE + COIN_RADIUS:
        score += 1
        # Move coin to new random position
        coin_x = random.randint(COIN_RADIUS, WIN_WIDTH - COIN_RADIUS)
        coin_y = random.randint(COIN_RADIUS, WIN_HEIGHT - COIN_RADIUS)
        # Play sound
        if coin_sound:
            coin_sound.play()

    draw_window()

    # Check win condition
    if score >= TARGET_SCORE:
        print("You Win!")
        running = False

    clock.tick(FPS)

pygame.quit()
