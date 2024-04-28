import pygame
import sys
import random
import cv2

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)  # New color for selected field

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pokemon Battle")

font = pygame.font.SysFont(None, 25)  # Adjusted font size

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def blur_background(image_path, target_size, blur_amount):
    original_image = cv2.imread(image_path)
    resized_image = cv2.resize(original_image, target_size)
    blurred_image = cv2.GaussianBlur(resized_image, (blur_amount, blur_amount), 0)
    blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)
    pygame_surface = pygame.image.frombuffer(blurred_image.flatten(), target_size, 'RGB')
    return pygame_surface

def battle_field_screen(toss_result):
    running = True
    selected_field = None
    field_options = ["Aquatic Field", "Infernal Field", "Electric Field"]

    # Load and blur the background image
    background_image = blur_background('Resources/field.png', (WIDTH, HEIGHT), 31)

    while running:
        window.fill(WHITE)

        # Draw the blurred background image
        window.blit(background_image, (0, 0))

        draw_text("Choose a battlefield:", font, BLACK, window, WIDTH // 2, 220)

        # Display field options
        for i, field in enumerate(field_options):
            text_color = BLACK
            if selected_field == field:
                text_color = GRAY  # Change color if field is selected
            draw_text(field, font, text_color, window, WIDTH // 2, 280 + i * 60)  # Adjust y-coordinate for spacing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, field in enumerate(field_options):
                    if WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and 250 + i * 60 - 25 <= mouse_y <= 250 + i * 60 + 25:  # Adjusted y-coordinate range
                        selected_field = field

        if selected_field:
            draw_text("Selected Field: " + selected_field, font, BLACK, window, WIDTH // 2, 500)
            pygame.display.flip()
            pygame.time.delay(2000)
            return selected_field

        pygame.display.flip()
