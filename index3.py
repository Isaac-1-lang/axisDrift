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
pygame.display.set_caption("Joystick 2D Shooter")

# -----------------------------
# Load background and character
# -----------------------------
bg_path = os.path.abspath("./assets/index.jpeg")
character_path = os.path.abspath("./assets/girl.png")

background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
character_img = pygame.image.load(character_path)
character_img = pygame.transform.scale(character_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

# -----------------------------
# Serial setup (Arduino)
# -----------------------------
arduino_serial = serial.Serial('/dev/ttyACM0', 9600)

# -----------------------------
# Game variables
# -----------------------------
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
CHARACTER_SPEED = 5
bullets = []
BULLET_SPEED = 10

# -----------------------------
# Game loop setup
# -----------------------------
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------------------
    # Read joystick data
    # -----------------------------
    if arduino_serial.in_waiting > 0:
        try:
            data = arduino_serial.readline().decode().strip().split(',')
            xValue, yValue, button = map(int, data)

            # Smooth movement
            x += (xValue - 512) / 512 * CHARACTER_SPEED
            y += (yValue - 512) / 512 * CHARACTER_SPEED
            print("X:", xValue, "Y:", yValue, "Button:", button)

            # Fire bullet when button pressed
            if button == 1:
                # Bullet starts from character center
                bullets.append([x + CHARACTER_WIDTH // 2, y + CHARACTER_HEIGHT // 2])

        except Exception as e:
            pass  # print(e) for debugging

    # -----------------------------
    # Set boundaries
    # -----------------------------
    x = max(0, min(WIN_WIDTH - CHARACTER_WIDTH, x))
    y = max(0, min(WIN_HEIGHT - CHARACTER_HEIGHT, y))

    # -----------------------------
    # Update bullets
    # -----------------------------
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED  # Move bullet up
        if bullet[1] < 0:
            bullets.remove(bullet)

    # -----------------------------
    # Draw everything
    # -----------------------------
    win.blit(background, (0, 0))
    win.blit(character_img, (x, y))

    for bullet in bullets:
        pygame.draw.circle(win, (255, 255, 0), bullet, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
