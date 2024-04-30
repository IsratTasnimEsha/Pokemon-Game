import pygame
import sys
import cv2

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pokemon Battle")

font = pygame.font.SysFont(None, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button_border(surface, rect, border_color, border_width):
    pygame.draw.rect(surface, border_color, rect, border_width)

def battle_field_screen(player0_numbers, player1_numbers):
    running = True
    selected_field = None
    field_options = ["Electric Field", "Infernal Field", "Aquatic Field"]
    button_images = [
        pygame.transform.scale(pygame.image.load('Resources/electric.png').convert_alpha(), (200, 200)),
        pygame.transform.scale(pygame.image.load('Resources/infernal.png').convert_alpha(), (200, 160)),
        pygame.transform.scale(pygame.image.load('Resources/aquatic.png').convert_alpha(), (200, 180))
    ]
    button_centers = [
        (1145, HEIGHT // 2 - 65),
        (1000, HEIGHT // 2 + 105),
        (1300, HEIGHT // 2 + 105)
    ]
    button_rects = [button.get_rect(center=center) for button, center in zip(button_images, button_centers)]

    background_image = pygame.image.load('Resources/battle_field_board.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
    while running:
        window.fill(WHITE)

        window.blit(background_image, (0, 0))

        player0_image = pygame.image.load('Resources/dashboard_player_0.png')
        player0_image = pygame.transform.scale(player0_image, (145, 180))
        window.blit(player0_image, (252, 50))

        player1_image = pygame.image.load('Resources/dashboard_player_1.png')
        player1_image = pygame.transform.scale(player1_image, (145, 180))
        window.blit(player1_image, (252, 410))

        player_positions = [
            (200, 300), (330, 300), (450, 300),
            (200, 660), (330, 660), (450, 660)
        ]
        for i, player_numbers in enumerate([player0_numbers, player1_numbers]):
            for j, number in enumerate(player_numbers):
                player_image = pygame.image.load(f'Resources/pokemon_{number}.png')
                player_image = pygame.transform.scale(player_image, (100, 100))
                rect = player_image.get_rect(center=player_positions[i * 3 + j])
                window.blit(player_image, rect)
                draw_button_border(window, rect, BLACK, 2)

        draw_text("Choose a battlefield:", font, BLACK, window, 1150, 130)

        for button, rect, field in zip(button_images, button_rects, field_options):
            if selected_field == field:
                draw_button_border(window, rect, BLACK, 3)
            window.blit(button, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for rect, field in zip(button_rects, field_options):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_field = field
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return selected_field

        if selected_field:
            draw_text("Selected Field: " + selected_field, font, BLACK, window, 1150, 650)
            pygame.display.flip()

        pygame.display.flip()

#battle_field_screen([0, 4, 2], [1, 5, 3])