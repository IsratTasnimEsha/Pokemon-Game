import pygame
import sys
import random
import cv2

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 50)
spinner_sound = pygame.mixer.Sound('Resources/sound_spinner.mp3')

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def toss():
    return random.choice(["Me(Ash)", "Team Rocket"])

def toss_screen():
    angle = 0
    rotation_speed = 1  
    toss_result = None
    toss_started = False
    spin_duration = 0
    current_toss = None

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Toss Screen")
 
    background_image = pygame.image.load('Resources/board_toss.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    spinner_img = pygame.image.load('Resources/spinner_toss.png')
    spinner_img = pygame.transform.scale(spinner_img, (350, 350))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not toss_started:   
                toss_started = True
                rotation_speed = 10 
                current_toss = toss()  
                spinner_sound.play() 

        if toss_started:
            angle += rotation_speed
            angle %= 360

            if rotation_speed > 0:
                spin_duration += 1
                if spin_duration >= 200:  
                    rotation_speed = 0
                    toss_result = current_toss
                    spinner_sound.stop() 
                    
            if spin_duration % 15 == 0:  
                current_toss = toss()

        window.fill(WHITE)
        window.blit(background_image, (0, 0))

        spinner_rotated = pygame.transform.rotate(spinner_img, -angle)
        spinner_rect = spinner_rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 55))
        window.blit(spinner_rotated, spinner_rect)
        
        if not toss_started:
            draw_text("Press any button to toss", font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 170)
        elif toss_result is None:
            draw_text("Tossing: " + current_toss, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 170)
        else:
            draw_text("Toss Result: " + toss_result, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 170)

        pygame.display.flip()
        clock.tick(60)
        
        if toss_result is not None:
            pygame.time.delay(2000)
            return toss_result

#toss_screen()