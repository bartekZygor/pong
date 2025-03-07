import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 12
BALL_SIZE = 20
FPS = 60

# Game settings
speed_increment_threshold = 5
speed_increment_factor = 1.05
initial_velocity = 3

# Initialize variables
player_pos = [SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 20]
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_velocity = [random.choice([initial_velocity, -initial_velocity]),
                 random.choice([initial_velocity, -initial_velocity])]

shadow_positions = []
score = 0
game_over = False

# Pygame settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
fps_font = pygame.font.SysFont(None, 18)
game_over_font = pygame.font.SysFont(None, 64)

# Reset game function
def reset_game():
    global player_pos, ball_pos, ball_velocity, shadow_positions, score, game_over
    player_pos = [SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 20]
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    ball_velocity = [random.choice([initial_velocity, -initial_velocity]),
                     random.choice([initial_velocity, -initial_velocity])]
    shadow_positions = []
    score = 0
    game_over = False

# Draw game elements
def draw_elements(fps):
    screen.fill(BLACK)
    
    if not game_over:
        # Draw shadow trail
        for i, pos in enumerate(reversed(shadow_positions)):
            alpha = max(180 - i * 40, 0)
            shadow_surface = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (150, 150, 150, alpha), (0, 0, BALL_SIZE, BALL_SIZE))
            screen.blit(shadow_surface, pos)
        
        # Draw ball
        pygame.draw.ellipse(screen, WHITE, (*ball_pos, BALL_SIZE, BALL_SIZE))
        
        # Draw paddle
        pygame.draw.rect(screen, WHITE, (*player_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
        
        # Draw score
        score_surface = font.render(str(score), True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(score_surface, score_rect)
        
        # Draw FPS counter
        fps_surface = fps_font.render(f"FPS: {fps:.0f}", True, WHITE)
        screen.blit(fps_surface, (5, 5))
    else:
        # Game over screen
        game_over_surface = game_over_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.flip()

# Main game loop
running = True
while running:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_pos[0] > 0:
            player_pos[0] -= 300 * delta_time
        if keys[pygame.K_d] and player_pos[0] < SCREEN_WIDTH - PADDLE_WIDTH:
            player_pos[0] += 300 * delta_time

        # Ball movement
        ball_pos[0] += ball_velocity[0] * delta_time * FPS
        ball_pos[1] += ball_velocity[1] * delta_time * FPS

        # Ball collision with walls
        if ball_pos[0] <= 0 or ball_pos[0] >= SCREEN_WIDTH - BALL_SIZE:
            ball_velocity[0] = -ball_velocity[0]
        if ball_pos[1] <= 0:
            ball_velocity[1] = -ball_velocity[1]

        # Ball collision with paddle
        if (player_pos[1] < ball_pos[1] + BALL_SIZE <= player_pos[1] + PADDLE_HEIGHT and
            player_pos[0] <= ball_pos[0] <= player_pos[0] + PADDLE_WIDTH):
            ball_velocity[1] = -abs(ball_velocity[1])  # Ensure upward movement
            score += 1
            if score % speed_increment_threshold == 0:
                ball_velocity[0] *= speed_increment_factor
                ball_velocity[1] *= speed_increment_factor

        # Additional collision check for missed frames
        elif (ball_pos[1] + BALL_SIZE > player_pos[1] and
              ball_velocity[1] > 0 and
              player_pos[0] <= ball_pos[0] <= player_pos[0] + PADDLE_WIDTH):
            ball_velocity[1] = -abs(ball_velocity[1])

        # Ball out of bounds
        if ball_pos[1] > SCREEN_HEIGHT:
            game_over = True

        # Update shadow trail
        shadow_positions.append(ball_pos[:])
        if len(shadow_positions) > 5:
            shadow_positions.pop(0)

    fps = clock.get_fps()
    draw_elements(fps)

pygame.quit()
sys.exit()
