import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255, 128)
RED = (255, 0, 0, 128)

font = pygame.font.SysFont(None, 20)

def generate_random_positions(num_images, existing_positions):
    positions = []
    while len(positions) < num_images:
        x = random.randint(260, WIDTH - 360)
        y = random.randint(180, HEIGHT - 150)

        new_position = (x, y)
        overlap = any(abs(pos[0] - x) < 150 and abs(pos[1] - y) < 150 for pos in existing_positions)
        if not overlap:
            positions.append(new_position)
            existing_positions.append(new_position)
    return positions

def draw_field_images(field_image, window, positions):
    for x, y in positions:
        window.blit(field_image, (x, y))

attack_choose_button_x_start0 = 20
attack_choose_button_y_start0 = 600

attack_choose_button_x_start1 = 1260
attack_choose_button_y_start1 = 600

attack_choose_button_width, attack_choose_button_height = 105, 50
attack_choose_button_spacing = 10

def draw_attack_choose_buttons(window, attack_choose_button_texts, attack_choose_button_x_start, attack_choose_button_y_start, current_button_clicked):
    for i, text in enumerate(attack_choose_button_texts):
        col = i % 2
        row = i // 2
        x = attack_choose_button_x_start + col * (attack_choose_button_width + attack_choose_button_spacing)
        y = attack_choose_button_y_start + row * (attack_choose_button_height + attack_choose_button_spacing)

        rect = pygame.Rect(x, y, attack_choose_button_width, attack_choose_button_height)
        color = BLUE if current_button_clicked == i else GRAY
        pygame.draw.rect(window, color, rect)
        pygame.draw.rect(window, BLACK, rect, 2)

        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        window.blit(text_surface, text_rect)

