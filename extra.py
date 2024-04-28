import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Toss")

font = pygame.font.SysFont(None, 30)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def toss():
    return random.choice(["Team Rocket", "Me(Ash)"])

angle = 0
rotation_speed = 1  # Increased rotation speed
toss_result = None
toss_started = False
spin_duration = 0
current_toss = None

spinner_img = pygame.image.load('Resources/spinner.png')
spinner_img = pygame.transform.scale(spinner_img, (250, 250))

running = True
clock = pygame.time.Clock()

while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not toss_started:
            if event.key == pygame.K_SPACE:
                toss_started = True
                rotation_speed = 8  # Increased rotation speed
                current_toss = toss()  # Start with a random toss

    if toss_started:
        angle += rotation_speed
        angle %= 360

        if rotation_speed > 0:
            spin_duration += 1
            if spin_duration >= 300:  # At least 10 seconds (60 frames per second * 10 seconds)
                rotation_speed = 0
                toss_result = current_toss

        # Change the toss while spinning
        if spin_duration % 15 == 0:  # Change toss every 15 frames
            current_toss = toss()

    spinner_rotated = pygame.transform.rotate(spinner_img, -angle)
    spinner_rect = spinner_rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35))
    window.blit(spinner_rotated, spinner_rect)
    
    if not toss_started:
        draw_text("Press the SPACE button to toss", font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 135)
    elif toss_result is None:
        draw_text("Tossing: " + current_toss, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 135)
    else:
        draw_text("Toss Result: " + toss_result, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 135)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
