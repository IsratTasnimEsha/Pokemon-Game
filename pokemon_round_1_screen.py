import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_alert_message(window, message, font, color, bg_color, x, y, width, height):
    pygame.draw.rect(window, bg_color, (x - width // 2, y - height // 2, width, height))
    draw_text(message, font, color, window, x, y)

background_image = pygame.image.load('Resources/board_pokemon.jpg')
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

def pokemon_round_1_screen(player0_numbers, player1_numbers, round_1_pokemon0):

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Toss Screen")

    pokemon_buttons0 = []
    pokemon_buttons1 = []
    for i in range(3):
        if player0_numbers[i] == round_1_pokemon0:
                pokemon_button = {
                'number': player0_numbers[i],
                'rect': pygame.Rect(115 + i * 125, 480, 105, 105),
                'image': pygame.image.load(f'Resources/pokemon_{player0_numbers[i]}.png'),
                'color': RED
            }
        else:
            pokemon_button = {
                'number': player0_numbers[i],
                'rect': pygame.Rect(115 + i * 125, 480, 105, 105),
                'image': pygame.image.load(f'Resources/pokemon_{player0_numbers[i]}.png'),
                'color': WHITE
            }
        pokemon_buttons0.append(pokemon_button)

    for i in range(3):
        pokemon_button = {
            'number': player1_numbers[i],
            'rect': pygame.Rect(1030 + i * 125, 480, 105, 105),
            'image': pygame.image.load(f'Resources/pokemon_{player1_numbers[i]}.png'),
            'color': WHITE 
        }
        pokemon_buttons1.append(pokemon_button)

    while True:
        window.fill(WHITE)

        window.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in pokemon_buttons1:
                        if button['rect'].collidepoint(event.pos):
                            round_1_pokemon1 = button['number']
                            for b in pokemon_buttons1:
                                b['color'] = WHITE
                            button['color'] = BLUE
            elif event.type == pygame.KEYDOWN:    
                return round_1_pokemon1

        window.blit(background_image, (0, 0))

        draw_alert_message(window, "Choose the pokemon for round-1 battle", font, WHITE, (0, 0, 0), WIDTH // 2, HEIGHT // 2, 700, 70)

        player0_image = pygame.image.load('Resources/dashboard_player_0.png')
        player0_image = pygame.transform.scale(player0_image, (240, 300))
        window.blit(player0_image, (177, 160))

        player1_image = pygame.image.load('Resources/dashboard_player_1.png')
        player1_image = pygame.transform.scale(player1_image, (240, 300))
        window.blit(player1_image, (1090, 160))

        for button in pokemon_buttons0:
            pokemon_image = pygame.transform.scale(button['image'], (105, 105))
            pokemon_image.fill(button['color'], None, pygame.BLEND_RGBA_MULT)
            window.blit(pokemon_image, button['rect'].topleft)
            border_width = 3
            pygame.draw.rect(window, BLACK, button['rect'], border_width)

        for button in pokemon_buttons1:
            pokemon_image = pygame.transform.scale(button['image'], (105, 105))
            pokemon_image.fill(button['color'], None, pygame.BLEND_RGBA_MULT)
            window.blit(pokemon_image, button['rect'].topleft)
            border_width = 3
            pygame.draw.rect(window, BLACK, button['rect'], border_width)

        pygame.display.flip()

#print("round_1_pokemon1", pokemon_round_1_screen([5, 0, 4], [1, 3, 2], 4))