import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pokemon Battle")

font = pygame.font.SysFont("comicsansms", 25)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button_border(surface, rect, border_color, border_width):
    pygame.draw.rect(surface, border_color, rect, border_width)

def result_pokemon_find_screen(winner):
    running = True

    background_image = pygame.image.load('Resources/board_battle_field.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    player0_image = pygame.image.load('Resources/dashboard_player_0.png')
    player0_image = pygame.transform.scale(player0_image, (320, 420))
    player1_image = pygame.image.load('Resources/dashboard_player_1.png')
    player1_image = pygame.transform.scale(player1_image, (320, 420))

    congrats_image = pygame.image.load('Resources/result_congrats.png')
    congrats_image = pygame.transform.scale(congrats_image, (500, 280))
    pokemon_master_image = pygame.image.load('Resources/result_pokemon_master.png')
    pokemon_master_image = pygame.transform.scale(pokemon_master_image, (250, 250))
    draw_image = pygame.image.load('Resources/result_draw.png')
    draw_image = pygame.transform.scale(draw_image, (350, 200))

    while running:
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

        window.blit(player0_image, (170, 190))
        window.blit(player1_image, (980, 190))

        if winner == "Me(Ash)":
            window.blit(congrats_image, (900, 25))
            window.blit(pokemon_master_image, (1015, 550))
        elif winner == "Team Rocket":
            window.blit(congrats_image, (90, 25))
            window.blit(pokemon_master_image, (205, 550))
        elif winner == "Draw":
            window.blit(draw_image, (565, 280))
        
        pygame.display.flip()

        pygame.time.wait(5000)
        return

#result_pokemon_find_screen("Draw")