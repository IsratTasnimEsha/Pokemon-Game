import pygame
import sys
import random
import cv2

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255, 128)
RED = (255, 0, 0, 128)

def generate_random_positions(num_images, existing_positions):
    positions = []
    while len(positions) < num_images:
        x = random.randint(260, WIDTH - 360)
        y = random.randint(180, HEIGHT - 150)
        
        new_position = (x, y)
        overlap = False
        for pos in existing_positions:
            if abs(pos[0] - x) < 150 and abs(pos[1] - y) < 150:
                overlap = True
                break
        if not overlap:
            positions.append(new_position)
            existing_positions.append(new_position)
    return positions

def draw_field_images(field_image, window, positions):
    for x, y in positions:
        window.blit(field_image, (x, y))

font = pygame.font.SysFont(None, 20)

attack_choose_button_x_start0 = 20
attack_choose_button_y_start0 = 600

attack_choose_button_x_start1 = 1260
attack_choose_button_y_start1 = 600

attack_choose_button_width, attack_choose_button_height = 105, 50
attack_choose_button_spacing = 10

def draw_attack_choose_buttons(window, attack_choose_button_texts, attack_choose_button_x_start, attack_choose_button_y_start, current_button_clicked):
    for i in range(2):
        for j in range(2):
            text = attack_choose_button_texts[i * 2 + j]
            attack_choose_button_rect = pygame.Rect(attack_choose_button_x_start + j * (attack_choose_button_width + attack_choose_button_spacing), attack_choose_button_y_start + i * (attack_choose_button_height + attack_choose_button_spacing), attack_choose_button_width, attack_choose_button_height)

            color = BLUE if current_button_clicked == i * 2 + j else GRAY 
            pygame.draw.rect(window, color, attack_choose_button_rect)
            pygame.draw.rect(window, BLACK, attack_choose_button_rect, 2) 

            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=attack_choose_button_rect.center)
            window.blit(text_surface, text_rect)

