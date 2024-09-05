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
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(x, y + i * font.get_linesize()))
        surface.blit(text_surface, text_rect)

def pseudo_blur(image, scale_factor=0.1):
    small_image = pygame.transform.smoothscale(image, (int(WIDTH * scale_factor), int(HEIGHT * scale_factor)))
    blurred_image = pygame.transform.smoothscale(small_image, (WIDTH, HEIGHT))
    return blurred_image

def announcement_screen(announcement):
    running = True

    background_image = pygame.image.load('Resources/board_announcement.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    background_image = pseudo_blur(background_image)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= mouse_x <= 1500 and 0 <= mouse_y <= 770:
                    return

        window.fill(WHITE)
        window.blit(background_image, (0, 0))

        if announcement == "pokemon_find":
            draw_text('''
                Ash, here's what you need to do:\n
                1. Catch Pikachu first (you know where it is).
                2. Get Charmander's location from Nurse Joy after catching Pikachu.
                3. Get Squirtle's location from Nurse Joy after catching Charmander.
                4. Use your 15 liters of fuel wisely for each Pokémon.
                5. Traveling between locations will cost 1 millisecond per unit of distance.
                6. Catch all Pokémon within 1 minute.\n
                Good luck!
                ''',
                font, BLACK, window, WIDTH // 2 - 70, HEIGHT // 4)
        if announcement == "player_1_elixir":
            draw_text('''
                Ash, here's what you need to know about elixirs:\n
                1. Use coins to buy elixirs with the highest power to strengthen your Pokémon in battles.
                2. Strategize your purchases to get the most powerful elixirs within your coin limit.
                3. Team Rocket will use a genetic algorithm to buy elixirs, so choose wisely.\n
                Good luck!
                ''',
                font, BLACK, window, WIDTH // 2 - 40, HEIGHT // 3)
        if announcement == "player_0_elixir":
            draw_text('''
                Team Rocket will use a genetic algorithm to buy elixirs with same amount of coins.
                ''',
                font, BLACK, window, WIDTH // 2 - 40, HEIGHT // 2 - 20)
        if announcement == "play":
            draw_text('''
                Ash, here are the battle rules:\n
                1. Choose between action or defense each turn.
                2. Match your Pokémon's type to the field type for more damage.
                3. Fire beats Electric, Electric beats Water, Water beats Fire.
                4. You can switch Pokémon if their health isn't zero.
                5. Boost your Pokémon's health with elixirs when needed.
                6. Team Rocket uses fuzzy logic to use elixirs or swap Pokémon.
                7. Team Rocket uses minimax algorithm for decisions.\n
                Get ready for battle!
                ''',
                font, BLACK, window, WIDTH // 2 - 70, HEIGHT // 4)
        
        pygame.display.flip()

#announcement_screen("play")