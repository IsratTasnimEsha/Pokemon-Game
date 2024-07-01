import pygame
import random
import time
import sys
import pokemon_swap_ai

pygame.init()

# Define colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255, 128)
RED = (255, 0, 0, 128)

font = pygame.font.SysFont(None, 20)

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pokemon Battle")

# Simplified Pokémon data structure
pokemon_data = {
    0: {"name": "Pikachu", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Electric"},
    1: {"name": "Charmander", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Fire"},
    2: {"name": "Squirtle", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Water"},
    3: {"name": "Raichu", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Electric"},
    4: {"name": "Charizard", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Fire"},
    5: {"name": "Blastoise", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Water"},
    6: {"name": "Meowth", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Electric"},
    7: {"name": "Wobbuffet", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Fire"},
    8: {"name": "Weezing", "health": 100, "attacks": ["Attack", "Defense", "Elixir"], "type": "Water"}
}

def evaluate_game_state(game_state):
    player0_healths, player1_healths, _, _, _ = game_state
    player0_score = sum(player0_healths)
    player1_score = sum(player1_healths)
    return player1_score - player0_score  # Positive if good for computer, negative if good for player

def minimax(game_state, depth, alpha, beta, maximizing_player, defense_left, elixir_used, field_type_value):
    if depth == 0 or game_over(game_state):
        return evaluate_game_state(game_state), None

    player0_healths, player1_healths, player_turn, current_pokemon_index0, current_pokemon_index1 = game_state

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        possible_moves = get_possible_moves(player1_healths[current_pokemon_index1], defense_left[1], elixir_used[1])

        for move in possible_moves:
            new_game_state = simulate_move(game_state, move, maximizing_player, defense_left, elixir_used, field_type_value)
            eval, _ = minimax(new_game_state, depth - 1, alpha, beta, False, defense_left, elixir_used, field_type_value)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        possible_moves = get_possible_moves(player0_healths[current_pokemon_index0], defense_left[0], elixir_used[0])

        for move in possible_moves:
            new_game_state = simulate_move(game_state, move, maximizing_player, defense_left, elixir_used, field_type_value)
            eval, _ = minimax(new_game_state, depth - 1, alpha, beta, True, defense_left, elixir_used, field_type_value)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_possible_moves(current_health, defense_left, elixir_left):
    moves = ["Attack"]
    if defense_left > 0:
        moves.append("Defense")
    if elixir_left >= 5:
        moves.append("Elixir")
    return moves

def simulate_move(game_state, move, maximizing_player, defense_left, elixir_used, field_type_value):
    player0_healths, player1_healths, player_turn, current_pokemon_index0, current_pokemon_index1 = game_state
    new_player0_healths = player0_healths[:]
    new_player1_healths = player1_healths[:]
    
    if maximizing_player:
        if move == "Attack":
            damage = attack_damage(pokemon_data[current_pokemon_index1]['type'], pokemon_data[current_pokemon_index0]['type'], field_type_value) + 10  # Increased attack damage
            new_player0_healths[current_pokemon_index0] -= damage
        elif move == "Defense":
            new_player1_healths[current_pokemon_index1] -= 5  # Reduced self-damage for defense
            defense_left[1] -= 1
        elif move == "Elixir":
            new_player1_healths[current_pokemon_index1] = min(100, new_player1_healths[current_pokemon_index1] + 30)
            elixir_used[1] -= 5
    else:
        if move == "Attack":
            damage = attack_damage(pokemon_data[current_pokemon_index0]['type'], pokemon_data[current_pokemon_index1]['type'], field_type_value)
            new_player1_healths[current_pokemon_index1] -= damage
        elif move == "Defense":
            new_player0_healths[current_pokemon_index0] -= 10  # Increased self-damage for defense
            defense_left[0] -= 1
        elif move == "Elixir":
            new_player0_healths[current_pokemon_index0] = min(100, new_player0_healths[current_pokemon_index0] + 30)
            elixir_used[0] -= 5
    
    return new_player0_healths, new_player1_healths, not player_turn, current_pokemon_index0, current_pokemon_index1

def game_over(game_state):
    player0_healths, player1_healths, _, _, _ = game_state
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

attack_choose_button_x_start0 = 20
attack_choose_button_y_start0 = 600

# Adjusted position to fit within the screen
attack_choose_button_x_start1 = 1060 
attack_choose_button_y_start1 = 600

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
    base_damage = 20
    field_bonus = 5 if attacker_type == field_type else 0
    type_bonus = 0

    if (attacker_type == "Electric" and defender_type == "Water") or \
       (attacker_type == "Water" and defender_type == "Fire") or \
       (attacker_type == "Fire" and defender_type == "Electric"):
        type_bonus = 5

    return base_damage + field_bonus + type_bonus

def play_screen(toss_result, selected_field, player0_numbers, player1_numbers, round_1_pokemon0, round_1_pokemon1, round_2_pokemon0, round_2_pokemon1):
    current_attack_choose_button_clicked0 = None
    current_attack_choose_button_clicked1 = None
    player_turn = True if toss_result == "Me(Ash)" else False
    defense_used0 = 0
    defense_used1 = 0
    defense_max = 4
    elixir_used0 = 15  # Added initial elixir value for player 0
    elixir_used1 = 15  # Added initial elixir value for player 1

    split_words = selected_field.lower().split(" ")
    field_sound = pygame.mixer.Sound(f'Resources/sound_{split_words[0]}.mp3')

    # Initial health for each Pokémon
    max_health = 100
    player0_healths = [max_health] * 3
    player1_healths = [max_health] * 3

    # Current Pokémon indexes
    current_pokemon_index0 = 0
    current_pokemon_index1 = 0

    # Field type mapping
    field_type_mapping = {
        "Electric Field": "Electric",
        "Infernal Field": "Fire",
        "Aquatic Field": "Water"
    }

    field_type_value = field_type_mapping.get(selected_field, "Electric")  # Default to Electric if field type not found

    #-------------------------------------------------------Pokemon Selection-------------------------------------------------------     
    if round_1_pokemon0 == None:
        round_1_pokemon0 = player0_numbers[0]

    #-------------------------------------------------------Background Images-------------------------------------------------------
    background_images = [
        pygame.image.load('Resources/water.png'),
        pygame.image.load('Resources/electric1.png'),
        pygame.image.load('Resources/fire2.png')
    ]
    for i in range(3):
        background_images[i] = pygame.transform.scale(background_images[i], (WIDTH, HEIGHT))

    background_image_index = 0
    last_background_change_time = pygame.time.get_ticks()

    #-------------------------------------------------------Players Images-------------------------------------------------------
    player0_image = pygame.image.load('Resources/player_0.png')
    player0_image = pygame.transform.scale(player0_image, (200, 300))

    player1_image = pygame.image.load('Resources/player_1.png')
    player1_image = pygame.transform.scale(player1_image, (280, 300))  # Adjusted size to fit within the screen

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
    if round_1_pokemon0 < 3:
        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))
    else:
        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (260, 300))

    pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon1}_fight_1.png')
    if round_1_pokemon1 < 3:
        pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
    else:
        pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

    #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
    attack_choose_button_texts0 = pokemon_data[round_1_pokemon0]['attacks']
    attack_choose_button_texts1 = pokemon_data[round_1_pokemon1]['attacks']

    #-------------------------------------------------------Loop Running-------------------------------------------------------
    timer = 0
    show_field = False
    positions = []
    clock = pygame.time.Clock()

    sound_playing = False
    sound_duration = field_sound.get_length() * 1000

    last_attack_time = 0
    computer_action_text = ""

    while True:
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
                        round_1_pokemon1 = player1_numbers[current_pokemon_index1]
                        attack_choose_button_texts1 = pokemon_data[round_1_pokemon1]['attacks']
                        pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon1}_fight_1.png')
                        if round_1_pokemon1 < 3:
                            pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
                        else:
                            pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

                if attack_choose_button_x_start1 <= mouse_x <= attack_choose_button_x_start1 + 2 * (attack_choose_button_width + attack_choose_button_spacing) and \
                        attack_choose_button_y_start1 <= mouse_y <= attack_choose_button_y_start1 + 2 * (attack_choose_button_height + attack_choose_button_spacing) and player_turn:
                    col = (mouse_x - attack_choose_button_x_start1) // (attack_choose_button_width + attack_choose_button_spacing)
                    row = (mouse_y - attack_choose_button_y_start1) // (attack_choose_button_height + attack_choose_button_spacing)
                    current_attack_choose_button_clicked1 = int(row * 2 + col)
                    action = attack_choose_button_texts1[current_attack_choose_button_clicked1]

                    if action == "Defense" and defense_used1 < defense_max:
                        defense_used1 += 1
                        player1_healths[current_pokemon_index1] -= 5  # Reduced self-damage for defense
                        print(f"{pokemon_data[round_1_pokemon1]['name']} used Defense and lost 5 health!")
                    elif action == "Elixir" and elixir_used1 >= 5:  # Added Elixir action handling
                        elixir_used1 -= 5
                        player1_healths[current_pokemon_index1] = min(max_health, player1_healths[current_pokemon_index1] + 30)
                        print(f"{pokemon_data[round_1_pokemon1]['name']} used Elixir and gained 30 health!")
                    elif action == "Elixir" and elixir_used1 < 5:  # Elixir depleted message
                        draw_text(window, "You have used all elixirs. Choose another option.", font, BLACK, WIDTH // 2, HEIGHT // 2)
                        print("You have used all elixirs. Choose another option.")
                    else:
                        attacker_type = pokemon_data[round_1_pokemon1]['type']
                        defender_type = pokemon_data[round_1_pokemon0]['type']
                        damage = attack_damage(attacker_type, defender_type, field_type_value)
                        if defense_used0:
                            defense_used0 = False
                           # draw_text(window, "Your attack is defended by your opponent", font, BLACK, WIDTH // 2, HEIGHT // 2)
                            print("Your attack is defended by your opponent!")
                        else:
                            player0_healths[current_pokemon_index0] -= damage
                            print(f"{pokemon_data[round_1_pokemon1]['name']} used {action} on {pokemon_data[round_1_pokemon0]['name']} causing {damage} damage!")

                    if player0_healths[current_pokemon_index0] <= 0:
                        player0_healths[current_pokemon_index0] = 0
                        print(f"{pokemon_data[round_1_pokemon0]['name']} has fainted!")
                        current_pokemon_index0 = pokemon_swap_ai.select_pokemon(player0_numbers, player0_healths, round_1_pokemon0, field_type_value)
                        if current_pokemon_index0 is None:
                            print("Team Rocket is defeated!")
                           # draw_text(window, "Team Rocket is defeated!", font, BLACK, WIDTH // 4, HEIGHT // 4)
                            pygame.display.flip()
                            time.sleep(3)
                            return
                        round_1_pokemon0 = player0_numbers[current_pokemon_index0]
                        attack_choose_button_texts0 = pokemon_data[round_1_pokemon0]['attacks']
                        pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon0}_fight_0.png')
                        if round_1_pokemon0 < 3:
                            pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))
                        else:
                            pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (260, 300))

                    player_turn = False
                    last_attack_time = pygame.time.get_ticks()
                else:
                    current_attack_choose_button_clicked1 = None

        if not player_turn and pygame.time.get_ticks() - last_attack_time >= 1000:
            _, action = minimax(
                (player0_healths, player1_healths, player_turn, current_pokemon_index0, current_pokemon_index1),
                3, float('-inf'), float('inf'), False, [defense_max - defense_used0, defense_max - defense_used1], [elixir_used0, elixir_used1], field_type_value
            )
            computer_action_text = f"Team Rocket chose {action}"
            print(computer_action_text)

            if action == "Defense" and defense_used0 < defense_max:
                defense_used0 += 1
                player0_healths[current_pokemon_index0] -= 10
                print(f"{pokemon_data[round_1_pokemon0]['name']} used Defense and lost 10 health!")
            elif action == "Elixir" and elixir_used0 >= 5:  # Added Elixir action handling
                elixir_used0 -= 5
                player0_healths[current_pokemon_index0] = min(max_health, player0_healths[current_pokemon_index0] + 30)
                draw_text(window, "used Elixir and gained 30 health!", font, GRAY, WIDTH // 2, HEIGHT // 2)
                print(f"{pokemon_data[round_1_pokemon0]['name']} used Elixir and gained 30 health!")
            elif action == "Elixir" and elixir_used0 < 5:  # Elixir depleted message
                draw_text(window, "Team Rocket has used all elixirs. Choosing another option.", font, BLACK, WIDTH // 2, HEIGHT // 2)
                print("Team Rocket has used all elixirs. Choosing another option.")
            else:
                attacker_type = pokemon_data[round_1_pokemon0]['type']
                defender_type = pokemon_data[round_1_pokemon1]['type']
                damage = attack_damage(attacker_type, defender_type, field_type_value) + 10  # Increased attack damage
                if defense_used1:
                    defense_used1 = False
                    draw_text(window, "Your attack is defended by Team Rocket", font, WHITE, WIDTH // 2, HEIGHT // 2)
                    print("Your attack is defended by Team Rocket!")
                else:
                    player1_healths[current_pokemon_index1] -= damage
                    print(f"{pokemon_data[round_1_pokemon0]['name']} used {action} on {pokemon_data[round_1_pokemon1]['name']} causing {damage} damage!")

            if player1_healths[current_pokemon_index1] <= 0:
                player1_healths[current_pokemon_index1] = 0
                print(f"{pokemon_data[round_1_pokemon1]['name']} has fainted!")
                current_pokemon_index1 = pokemon_swap_ai.select_pokemon(player1_numbers, player1_healths, round_1_pokemon1, field_type_value)
                if current_pokemon_index1 is None:
                    print("Ash is defeated!")
                    draw_text(window, "Ash is defeated!", font, BLACK, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    time.sleep(3)
                    return
                round_1_pokemon1 = player1_numbers[current_pokemon_index1]
                attack_choose_button_texts1 = pokemon_data[round_1_pokemon1]['attacks']
                pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{round_1_pokemon1}_fight_1.png')
                if round_1_pokemon1 < 3:
                    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
                else:
                    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

            player_turn = True

        window.fill(WHITE)
        window.blit(background_images[background_image_index], (0, 0))

        #-------------------------------------------------------Players-------------------------------------------------------
        window.blit(player0_image, (20, 130))
        window.blit(player1_image, (WIDTH - 320, 150))  # Adjusted position to fit within the screen

        #-------------------------------------------------------Health Display-------------------------------------------------------
        # Draw health bars for both players with adjusted positions
        # Calculate the x-coordinate for the health bars
        health_bar_x0 = attack_choose_button_x_start0 + 2 * (attack_choose_button_width + attack_choose_button_spacing) + 10
        health_bar_x1 = health_bar_x0 + 580  # Adjust the gap between the health bars
        # Calculate the y-coordinate for both health bars
        health_bar_y = attack_choose_button_y_start0

        # For player0's health bar
        draw_health_bar(window, player0_healths[current_pokemon_index0], max_health, health_bar_x0, health_bar_y, 100, 20)

        # For player1's health bar
        draw_health_bar(window, player1_healths[current_pokemon_index1], max_health, health_bar_x1, health_bar_y, 100, 20)

        # Define the font for the text
        text_font = pygame.font.SysFont(None, 20)

        # Render the text for player0's health
        health_text_surface0 = text_font.render(f"Health Remain: {player0_healths[current_pokemon_index0]}%", True, BLACK)
        health_text_rect0 = health_text_surface0.get_rect()
        health_text_rect0.midtop = (health_bar_x0 + 50, health_bar_y + 30)  # Adjust position as needed

        # Render the text for player1's health
        health_text_surface1 = text_font.render(f"Health Remain: {player1_healths[current_pokemon_index1]}%", True, BLACK)
        health_text_rect1 = health_text_surface1.get_rect()
        health_text_rect1.midtop = (health_bar_x1 + 50, health_bar_y + 30)  # Adjust position as needed

        # Blit the text onto the window
        window.blit(health_text_surface0, health_text_rect0)
        window.blit(health_text_surface1, health_text_rect1)

        # Display the chosen action by the computer
        computer_action_surface = font.render(computer_action_text, True, BLACK)
        computer_action_rect = computer_action_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(computer_action_surface, computer_action_rect)

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
        if round_1_pokemon0 < 3:
            window.blit(pokemon_fight_image0, (265, 305))
        else:
            window.blit(pokemon_fight_image0, (265, 305-75))

        if round_1_pokemon1 < 3:
            window.blit(pokemon_fight_image1, (WIDTH-395, 305))
        else:
            window.blit(pokemon_fight_image1,  (WIDTH-395-130, 305-75))

        #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
        draw_attack_choose_buttons(window, attack_choose_button_texts0, attack_choose_button_x_start0, attack_choose_button_y_start0, current_attack_choose_button_clicked0)
        draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)

        # Display the number of defenses left for each player
        defenses_left_text0 = f"Defenses left: {defense_max - defense_used0}"  # Added line for defense count display
        defenses_left_surface0 = font.render(defenses_left_text0, True, BLACK)  # Added line for defense count display
        window.blit(defenses_left_surface0, (attack_choose_button_x_start0, attack_choose_button_y_start0 - 30))  # Added line for defense count display

        defenses_left_text1 = f"Defenses left: {defense_max - defense_used1}"  # Added line for defense count display
        defenses_left_surface1 = font.render(defenses_left_text1, True, BLACK)  # Added line for defense count display
        window.blit(defenses_left_surface1, (attack_choose_button_x_start1, attack_choose_button_y_start1 - 30))  # Added line for defense count display

        # Display the number of elixirs left for each player
        elixirs_left_text0 = f"Elixirs left: {elixir_used0}"  # Added line for elixir count display
        elixirs_left_surface0 = font.render(elixirs_left_text0, True, BLACK)  # Added line for elixir count display
        window.blit(elixirs_left_surface0, (attack_choose_button_x_start0, attack_choose_button_y_start0 - 60))  # Added line for elixir count display

        elixirs_left_text1 = f"Elixirs left: {elixir_used1}"  # Added line for elixir count display
        elixirs_left_surface1 = font.render(elixirs_left_text1, True, BLACK)  # Added line for elixir count display
        window.blit(elixirs_left_surface1, (attack_choose_button_x_start1, attack_choose_button_y_start1 - 60))  # Added line for elixir count display

        pygame.display.flip()

        # Check if 30 seconds have passed to change the background
        if pygame.time.get_ticks() - last_background_change_time > 10000:
            background_image_index = (background_image_index + 1) % len(background_images)
            last_background_change_time = pygame.time.get_ticks()

def draw_text(window, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)  # Display the text for 1 second

play_screen('Team_Rocket', random.choice(["Electric Field", "Infernal Field", "Aquatic Field"]), [0, 1, 2], [3, 4, 5], 1, 5, None, None)