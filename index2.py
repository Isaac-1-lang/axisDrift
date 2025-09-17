import serial
import pygame
import os

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Joystick 2D Game")

# -----------------------------
# Load background and character
# -----------------------------
bg_path = os.path.abspath("../Downloads/index.jpeg")
character_path = os.path.abspath("../Downloads/girl.png")

background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

character_img = pygame.image.load(character_path)
CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
character_img = pygame.transform.scale(character_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

# Starting position
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
CHARACTER_SPEED = 5  # Reduce speed for smoother movement

# -----------------------------
# Serial setup (Arduino)
# -----------------------------
arduino_serial = serial.Serial('/dev/ttyACM0', 9600)

# -----------------------------
# Game loop setup
# -----------------------------
clock = pygame.time.Clock()
running = True

while running:
    # -----------------------------
    # Handle events
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------------------
    # Read joystick data from Arduino
    # -----------------------------
    if arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode().strip().split(',')
            xValue, yValue, button = map(int, data)

            # Map joystick values (0-1023) to smooth movement
            x += (xValue - 512) / 512 * CHARACTER_SPEED
            y += (yValue - 512) / 512 * CHARACTER_SPEED

        except Exception as e:
            pass  # You can print(e) for debugging

    # -----------------------------
    # Set boundaries
    # -----------------------------
    x = max(0, min(WIN_WIDTH - CHARACTER_WIDTH, x))
    y = max(0, min(WIN_HEIGHT - CHARACTER_HEIGHT, y))

    # -----------------------------
    # Draw everything
    # -----------------------------
    win.blit(background, (0, 0))
    win.blit(character_img, (x, y))
    pygame.display.flip()

    # -----------------------------
    # Control frame rate
    # -----------------------------
    clock.tick(60)

# -----------------------------
# Quit Pygame
# -----------------------------
pygame.quit()
