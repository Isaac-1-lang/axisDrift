import pygame
import serial
import os
import math

pygame.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("2D Car Driving")

# -----------------------------
# Load background and car
# -----------------------------
bg_path = os.path.abspath("../Downloads/index3.jpeg")
car_path = os.path.abspath("../Downloads/car.png")  # Replace with car sprite

background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

car_img = pygame.image.load(car_path)
CAR_WIDTH, CAR_HEIGHT = 50, 50
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))

# -----------------------------
# Serial (Arduino joystick)
# -----------------------------
arduino_serial = serial.Serial('/dev/ttyACM0', 9600)

# -----------------------------
# Car variables
# -----------------------------
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
angle = 0       # rotation angle
speed = 0
MAX_SPEED = 8
ACCELERATION = 0.5
TURN_SPEED = 3  # degrees per frame

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

            # Map joystick Y-axis to forward/backward
            if yValue < 400:
                speed += ACCELERATION  # forward
            elif yValue > 600:
                speed -= ACCELERATION  # backward
            else:
                speed *= 0.95  # friction

            speed = max(-MAX_SPEED, min(MAX_SPEED, speed))

            # Map joystick X-axis to steering
            if xValue < 400:
                angle += TURN_SPEED
            elif xValue > 600:
                angle -= TURN_SPEED

        except Exception as e:
            pass  # print(e) for debugging

    # -----------------------------
    # Update car position
    # -----------------------------
    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))

    # Keep car inside window
    x = max(0, min(WIN_WIDTH - CAR_WIDTH, x))
    y = max(0, min(WIN_HEIGHT - CAR_HEIGHT, y))

    # -----------------------------
    # Draw everything
    # -----------------------------
    win.blit(background, (0, 0))
    rotated_car = pygame.transform.rotate(car_img, angle)
    rect = rotated_car.get_rect(center=(x + CAR_WIDTH//2, y + CAR_HEIGHT//2))
    win.blit(rotated_car, rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
