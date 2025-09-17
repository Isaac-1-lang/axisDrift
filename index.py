import serial
import pygame

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Joystick Control")

# -----------------------------
# Character setup
# -----------------------------
CHARACTER_SIZE = 50
CHARACTER_COLOR = (255, 0, 0)
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
CHARACTER_SPEED = 10

# -----------------------------
# Serial setup
# -----------------------------
# Make sure the COM port matches your Arduino
arduino_serial = serial.Serial('/dev/ttyACM0', 9600)

# -----------------------------
# Game loop setup
# -----------------------------
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick data from Arduino
    if arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode().strip().split(',')
            xValue, yValue, button = map(int, data)

            # Map joystick values to character movement
            if xValue < 400:
                x -= CHARACTER_SPEED
            elif xValue > 600:
                x += CHARACTER_SPEED

            if yValue < 400:
                y -= CHARACTER_SPEED
            elif yValue > 600:
                y += CHARACTER_SPEED

        except Exception as e:
            # You can print(e) for debugging
            pass
    #Set boundaries
    x=max(CHARACTER_SIZE, min(WIN_WIDTH - CHARACTER_SIZE, x))
    y=max(CHARACTER_SIZE, min(WIN_HEIGHT - CHARACTER_SIZE, y))
    # Draw everything
    win.fill((0, 0, 0))  # Clear screen with black
    pygame.draw.circle(win, CHARACTER_COLOR, (x, y), CHARACTER_SIZE)
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
