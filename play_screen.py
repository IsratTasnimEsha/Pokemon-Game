import pygame
import random
import time
import sys
from fuzzy_logic_decision import find_best_pokemon_index

pygame.init()

move = 0
moves = 0
bg_index = 0

# Constants
WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

# Define colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255, 128)
RED = (255, 0, 0, 128)

font = pygame.font.SysFont("comicsansms", 15)

# Simplified Pokémon data structure

pokemon_data0 = {
    0: {"name": "Meowth", "health": 100, "attacks": ["Attack", "Defense"], "type": "Electric"},
    1: {"name": "Weezing", "health": 100, "attacks": ["Attack", "Defense"], "type": "Fire"},
    2: {"name": "Wobbuffet", "health": 100, "attacks": ["Attack", "Defense"], "type": "Water"}
}

pokemon_data1 = {
    0: {"name": "Pikachu", "health": 100, "attacks": ["Attack", "Defense"], "type": "Electric"},
    1: {"name": "Charmander", "health": 100, "attacks": ["Attack", "Defense"], "type": "Fire"},
    2: {"name": "Squirtle", "health": 100, "attacks": ["Attack", "Defense"], "type": "Water"},
}

# Define the mappings for field names to indices


def get_score(current_field_index, player0_current_pokemon_index, player1_current_pokemon_index):
    # Define the mappings for each field
    field_scores = {
        0: {
            (0, 0): 5-5, (0, 1): 5-3, (0, 2): 8-0,
            (1, 0): 3-5, (1, 1): 0-0, (1, 2): 0-5,
            (2, 0): 0-8, (2, 1): 3-0, (2, 2): 0-0
        },
        1: {
            (0, 0): 0-0, (0, 1): 0-8, (0, 2): 3-0,
            (1, 0): 8-0, (1, 1): 5-5, (1, 2): 5-3,
            (2, 0): 0-3, (2, 1): 3-5, (2, 2): 0-0
        },
        2: {
            (0, 0): 0-0, (0, 1): 0-3, (0, 2): 3-5,
            (1, 0): 3-0, (1, 1): 0-0, (1, 2): 0-8,
            (2, 0): 5-3, (2, 1): 8-0, (2, 2): 5-5
        }
    }

    # Get the score based on the current field and Pokémon indices
    return field_scores.get(current_field_index, {}).get((player0_current_pokemon_index, player1_current_pokemon_index), None)

def minimax(current_field_index, player0_current_pokemon_index, player1_current_pokemon_index, depth, is_maximizing_player):
    score = get_score(current_field_index, player0_current_pokemon_index, player1_current_pokemon_index)
    if score is not None:
        return score
    
    if is_maximizing_player:
        best_score = float('-inf')
        for p0_index in range(3):
            for p1_index in range(3):
                if (p0_index, p1_index) != (player0_current_pokemon_index, player1_current_pokemon_index):
                    current_score = minimax(current_field_index, p0_index, p1_index, depth + 1, False)
                    best_score = max(best_score, current_score)
        return best_score
    else:
        best_score = float('inf')
        for p0_index in range(3):
            for p1_index in range(3):
                if (p0_index, p1_index) != (player0_current_pokemon_index, player1_current_pokemon_index):
                    current_score = minimax(current_field_index, p0_index, p1_index, depth + 1, True)
                    best_score = min(best_score, current_score)
        return best_score

def choose_action(current_field_index, player0_current_pokemon_index, player1_current_pokemon_index):
    if current_field_index == 'electric':
        current_field_index = 0
    if current_field_index == 'fire':
        current_field_index = 1
    if current_field_index == 'water':
        current_field_index = 2
    score = minimax(current_field_index, player0_current_pokemon_index, player1_current_pokemon_index, 0, True)
    if score >= 0:
        return 'attack'
    else:
        return 'defend'


def game_over(game_state):
    player0_healths, player1_healths, _, _, _, _ = game_state
    return all(hp <= 0 for hp in player0_healths) or all(hp <= 0 for hp in player1_healths)

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

attack_choose_button_x_start0 = -80
attack_choose_button_y_start0 = 680

# Adjusted position to fit within the screen
attack_choose_button_x_start1 = 1260 
attack_choose_button_y_start1 = 680

attack_choose_button_width, attack_choose_button_height = 100, 50
attack_choose_button_spacing = 5

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

