import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (0, 0, 255, 0)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pokemon Battle")

font = pygame.font.SysFont(None, 25)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button_border(surface, rect, border_color, border_width):
    pygame.draw.rect(surface, border_color, rect, border_width)

def play_screen(toss_result, selected_field, player0_numbers, player1_numbers, round_1_pokemon0, round_1_pokemon1, round_2_pokemon0, round_2_pokemon1):
    running = True

    current_attack_choose_button_clicked0 = None
    current_attack_choose_button_clicked1 = None

    background_image = pygame.image.load('Resources/water.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    player0_image = pygame.image.load('Resources/player_0.png')
    player0_image = pygame.transform.scale(player0_image, (280, 400))

    player1_image = pygame.image.load('Resources/player_1.png')
    player1_image = pygame.transform.scale(player1_image, (200, 300))

    pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon0}_fight_0.png')
    pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (150, 180))

    pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon1}_fight_1.png')
    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (150, 180))

    player0_attack = pygame.image.load('Resources/player_0_attack.png')
    player0_attack = pygame.transform.scale(player0_attack, (150, 55))

    player0_defence = pygame.image.load('Resources/player_0_defence.png')
    player0_defence = pygame.transform.scale(player0_defence, (150, 55))

    player0_power = pygame.image.load('Resources/player_0_power.png')
    player0_power = pygame.transform.scale(player0_power, (150, 55))

    player1_attack = pygame.image.load('Resources/player_1_attack.png')
    player1_attack = pygame.transform.scale(player1_attack, (150, 55))

    player1_defence = pygame.image.load('Resources/player_1_defence.png')
    player1_defence = pygame.transform.scale(player1_defence, (150, 55))

    player1_power = pygame.image.load('Resources/player_1_power.png')
    player1_power = pygame.transform.scale(player1_power, (150, 55))

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            

            window.fill(WHITE)
            window.blit(background_image, (0, 0))

            window.blit(player0_image, (20, 100))
            window.blit(player1_image, (WIDTH - 280, 150))

            window.blit(pokemon_fight_image0, (300, 305))
            window.blit(pokemon_fight_image1, (WIDTH-400, 305))

            window.blit(player0_attack, (260, 680))
            window.blit(player0_defence, (420, 680))
            window.blit(player0_power, (580, 680))

            window.blit(player1_attack, (260, 680))
            window.blit(player1_defence, (420, 680))
            window.blit(player1_power, (WIDTH - 20, 680))

            pygame.display.flip()


#play_screen('Team_Rocket', random.choice(["Electric Field", "Infernal Field", "Aquatic Field"]), [0, 1, 2], [3, 4, 5], 1, 5, None, None)