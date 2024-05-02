import pygame
import sys

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
        pygame.transform.scale(pygame.image.load('Resources/field_electric.png').convert_alpha(), (200, 200)),
        pygame.transform.scale(pygame.image.load('Resources/field_infernal.png').convert_alpha(), (200, 150)),
        pygame.transform.scale(pygame.image.load('Resources/field_aquatic.png').convert_alpha(), (200, 180))
    ]
    button_centers = [
        (750, HEIGHT // 2),
        (500, HEIGHT // 2),
        (1000, HEIGHT // 2)
    ]
    button_rects = [button.get_rect(center=center) for button, center in zip(button_images, button_centers)]

    background_image = pygame.image.load('Resources/board_battle_field.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    player0_image = pygame.image.load('Resources/dashboard_player_0.png')
    player0_image = pygame.transform.scale(player0_image, (280, 360))
    player1_image = pygame.image.load('Resources/dashboard_player_1.png')
    player1_image = pygame.transform.scale(player1_image, (280, 360))

    field_sounds = [
        pygame.mixer.Sound('Resources/sound_electric.mp3'),
        pygame.mixer.Sound('Resources/sound_infernal.mp3'),
        pygame.mixer.Sound('Resources/sound_aquatic.mp3')
    ]

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = False
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_field = field_options[i]
                        clicked = True
                        for j, sound in enumerate(field_sounds):
                            if j == i:
                                sound.play()
                            else:
                                sound.stop()
                if not clicked:
                    selected_field = None
                    for sound in field_sounds:
                        sound.stop()
            elif event.type == pygame.KEYDOWN:  
                if selected_field is not None: 
                    for sound in field_sounds:
                        sound.stop() 
                    return selected_field

        window.fill(WHITE)
        window.blit(background_image, (0, 0))

        window.blit(player0_image, (40, 40))
        window.blit(player1_image, (1180, 370))

        player_positions = [
            (390, 100), (520, 100), (650, 100),
            (850, 670), (980, 670), (1110, 670)
        ]
        for i, player_numbers in enumerate([player0_numbers, player1_numbers]):
            for j, number in enumerate(player_numbers):
                player_image = pygame.image.load(f'Resources/pokemon_{number}.png')
                player_image = pygame.transform.scale(player_image, (120, 120))
                rect = player_image.get_rect(center=player_positions[i * 3 + j])
                window.blit(player_image, rect)
                draw_button_border(window, rect, BLACK, 2)

        draw_text("Choose a battlefield:", font, BLACK, window, WIDTH // 2, HEIGHT // 2 - 160)

        for button, rect, field in zip(button_images, button_rects, field_options):
            if selected_field == field:
                draw_button_border(window, rect, BLACK, 3)
            window.blit(button, rect)

        if selected_field:
            draw_text("Selected Field: " + selected_field, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 160)
            pygame.display.flip()

        pygame.display.flip()

#battle_field_screen([0, 4, 2], [1, 5, 3])