def draw_health_bar(window, health, max_health, x, y, width, height):
    # Calculate the health bar width
    health_bar_width = int((health / max_health) * width)
    
    # Draw the health bar background
    pygame.draw.rect(window, GRAY, (x, y, width, height))
    
    # Draw the health bar
    pygame.draw.rect(window, BLUE, (x, y, health_bar_width, height))

def attack_damage(attacker_type, defender_type, field_type):
    base_damage = 10
    field_bonus = 5 if attacker_type == field_type else 0
    type_bonus = 0

    if (attacker_type == "Electric" and defender_type == "Water") or \
       (attacker_type == "Water" and defender_type == "Fire") or \
       (attacker_type == "Fire" and defender_type == "Electric"):
        type_bonus = 3

    return base_damage + field_bonus + type_bonus

def play_screen(player0_numbers, player1_numbers, current_pokemon_index1, elixir0, elixir1):
    global move, moves, bg_index

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Play Screen")

    current_attack_choose_button_clicked0 = None
    current_attack_choose_button_clicked1 = None
    player_turn = False

    # Initial health for each Pokémon
    max_health = 100
    player0_healths = [max_health] * 3
    player1_healths = [max_health] * 3

    # Field type mapping
    field_type_mapping = {
        "Electric Field": "Electric",
        "Infernal Field": "Fire",
        "Aquatic Field": "Water"
    }
    
    #-------------------------------------------------------Background Images-------------------------------------------------------
    background_images = [
        pygame.image.load('Resources/board_electric.png'),
        pygame.image.load('Resources/board_fire.png'),
        pygame.image.load('Resources/board_water.png')        
    ]
    background_images = [pygame.transform.scale(image, (WIDTH, HEIGHT)) for image in background_images]

    positions = []

    last_attack_time = 0
    computer_action_text = ""

    #-------------------------------------------------------Players Images-------------------------------------------------------
    player0_image = pygame.image.load('Resources/player_0.png')
    player0_image = pygame.transform.scale(player0_image, (250, 400))

    player1_image = pygame.image.load('Resources/player_1.png')
    player1_image = pygame.transform.scale(player1_image, (180, 300))  # Adjusted size to fit within the screen

    #-------------------------------------------------------Pokemon Buttons Images-------------------------------------------------------
    pokemon_button_images0 = []
    pokemon_button_images1 = []
    for i in player0_numbers:
        pokemon_button_image = pygame.image.load(f'Resources/pokemon_{i}.png')
        pokemon_button_image_scaled0 = pygame.transform.scale(pokemon_button_image, (65, 65))
        pokemon_button_images0.append((pokemon_button_image_scaled0, i))
    for i in player1_numbers:
        pokemon_button_image = pygame.image.load(f'Resources/pokemon_{i + 3}.png')
        pokemon_button_image_scaled1 = pygame.transform.scale(pokemon_button_image, (65, 65))
        pokemon_button_images1.append((pokemon_button_image_scaled1, i))

    #-------------------------------------------------------Loop Running-------------------------------------------------------
    while True:
        window.fill(WHITE)

        if (moves % 3 == 0):
            window.blit(background_images[bg_index], (0, 0))
        if (moves % 3 == 1):
            window.blit(background_images[bg_index], (0, 0))
        if (moves % 3 == 2):
            window.blit(background_images[bg_index], (0, 0))

        if bg_index == 0:
            field_type_value = 'electric'
        if bg_index == 1:
            field_type_value = 'fire'
        if bg_index == 2:
            field_type_value = 'water'
        
        current_pokemon_index0 = find_best_pokemon_index(0, current_pokemon_index1, field_type_value, player0_healths, elixir0)

        #-------------------------------------------------------Pokemon Fighting Images-------------------------------------------------------
        pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index0}_fight_0.png')
        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))

        pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index1 + 3}_fight_1.png')
        pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))

        #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
        attack_choose_button_texts0 = pokemon_data0[current_pokemon_index0]['attacks']
        attack_choose_button_texts1 = pokemon_data1[current_pokemon_index1]['attacks']

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
                # Handle Pokémon switching
                for i, (img, num) in enumerate(pokemon_button_images1):
                    if pokemon_choose_button_x1[i] <= mouse_x <= pokemon_choose_button_x1[i] + 65 and \
                            pokemon_choose_button_y1 <= mouse_y <= pokemon_choose_button_y1 + 65 and player1_healths[i] > 0:
                        current_pokemon_index1 = i
                        current_pokemon_index1 = player1_numbers[current_pokemon_index1]
                        attack_choose_button_texts1 = pokemon_data1[current_pokemon_index1]['attacks']
                        pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index1 + 3}_fight_1.png')
                        if current_pokemon_index1 < 3:
                            pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
                        else:
                            pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

                if attack_choose_button_x_start1 <= mouse_x <= attack_choose_button_x_start1 + 2 * (attack_choose_button_width + attack_choose_button_spacing) and \
                        attack_choose_button_y_start1 <= mouse_y <= attack_choose_button_y_start1 + 2 * (attack_choose_button_height + attack_choose_button_spacing) and player_turn:
                    col = (mouse_x - attack_choose_button_x_start1) // (attack_choose_button_width + attack_choose_button_spacing)
                    row = (mouse_y - attack_choose_button_y_start1) // (attack_choose_button_height + attack_choose_button_spacing)
                    current_attack_choose_button_clicked1 = int(row * 2 + col)
                    action = attack_choose_button_texts1[current_attack_choose_button_clicked1]

                    if action == "Defense":
                        print(f"{pokemon_data1[current_pokemon_index1]['name']} used Defense!")
                    else:
                        attacker_type = pokemon_data1[current_pokemon_index1]['type']
                        defender_type = pokemon_data0[current_pokemon_index0]['type']
                        damage = attack_damage(attacker_type, defender_type, field_type_value)        
                        player0_healths[current_pokemon_index0] -= damage
                        print(f"{pokemon_data1[current_pokemon_index1]['name']} used {action} on {pokemon_data0[current_pokemon_index0]['name']} causing {damage} damage!")

                    if player0_healths[current_pokemon_index0] <= 0:
                        player0_healths[current_pokemon_index0] = 0
                        print(f"{pokemon_data0[current_pokemon_index0]['name']} has fainted!")
                        best_pokemon_index0 = find_best_pokemon_index(current_pokemon_index0, current_pokemon_index1, field_type_value, player0_healths, elixir0)
                        if best_pokemon_index0 == current_pokemon_index0:
                            player0_healths[best_pokemon_index0] += elixir0.pop(0)
                        elif best_pokemon_index0 != current_pokemon_index0:
                            current_pokemon_index0 = best_pokemon_index0
                        if current_pokemon_index0 is None:
                            print("Team Rocket is defeated!")
                            draw_text(window, "Team Rocket is defeated!", font, BLACK, WIDTH // 4, HEIGHT // 4)
                            pygame.display.flip()
                            time.sleep(3)
                            return
                        attack_choose_button_texts0 = pokemon_data0[current_pokemon_index0]['attacks']
                        pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index0}_fight_0.png')
                        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))

                    player_turn = False
                    last_attack_time = pygame.time.get_ticks()
                else:
                    current_attack_choose_button_clicked1 = None

        if not player_turn and pygame.time.get_ticks() - last_attack_time >= 1000:
            action = choose_action(field_type_value, current_pokemon_index0, current_pokemon_index1)
            move += 1
            if (move % 3 == 0):
                moves += 1
                bg_index = random.randint(0, 2)

            if moves % 5 == 0:
                background_image = background_images[1]
                background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

            computer_action_text = f"Team Rocket chose {action}"
            print(computer_action_text)

            if action == "Defense":
                print(f"{pokemon_data0[current_pokemon_index0]['name']} used Defense!")
            else:
                attacker_type = pokemon_data0[current_pokemon_index0]['type']
                defender_type = pokemon_data1[current_pokemon_index1]['type']
                damage = attack_damage(attacker_type, defender_type, field_type_value)  # Increased attack damage   
                player1_healths[current_pokemon_index1] -= damage
                print(f"{pokemon_data0[current_pokemon_index0]['name']} used {action} on {pokemon_data1[current_pokemon_index1]['name']} causing {damage} damage!")

            if player1_healths[current_pokemon_index1] <= 0:
                player1_healths[current_pokemon_index1] = 0
                print(f"{pokemon_data1[current_pokemon_index1]['name']} has fainted!")
                if player1_healths[(current_pokemon_index1 + 1) % 3] != 0:
                    current_pokemon_index1 = (current_pokemon_index1 + 1) % 3
                elif player1_healths[(current_pokemon_index1 + 2) % 3] != 0:
                    current_pokemon_index1 = (current_pokemon_index1 + 2) % 3
                else:
                    current_pokemon_index1 = None
                if current_pokemon_index1 is None:
                    print("Ash is defeated!")
                    draw_text(window, "Ash is defeated!", font, RED, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    time.sleep(3)
                    return
                current_pokemon_index1 = player1_numbers[current_pokemon_index1]
                attack_choose_button_texts1 = pokemon_data1[current_pokemon_index1]['attacks']
                pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index1 + 3}_fight_1.png')
                if current_pokemon_index1 < 3:
                    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
                else:
                    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

            player_turn = True

        #-------------------------------------------------------Players-------------------------------------------------------
        window.blit(player0_image, (50, 80))
        window.blit(player1_image, (WIDTH - 270, 150))  # Adjusted position to fit within the screen

        #-------------------------------------------------------Health Display-------------------------------------------------------
        # Draw health bars for both players with adjusted positions
        # Calculate the x-coordinate for the health bars
        health_bar_x0 = attack_choose_button_x_start0 + 2 * (attack_choose_button_width + attack_choose_button_spacing)
        health_bar_x1 = health_bar_x0 + 580  # Adjust the gap between the health bars
        # Calculate the y-coordinate for both health bars
        health_bar_y = attack_choose_button_y_start0

        # For player0's health bar
        draw_health_bar(window, player0_healths[current_pokemon_index0], max_health, health_bar_x0 + 170, health_bar_y + 5, 250, 40)

        # For player1's health bar
        draw_health_bar(window, player1_healths[current_pokemon_index1], max_health, health_bar_x1 + 280, health_bar_y + 5, 250, 40)

        # Define the font for the text
        text_font = pygame.font.SysFont(None, 20)

        # Render the text for player0's health
        health_text_surface0 = font.render(f"Health Remain: {player0_healths[current_pokemon_index0]}%", True, BLACK)
        health_text_rect0 = health_text_surface0.get_rect()
        health_text_rect0.midtop = (health_bar_x0 + 300, health_bar_y + 12)  # Adjust position as needed

        # Render the text for player1's health
        health_text_surface1 = font.render(f"Health Remain: {player1_healths[current_pokemon_index1]}%", True, BLACK)
        health_text_rect1 = health_text_surface1.get_rect()
        health_text_rect1.midtop = (health_bar_x1 + 405, health_bar_y + 12)  # Adjust position as needed

        # Blit the text onto the window
        window.blit(health_text_surface0, health_text_rect0)
        window.blit(health_text_surface1, health_text_rect1)

        # Display the chosen action by the computer
        computer_action_surface = font.render(computer_action_text, True, BLACK)
        computer_action_rect = computer_action_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(computer_action_surface, computer_action_rect)

        #-------------------------------------------------------Pokemon Buttons Border-------------------------------------------------------
        pokemon_choose_button_x0 = 301
        pokemon_choose_button_x0 = [pokemon_choose_button_x0, pokemon_choose_button_x0 + 75, pokemon_choose_button_x0 + 150]
        pokemon_choose_button_y0 = 45

        pokemon_choose_button_x1 = WIDTH - 490
        pokemon_choose_button_x1 = [pokemon_choose_button_x1, pokemon_choose_button_x1 + 65, pokemon_choose_button_x1 + 130]
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
            pygame.draw.rect(window, (0, 0, 0), (x - 2, pokemon_choose_button_y1 - 2, 70, 70), 2)
        for i in range(3):
            window.blit(pokemon_button_images1[i][0], (pokemon_choose_button_x1[i], pokemon_choose_button_y1))

        for i in range(3):
            if current_pokemon_index0 == player0_numbers[i]:
                pokemon_button_image_copy = pokemon_button_images0[i][0].copy()
                pokemon_button_image_copy.fill(RED, None, pygame.BLEND_RGBA_MULT)
                window.blit(pokemon_button_image_copy, (pokemon_choose_button_x0[i], pokemon_choose_button_y0))

        for i in range(3):
            if current_pokemon_index1 == player1_numbers[i]:
                pokemon_button_image_copy = pokemon_button_images1[i][0].copy()
                pokemon_button_image_copy.fill(BLUE, None, pygame.BLEND_RGBA_MULT)
                window.blit(pokemon_button_image_copy, (pokemon_choose_button_x1[i], pokemon_choose_button_y1))

        #-------------------------------------------------------Pokemon Fighting-------------------------------------------------------
        window.blit(pokemon_fight_image0, (300, 305))
        window.blit(pokemon_fight_image1, (WIDTH-400, 305))

        #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
        draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)
        pygame.display.flip()

def draw_text(window, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)  # Display the text for 1 second

#play_screen([0, 1, 2], [0, 1, 2], 1, [40, 50], [0,1])