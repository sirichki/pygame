import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 10
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong Game")

# Ball properties
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

# Paddle properties
paddle1 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 60, 10, 120)
paddle2 = pygame.Rect(10, HEIGHT // 2 - 60, 10, 120)

# Game variables
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

def display_score():
    score_display = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - 30, 10))

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle2.bottom < HEIGHT:
        paddle2.y += PADDLE_SPEED
    if keys[pygame.K_w] and paddle2.top > 0:
        paddle2.y -= PADDLE_SPEED

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collisions with top and bottom boundaries
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collisions with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1

    # Ball out of bounds (score)
    if ball.left <= 0:
        score1 += 1
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = BALL_SPEED
        ball_speed_y = BALL_SPEED

    if ball.right >= WIDTH:
        score2 += 1
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = -BALL_SPEED
        ball_speed_y = BALL_SPEED

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)

    display_score()

    # Update the display
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()