def play_screen(toss_result, selected_field, player0_numbers, player1_numbers, round_1_pokemon0, round_1_pokemon1, round_2_pokemon0, round_2_pokemon1):
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Play Screen")

    current_attack_choose_button_clicked0 = None
    current_attack_choose_button_clicked1 = None

    split_words = selected_field.lower().split(" ")
    field_sound = pygame.mixer.Sound(f'Resources/sound_{split_words[0]}.mp3')

    #-------------------------------------------------------Pokemon Selection-------------------------------------------------------     
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

    #-------------------------------------------------------Background Image-------------------------------------------------------
    background_image = pygame.image.load('Resources/board_play.png')
    background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

    #-------------------------------------------------------Players Images-------------------------------------------------------
    player0_image = pygame.image.load('Resources/player_0.png')
    player0_image = pygame.transform.scale(player0_image, (250, 350))

    player1_image = pygame.image.load('Resources/player_1.png')
    player1_image = pygame.transform.scale(player1_image, (170, 290))

    #-------------------------------------------------------Field Images-------------------------------------------------------
    if selected_field == 'Electric Field':
        field_image = pygame.image.load('Resources/field_electric.png')
        field_image = pygame.transform.scale(field_image, (100, 100))
    elif selected_field == 'Infernal Field':
        field_image = pygame.image.load('Resources/field_infernal.png')
        field_image = pygame.transform.scale(field_image, (100, 60))
    elif selected_field == 'Aquatic Field':
        field_image = pygame.image.load('Resources/field_aquatic.png')
        field_image = pygame.transform.scale(field_image, (100, 80))

    #-------------------------------------------------------Pokemon Buttons Images-------------------------------------------------------
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

    #-------------------------------------------------------Pokemon Fighting Images-------------------------------------------------------
    pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon0}_fight_0.png')
    if round_1_pokemon0 >= 3:
        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))
    else:
        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (260, 300))

    pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon1}_fight_1.png')
    if round_1_pokemon1 >= 3:
        pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
    else:
        pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

    #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
    if round_1_pokemon0 == 0 or round_1_pokemon0 == 3:
        attack_choose_button_texts0 = ["Thunderbolt", "Electro Ball", "Quick Attack", "Iron Tail"]
    elif round_1_pokemon0 == 1 or round_1_pokemon0 == 4:
        attack_choose_button_texts0 = ["Ember", "Flamethrower", "Fire Spin", "Fire Fang"]
    elif round_1_pokemon0 == 2 or round_1_pokemon0 == 5:
        attack_choose_button_texts0 = ["Water Gun", "Bubble Beam", "Water Pulse", "Aqua Tail"]
    if round_1_pokemon1 == 0 or round_1_pokemon1 == 3:
        attack_choose_button_texts1 = ["Thunderbolt", "Electro Ball", "Quick Attack", "Iron Tail"]
    elif round_1_pokemon1 == 1 or round_1_pokemon1 == 4:
        attack_choose_button_texts1 = ["Ember", "Flamethrower", "Fire Spin", "Fire Fang"]
    elif round_1_pokemon1 == 2 or round_1_pokemon1 == 5:
        attack_choose_button_texts1 = ["Water Gun", "Bubble Beam", "Water Pulse", "Aqua Tail"]

    #-------------------------------------------------------Pokemon Attack Images-------------------------------------------------------
    pokemon_attack_images0 = []
    pokemon_attack_images1 = []

    limit = 3
    if round_1_pokemon0 == 0 or round_1_pokemon0 == 3:
        limit = 2
    
    for i in range(limit):
        pokemon_attack_image0 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon0}_attack_{i}_0.png')
        pokemon_attack_image0 = pygame.transform.scale(pokemon_attack_image0, (130, 150))
        pokemon_attack_images0.append(pokemon_attack_image0)
    
    limit = 3
    if round_1_pokemon1 == 0 or round_1_pokemon1 == 3:
        limit = 2
    
    for i in range(limit):
        pokemon_attack_image1 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon1}_attack_{i}_1.png')
        pokemon_attack_image1 = pygame.transform.scale(pokemon_attack_image1, (130, 150))
        pokemon_attack_images1.append(pokemon_attack_image1)

    #-------------------------------------------------------Loop Running-------------------------------------------------------
    timer = 0
    show_field = False
    positions = []
    clock = pygame.time.Clock()

    sound_playing = False
    sound_duration = field_sound.get_length() * 1000

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if attack_choose_button_x_start1 <= mouse_x <= attack_choose_button_x_start1 + 2 * (attack_choose_button_width + attack_choose_button_spacing) and \
                        attack_choose_button_y_start1 <= mouse_y <= attack_choose_button_y_start1 + 2 * (attack_choose_button_height + attack_choose_button_spacing):
                    col = (mouse_x - attack_choose_button_x_start1) // (attack_choose_button_width + attack_choose_button_spacing)
                    row = (mouse_y - attack_choose_button_y_start1) // (attack_choose_button_height + attack_choose_button_spacing)
                    current_attack_choose_button_clicked1 = int(row * 2 + col)
                else:
                    current_attack_choose_button_clicked1 = None

        window.fill(WHITE)
        window.blit(background_image, (0, 0))

        #-------------------------------------------------------Players-------------------------------------------------------
        window.blit(player0_image, (50, 130))
        window.blit(player1_image, (1210, 180))

        #-------------------------------------------------------Field-------------------------------------------------------
        timer += clock.get_rawtime()
        clock.tick()
        
        if timer >= 10000:
            positions = generate_random_positions(random.randint(2, 5), [])
            timer -= 10000
            
            if sound_playing:
                field_sound.stop()
                sound_playing = False
        
        if timer < 5000:
            show_field = True
            draw_field_images(field_image, window, positions)
            if not sound_playing:
                field_sound.play() 
                sound_playing = True
                
        else:
            show_field = False
            if sound_playing:
                field_sound.stop() 
                sound_playing = False

        #-------------------------------------------------------Pokemon Buttons Border-------------------------------------------------------
        pokemon_choose_button_x0 = 301
        pokemon_choose_button_x0 = [pokemon_choose_button_x0, pokemon_choose_button_x0 + 75, pokemon_choose_button_x0 + 150]
        pokemon_choose_button_y0 = 45

        pokemon_choose_button_x1 = 983
        pokemon_choose_button_x1 = [pokemon_choose_button_x1, pokemon_choose_button_x1 + 75, pokemon_choose_button_x1 + 150]
        pokemon_choose_button_y1 = 45

        for x in pokemon_choose_button_x0:
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y0 - 2, 70, 70), 2)
        for x in pokemon_choose_button_x1:
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y1 - 2, 70, 70), 2)

        #-------------------------------------------------------Pokemon Buttons-------------------------------------------------------
        for x in pokemon_choose_button_x0:
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y0 - 2, 70, 70), 2)
        for i in range(3):
            window.blit(pokemon_button_images0[i][0], (pokemon_choose_button_x0[i], pokemon_choose_button_y0))
        
        for x in pokemon_choose_button_x1:
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y0 - 2, 70, 70), 2)
        for i in range(3):
            window.blit(pokemon_button_images1[i][0], (pokemon_choose_button_x1[i], pokemon_choose_button_y1))

        for i in range(3):
            if round_1_pokemon0 == player0_numbers[i]:
                pokemon_button_image_copy = pokemon_button_images0[i][0].copy()
                pokemon_button_image_copy.fill(RED, None, pygame.BLEND_RGBA_MULT)
                window.blit(pokemon_button_image_copy, (pokemon_choose_button_x0[i], pokemon_choose_button_y0))

        for i in range(3):
            if round_1_pokemon1 == player1_numbers[i]:
                pokemon_button_image_copy = pokemon_button_images1[i][0].copy()
                pokemon_button_image_copy.fill(BLUE, None, pygame.BLEND_RGBA_MULT)
                window.blit(pokemon_button_image_copy, (pokemon_choose_button_x1[i], pokemon_choose_button_y1))

        #-------------------------------------------------------Pokemon Fighting-------------------------------------------------------
        if round_1_pokemon0 >= 3:
            window.blit(pokemon_fight_image0, (265, 305))
        else:
            window.blit(pokemon_fight_image0, (265, 305-75))

        if round_1_pokemon1 >= 3:
            window.blit(pokemon_fight_image1, (WIDTH-395, 305))
        else:
            window.blit(pokemon_fight_image1,  (WIDTH-395-130, 305-75))

        #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
        if round_1_pokemon0 == 0 or round_1_pokemon0 == 3:
            draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)
        elif round_1_pokemon0 == 1 or round_1_pokemon0 == 4:
            draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)
        elif round_1_pokemon0 == 2 or round_1_pokemon0 == 5:
            draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)
        if round_1_pokemon1 == 0 or round_1_pokemon1 == 3:
            draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)
        elif round_1_pokemon1 == 1 or round_1_pokemon1 == 4:
            draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)
        elif round_1_pokemon1 == 2 or round_1_pokemon1 == 5:
            draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)
        
        #-------------------------------------------------------Pokemon Attacks-------------------------------------------------------

        pygame.display.flip()

play_screen('Team_Rocket', random.choice(["Electric Field", "Infernal Field", "Aquatic Field"]), [2, 3, 4], [0, 3, 5], None, 0, None, None)