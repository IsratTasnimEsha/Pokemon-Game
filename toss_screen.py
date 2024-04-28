import pygame
import sys
import random
import cv2

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 25)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def toss():
    return random.choice(["Team Rocket", "Me(Ash)"])

def blur_background(image_path, target_size, blur_amount):
    original_image = cv2.imread(image_path)
    resized_image = cv2.resize(original_image, target_size)
    blurred_image = cv2.GaussianBlur(resized_image, (blur_amount, blur_amount), 0)
    blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)
    pygame_surface = pygame.image.frombuffer(blurred_image.flatten(), target_size, 'RGB')
    return pygame_surface

def toss_screen():
    angle = 0
    rotation_speed = 1  
    toss_result = None
    toss_started = False
    spin_duration = 0
    current_toss = None

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Toss Screen")

    blurred_background = blur_background('Resources/field.png', (WIDTH, HEIGHT), 31)

    spinner_img = pygame.image.load('Resources/spinner.png')
    spinner_img = pygame.transform.scale(spinner_img, (250, 250))

    clock = pygame.time.Clock()

    while True:
        window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not toss_started:
                if event.key == pygame.K_SPACE:
                    toss_started = True
                    rotation_speed = 8  
                    current_toss = toss()  

        if toss_started:
            angle += rotation_speed
            angle %= 360

            if rotation_speed > 0:
                spin_duration += 1
                if spin_duration >= 300:  
                    rotation_speed = 0
                    toss_result = current_toss

            if spin_duration % 15 == 0:  
                current_toss = toss()

        window.blit(blurred_background, (0, 0))

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
        
        # Return toss result and exit if toss is complete
        if toss_result is not None:
            pygame.time.delay(2000)
            return toss_result