def play_screen(toss_result, selected_field, player0_numbers, player1_numbers, round_1_pokemon0, round_1_pokemon1, round_2_pokemon0, round_2_pokemon1):
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Play Screen")

    background_image = pygame.image.load('Resources/board_play.png')
    background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

    running = True

    current_attack_choose_button_clicked0 = None
    current_attack_choose_button_clicked1 = None

    while running:
        window.blit(background_image, (0, 0))

        player0_image = pygame.image.load('Resources/player_0.png')
        player0_image = pygame.transform.scale(player0_image, (250, 350))
        window.blit(player0_image, (50, 130))

        player1_image = pygame.image.load('Resources/player_1.png')
        player1_image = pygame.transform.scale(player1_image, (170, 290))
        window.blit(player1_image, (1210, 180))

        pokemon_button_images0 = []
        pokemon_button_images1 = []
        for i in player0_numbers:
            pokemon_button_image = pygame.image.load(f'Resources/pokemon_{i}.png')
            pokemon_button_image_scaled0 = pygame.transform.scale(pokemon_button_image, (65, 65))
            pokemon_button_images0.append((pokemon_button_image_scaled0, i))
        for i in player1_numbers:
            pokemon_button_image = pygame.image.load(f'Resources/pokemon_{i}.png')
            pokemon_button_image_scaled1 = pygame.transform.scale(pokemon_button_image, (65, 65))
            pokemon_button_images1.append((pokemon_button_image_scaled1, i))

        pokemon_fight_images0 = []
        pokemon_fight_images1 = []
        for i in player0_numbers:
            pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{i}_fight_0.png')
            if i<3:
                pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))
            else: 
                pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (260, 300))
            pokemon_fight_images0.append((pokemon_fight_image0, i))
        for i in player1_numbers:
            pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{i}_fight_1.png')
            if i<3:
                pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
            else:
                pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300)) 
            pokemon_fight_images1.append((pokemon_fight_image1, i))

        pokemon_attack_images0 = []
        pokemon_attack_images1 = []
        missing_files0 = []
        missing_files1 = []
        for i in player0_numbers:
            for j in range(4):
                try:
                    pokemon_attack_image0 = pygame.image.load(f'Resources/pokemon_{i}_attack_{j}_0.png')
                    pokemon_attack_image0 = pygame.transform.scale(pokemon_attack_image0, (130, 150))
                    pokemon_attack_images0.append((pokemon_attack_image0, i))
                    valid_pair = (i, j)
                except FileNotFoundError:
                    missing_files0.append((i, j))
        for i in player1_numbers:
            for j in range(4):
                try:
                    pokemon_attack_image1 = pygame.image.load(f'Resources/pokemon_{i}_attack_{j}_1.png')
                    pokemon_attack_image1 = pygame.transform.scale(pokemon_attack_image1, (130, 150))
                    pokemon_attack_images1.append((pokemon_attack_image1, 0))                  
                    valid_pair = (i, j)
                except FileNotFoundError:
                    missing_files1.append((i, j))

        pokemon_choose_button_x0 = 301
        pokemon_choose_button_x0 = [pokemon_choose_button_x0, pokemon_choose_button_x0 + 75, pokemon_choose_button_x0 + 150]
        pokemon_choose_button_y0 = 45

        pokemon_choose_button_x1 = 983
        pokemon_choose_button_x1 = [pokemon_choose_button_x1, pokemon_choose_button_x1 + 75, pokemon_choose_button_x1 + 150]
        pokemon_choose_button_y1 = 45

        positions = generate_random_positions(random.randint(2, 5), [])

        if selected_field == 'Electric Field':
            field_image = pygame.image.load('Resources/field_electric.png')
            field_image = pygame.transform.scale(field_image, (100, 100))

        elif selected_field == 'Infernal Field':
            field_image = pygame.image.load('Resources/field_infernal.png')
            field_image = pygame.transform.scale(field_image, (100, 60))

        elif selected_field == 'Aquatic Field':
            field_image = pygame.image.load('Resources/field_aquatic.png')
            field_image = pygame.transform.scale(field_image, (100, 80))

        draw_field_images(field_image, window, positions)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if round_1_pokemon0 == None:
            round_1_pokemon0 = player0_numbers[0]
    
        '''
        if selected_field == "Electric Field":
            if 3 in player0_numbers:
                current_pokemon_choose_button_clicked0 = 3
            elif 0 in player0_numbers:
                if 3 not in player1_numbers:
                    current_pokemon_choose_button_clicked0 = 0
            elif 2 in player0_numbers:
                current_pokemon_choose_button_clicked0 = 2
            else:
                current_pokemon_choose_button_clicked0 = 1
        if selected_field == "Infernal Field":
            if 4 in player0_numbers:
                current_pokemon_choose_button_clicked0 = 4
            elif 1 in player0_numbers:
                if 4 not in player1_numbers:
                    current_pokemon_choose_button_clicked0 = 1
            elif 2 in player0_numbers:
                current_pokemon_choose_button_clicked0 = 2
            else:
                current_pokemon_choose_button_clicked0 = 0
        if selected_field == "Aquatic Field":
            if 5 in player0_numbers:
                current_pokemon_choose_button_clicked0 = 5
            elif 2 in player0_numbers:
                if 5 not in player1_numbers:
                    current_pokemon_choose_button_clicked0 = 2
            elif 1 in player0_numbers:
                current_pokemon_choose_button_clicked0 = 1
            else:
                current_pokemon_choose_button_clicked0 = 0
        '''

        for x in pokemon_choose_button_x0:
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y0 - 2, 70, 70), 2)

        for i in range(3):
            if round_1_pokemon0 == player0_numbers[i]:
                pokemon_button_images0[i][0].fill(RED, None, pygame.BLEND_RGBA_MULT)
                if pokemon_fight_images0[i][1]<3:
                    window.blit(pokemon_fight_images0[i][0], (265, 305))
                else:
                    window.blit(pokemon_fight_images0[i][0], (265, 305-75))

        for i in range(3):
            window.blit(pokemon_button_images0[i][0], (pokemon_choose_button_x0[i], pokemon_choose_button_y0))

        for x in pokemon_choose_button_x1:
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y0 - 2, 70, 70), 2)

        for i in range(3):
            if round_1_pokemon1 == player1_numbers[i]:
                pokemon_button_images1[i][0].fill(BLUE, None, pygame.BLEND_RGBA_MULT)
                if pokemon_fight_images1[i][1]<3:
                    window.blit(pokemon_fight_images1[i][0], (WIDTH-395, 305))
                else:
                    window.blit(pokemon_fight_images1[i][0], (WIDTH-395-130, 305-75))
        
        for i in range(3):
            window.blit(pokemon_button_images1[i][0], (pokemon_choose_button_x1[i], pokemon_choose_button_y1))

        if round_1_pokemon0 == 0 or round_1_pokemon0 == 3:
            attack_choose_button_texts0 = ["Thunderbolt", "Quick Attack", "Electro Ball", "Iron Tail"]
            draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)

        elif round_1_pokemon0 == 1 or round_1_pokemon0 == 4:
            attack_choose_button_texts0 = ["Ember", "Flamethrower", "Fire Spin", "Fire Fang"]
            draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)

        elif round_1_pokemon0 == 2 or round_1_pokemon0 == 5:
            attack_choose_button_texts0 = ["Water Gun", "Bubble Beam", "Water Pulse", "Aqua Tail"]
            draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)

        if round_1_pokemon1 == 0 or round_1_pokemon1 == 3:
            attack_choose_button_texts1 = ["Thunderbolt", "Quick Attack", "Electro Ball", "Iron Tail"]
            draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)

        elif round_1_pokemon1 == 1 or round_1_pokemon1 == 4:
            attack_choose_button_texts1 = ["Ember", "Flamethrower", "Fire Spin", "Fire Fang"]
            draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)

        elif round_1_pokemon1 == 2 or round_1_pokemon1 == 5:
            attack_choose_button_texts1 = ["Water Gun", "Bubble Beam", "Water Pulse", "Aqua Tail"]
            draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)

        pygame.display.flip()

#play_screen('Team Rocket', random.choice(["Aquatic Field", "Infernal Field", "Electric Field"]), [1, 4, 2], [0, 3, 5], None, 3, None, None)