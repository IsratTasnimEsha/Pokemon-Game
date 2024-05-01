import pygame
import sys
import random
import cv2

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 30)

pygame.mixer.init()
spinner_sound = pygame.mixer.Sound('Resources/sound_spinner.mp3')

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_alert_message(window, message, font, color, bg_color, x, y, width, height):
    pygame.draw.rect(window, bg_color, (x - width // 2, y - height // 2, width, height))
    draw_text(message, font, color, window, x, y)

background_image = pygame.image.load('Resources/board_pokemon.jpg')
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

spinner_img0 = pygame.image.load('Resources/spinner_pokemon_0.png')
spinner_img0 = pygame.transform.scale(spinner_img0, (190, 190))
spinner_img1 = pygame.image.load('Resources/spinner_pokemon_1.png')
spinner_img1 = pygame.transform.scale(spinner_img1, (190, 190))

def pokemon_screen():
    toss_count = 0
    player0_numbers = []
    player1_numbers = []

    while toss_count < 3:
        angle0 = 0
        angle1 = 0
        rotation_speed0 = 1  
        rotation_speed1 = 1  
        toss_result0 = None
        toss_result1 = None
        toss_started0 = False
        toss_started1 = False
        spin_duration0 = 0
        spin_duration1 = 0
        current_toss0 = None
        current_toss1 = None
        show_alert = True  
        alert_timer = 1000

        window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Toss Screen")

        clock = pygame.time.Clock()

        while True:
            window.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and not toss_started0 and not toss_started1:
                    toss_started0 = True
                    toss_started1 = True
                    rotation_speed0 = 30
                    rotation_speed1 = 30  
                    current_toss0 = random.randint(0, 5)
                    while current_toss0 in player0_numbers:
                        current_toss0 = random.randint(0, 5)
                    current_toss1 = random.randint(0, 5)
                    while current_toss1 in player1_numbers:
                        current_toss1 = random.randint(0, 5)
                    spinner_sound.play()         

            if toss_started0:
                angle0 += rotation_speed0
                angle0 %= 360
                spin_duration0 += 1  

                if rotation_speed0 > 0:
                    if spin_duration0 >= 10:  
                        rotation_speed0 = 0
                        toss_result0 = current_toss0
                        spinner_sound.stop() 

                    if spin_duration0 % 15 == 0:   
                        current_toss0 = random.randint(0, 5)
                        while current_toss0 in player0_numbers:
                            current_toss0 = random.randint(0, 5)
                        

            if toss_started1:
                angle1 += rotation_speed1
                angle1 %= 360
                spin_duration1 += 1  

                if rotation_speed1 > 0:
                    if spin_duration1 >= 10:  
                        rotation_speed1 = 0
                        toss_result1 = current_toss1
                        spinner_sound.stop()
                        
                    if spin_duration1 % 15 == 0:  
                        current_toss1 = random.randint(0, 5)
                        while current_toss1 in player1_numbers:
                            current_toss1 = random.randint(0, 5)

            window.blit(background_image, (0, 0))

            player0_image = pygame.image.load('Resources/dashboard_player_0.png')
            player0_image = pygame.transform.scale(player0_image, (240, 300))
            window.blit(player0_image, (177, 160))

            player1_image = pygame.image.load('Resources/dashboard_player_1.png')
            player1_image = pygame.transform.scale(player1_image, (240, 300))
            window.blit(player1_image, (1090, 160))

            pokemon_image0 = []
            pokemon_image1 = []
            
            for i in range(3):
                if toss_count > i:
                    pokemon_number = player0_numbers[i]
                    pokemon_image = pygame.image.load(f'Resources/pokemon_{pokemon_number}.png')
                else:
                    pokemon_image = pygame.image.load('Resources/pokemon_blank.png')
                
                pokemon_image = pygame.transform.scale(pokemon_image, (105, 105))
                x = 115 + i * 125
                y = 480
                window.blit(pokemon_image, (x, y))
                border_width = 3
                pygame.draw.rect(window, BLACK, (x - border_width, y - border_width, 105 + 2 * border_width, 105 + 2 * border_width), border_width)

            for i in range(3):
                if toss_count > i:
                    pokemon_number = player1_numbers[i]
                    pokemon_image = pygame.image.load(f'Resources/pokemon_{pokemon_number}.png')
                else:
                    pokemon_image = pygame.image.load('Resources/pokemon_blank.png')
                
                pokemon_image = pygame.transform.scale(pokemon_image, (105, 105))
                x = 1030 + i * 125
                y = 480
                window.blit(pokemon_image, (x, y))
                border_width = 3
                pygame.draw.rect(window, BLACK, (x - border_width, y - border_width, 105 + 2 * border_width, 105 + 2 * border_width), border_width)

            spinner_rotated0 = pygame.transform.rotate(spinner_img0, -angle0)
            spinner_rect0 = spinner_rotated0.get_rect(center=(WIDTH // 2, HEIGHT// 2 - 200))
            window.blit(spinner_rotated0, spinner_rect0)
            
            spinner_rotated1 = pygame.transform.rotate(spinner_img1, -angle1)
            spinner_rect1 = spinner_rotated1.get_rect(center=(WIDTH // 2, HEIGHT// 2 + 200))
            window.blit(spinner_rotated1, spinner_rect1)
            
            if not toss_started0 and not toss_started1:
                if show_alert:
                    draw_alert_message(window, "Press any button to toss", font, WHITE, (0, 0, 0, 255), WIDTH // 2, HEIGHT // 2, 300, 50)
                    alert_timer -= 1
                    if alert_timer <= 0:
                        show_alert = False

            if toss_result0 != None:
                player0_numbers.append(toss_result0)
                pokemon_image = pygame.image.load(f'Resources/pokemon_{player0_numbers[toss_count]}.png')
                pokemon_image = pygame.transform.scale(pokemon_image, (105, 105))
                window.blit(pokemon_image, (115 + toss_count * 125, 480))

            if toss_result1 != None:
                player1_numbers.append(toss_result1)
                pokemon_image = pygame.image.load(f'Resources/pokemon_{player1_numbers[toss_count]}.png')
                pokemon_image = pygame.transform.scale(pokemon_image, (105, 105))
                window.blit(pokemon_image, (1030 + toss_count * 125, 480))

            pygame.display.flip()
            clock.tick(60)
            
            if toss_result0 is not None and toss_result1 is not None:
                break
                
        toss_count += 1

    pygame.time.delay(4000)
    return player0_numbers, player1_numbers

#player0_numbers, player1_numbers = pokemon_screen()