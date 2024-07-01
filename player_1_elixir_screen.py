import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pokemon Battle")

font1 = pygame.font.SysFont("comicsansms", 25)
font2 = pygame.font.SysFont("comicsansms", 20)
font3 = pygame.font.SysFont("comicsansms", 30)

player1_best_elixirs = [0, 0, 0, 0, 0]

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button_border(surface, rect, border_color, border_width):
    pygame.draw.rect(surface, border_color, rect, border_width)

def draw_text_with_outline(text, font, text_color, outline_color, surface, x, y):
    # Render the outline text
    outline_text = font.render(text, True, outline_color)
    outline_rect = outline_text.get_rect(center=(x, y))

    # Render the main text
    main_text = font.render(text, True, text_color)
    main_rect = main_text.get_rect(center=(x, y))

    # Draw the outline by offsetting the text
    offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for offset in offsets:
        surface.blit(outline_text, (outline_rect.x + offset[0], outline_rect.y + offset[1]))

    # Draw the main text on top
    surface.blit(main_text, main_rect)

def player_1_elixir_screen():
    running = True

    background_image = pygame.image.load('Resources/board_elixir.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    owned_image = pygame.image.load('Resources/elixir_owned.png')
    owned_images = []
    owned_images_sizes = [(190, 335), (150 ,335), (145 ,335), (118 ,335), (174 ,335)]
    for i in range(5):
        owned_images.append(pygame.transform.scale(owned_image, owned_images_sizes[i]))    

    elixir_positions = [(352, 180), (556, 180), (720, 180), (880, 180), (1015, 180)]

    elixir_rects = []
    elixir_rects = [pygame.Rect(pos, (owned_images_sizes[i][0], owned_images_sizes[i][1])) for i, pos in enumerate(elixir_positions)]

    elixir_price_power = [
        (random.randint(1, 10), random.randint(5, 20)), (random.randint(1, 10), random.randint(5, 20)), 
        (random.randint(1, 10), random.randint(5, 20)), (random.randint(1, 10), random.randint(5, 20)), 
        (random.randint(1, 10), random.randint(5, 20))
    ]

    total_prices = 0
    for i, j in elixir_price_power:
        total_prices += i
    
    remaining = int(0.5 * total_prices)
    remaining_original = int(0.5 * total_prices)

    clicked_positions = [False] * 5
    sum_of_power = 0

    def draw_static_elements():
        window.fill(WHITE)
        window.blit(background_image, (0, 0))
        
        draw_text_with_outline(f"Price: {elixir_price_power[0][0]}$", font2, WHITE, BLACK, window, 447, 145)
        draw_text_with_outline(f"Price: {elixir_price_power[1][0]}$", font2, WHITE, BLACK, window, 640, 145)
        draw_text_with_outline(f"Price: {elixir_price_power[2][0]}$", font2, WHITE, BLACK, window, 795, 145)
        draw_text_with_outline(f"Price: {elixir_price_power[3][0]}$", font2, WHITE, BLACK, window, 940, 145)
        draw_text_with_outline(f"Price: {elixir_price_power[4][0]}$", font2, WHITE, BLACK, window, 1095, 145)

        draw_text_with_outline(f"Power: {elixir_price_power[0][1]}", font1, WHITE, BLACK, window, 447, 100)
        draw_text_with_outline(f"Power: {elixir_price_power[1][1]}", font1, WHITE, BLACK, window, 640, 100)
        draw_text_with_outline(f"Power: {elixir_price_power[2][1]}", font1, WHITE, BLACK, window, 795, 100)
        draw_text_with_outline(f"Power: {elixir_price_power[3][1]}", font1, WHITE, BLACK, window, 940, 100)
        draw_text_with_outline(f"Power: {elixir_price_power[4][1]}", font1, WHITE, BLACK, window, 1095, 100)
        
        draw_text_with_outline(f"Remaining:", font2, WHITE, BLACK, window, 1270, 330)
        draw_text_with_outline(f"{remaining}", font3, WHITE, BLACK, window, 1270, 370)

        draw_text_with_outline(f"Power:", font2, WHITE, BLACK, window, 1270, 430)
        draw_text_with_outline(f"{sum_of_power}", font3, WHITE, BLACK, window, 1270, 470)

        # Redraw the owned images
        for i, clicked in enumerate(clicked_positions):
            if clicked:
                window.blit(owned_images[i], elixir_positions[i])

    draw_static_elements()

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(elixir_rects):
                        if rect.collidepoint(mouse_x, mouse_y) and not clicked_positions[i]:
                                
                            if (remaining - elixir_price_power[i][0]) < 0:
                                pygame.time.delay(2000)  # Delay before returning
                                return elixir_price_power, remaining_original, player1_best_elixirs

                            clicked_positions[i] = True
                            player1_best_elixirs[i] = 1
                            remaining -= elixir_price_power[i][0]
                            sum_of_power += elixir_price_power[i][1]
                            draw_static_elements()
                            window.blit(owned_images[i], elixir_positions[i])

                            if (remaining - elixir_price_power[i][0]) == 0:
                                pygame.time.delay(2000)  # Delay before returning
                                return elixir_price_power, remaining_original, player1_best_elixirs

        pygame.display.flip()

#player_1_elixir_screen()