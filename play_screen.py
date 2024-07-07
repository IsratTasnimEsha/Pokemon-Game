import pygame
import random
import time
import sys
from fuzzy_logic_decision import find_best_pokemon_index

pygame.init()

move = 0
moves = 0
bg_index = 0

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

#-------------------------------------------------------Colors-------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255, 128)
RED = (255, 0, 0, 128)
TRANSPARENT = (255, 255, 255, 128)

radius = 100

#-------------------------------------------------------Fonts-------------------------------------------------------
font = pygame.font.SysFont("comicsansms", 15)
font2 = pygame.font.SysFont("comicsansms", 25)
font3 = pygame.font.SysFont("comicsansms", 50)

attack_choose_button_x_start0 = -80
attack_choose_button_y_start0 = 680

attack_choose_button_x_start1 = 1260 
attack_choose_button_y_start1 = 680

attack_choose_button_width, attack_choose_button_height = 100, 50
attack_choose_button_spacing = 5

target_x0 = 1060
target_y0 = 350

target_x1 = 300
target_y1 = 350

speed0 = 50
speed1 = 50

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

def get_score(current_field_index, player0_current_pokemon_index, player1_current_pokemon_index):
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
        return 'Attack'
    else:
        return 'Defense'

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
    health_bar_width = int((health / max_health) * width)
    pygame.draw.rect(window, GRAY, (x, y, width, height))
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
    global move, moves, bg_index, target_x, target_y

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Play Screen")

    current_attack_choose_button_clicked0 = None
    current_attack_choose_button_clicked1 = None

    defense_used0 = False
    defense_used1 = False

    player_turn = False

    max_health = 100
    player0_healths = [max_health] * 3
    player1_healths = [max_health] * 3

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
    computer_action_text0 = ""
    computer_action_text1 = ""

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

    #-------------------------------------------------------Elixir Images-------------------------------------------------------
    elixir0_image = pygame.image.load(f'Resources/elixir0.png')
    elixir0_image = pygame.transform.scale(elixir0_image, (50, 80))
    elixir1_image = pygame.image.load(f'Resources/elixir1.png')
    elixir1_image = pygame.transform.scale(elixir1_image, (50, 80))
    elixir2_image = pygame.image.load(f'Resources/elixir2.png')
    elixir2_image = pygame.transform.scale(elixir2_image, (50, 80))
    elixir3_image = pygame.image.load(f'Resources/elixir3.png')
    elixir3_image = pygame.transform.scale(elixir3_image, (50, 80))

    transparent_rect = pygame.Surface((120, 100), pygame.SRCALPHA)
    transparent_rect.fill(TRANSPARENT)
    pygame.draw.rect(transparent_rect, BLACK, transparent_rect.get_rect(), 3)

    #-------------------------------------------------------Pokemon Attack Images-------------------------------------------------------
    player0_pokemon_attack_images = [None] * 3
    player1_pokemon_attack_images = [None] * 3
    player0_pokemon_attack_images_rect = [None] * 3
    player1_pokemon_attack_images_rect = [None] * 3
    
    player0_pokemon_attack_images[0] = pygame.image.load('Resources/pokemon_0_attack_0.png')
    player0_pokemon_attack_images[0] = pygame.transform.scale(player0_pokemon_attack_images[0], (100, 50))
    player0_pokemon_attack_images_rect[0] = player0_pokemon_attack_images[0].get_rect()
    player0_pokemon_attack_images_rect[0].topleft = (50, 100)

    player1_pokemon_attack_images[0] = pygame.image.load('Resources/pokemon_0_attack_1.png')
    player1_pokemon_attack_images[0] = pygame.transform.scale(player1_pokemon_attack_images[0], (100, 50))
    player1_pokemon_attack_images_rect[0] = player1_pokemon_attack_images[0].get_rect()
    player1_pokemon_attack_images_rect[0].topleft = (50, 100)

    player0_pokemon_attack_images[1] = pygame.image.load('Resources/pokemon_1_attack_0.png')
    player0_pokemon_attack_images[1] = pygame.transform.scale(player0_pokemon_attack_images[1], (100, 50))
    player0_pokemon_attack_images_rect[1] = player0_pokemon_attack_images[1].get_rect()
    player0_pokemon_attack_images_rect[1].topleft = (50, 100)

    player1_pokemon_attack_images[1] = pygame.image.load('Resources/pokemon_1_attack_1.png')
    player1_pokemon_attack_images[1] = pygame.transform.scale(player1_pokemon_attack_images[1], (100, 50))
    player1_pokemon_attack_images_rect[1] = player1_pokemon_attack_images[1].get_rect()
    player1_pokemon_attack_images_rect[1].topleft = (50, 100)

    player0_pokemon_attack_images[2] = pygame.image.load('Resources/pokemon_2_attack_0.png')
    player0_pokemon_attack_images[2] = pygame.transform.scale(player0_pokemon_attack_images[2], (100, 50))
    player0_pokemon_attack_images_rect[2] = player0_pokemon_attack_images[2].get_rect()
    player0_pokemon_attack_images_rect[2].topleft = (50, 100)

    player1_pokemon_attack_images[2] = pygame.image.load('Resources/pokemon_2_attack_1.png')
    player1_pokemon_attack_images[2] = pygame.transform.scale(player1_pokemon_attack_images[2], (100, 50))
    player1_pokemon_attack_images_rect[2] = player1_pokemon_attack_images[2].get_rect()
    player1_pokemon_attack_images_rect[2].topleft = (50, 100)

    image_visible0 = False
    button_clicked0 = False

    image_visible1 = False
    button_clicked1 = False

    circle_drawn0 = False
    circle_start_time0 = None

    circle_drawn1 = False
    circle_start_time1 = None

    #-------------------------------------------------------Pokemon Attack Images-------------------------------------------------------
    image0 = player0_pokemon_attack_images[0]
    initial_position0 = (350, 350)  
    image_rect0 = image0.get_rect()
    image_rect0.topleft = initial_position0

    image1 = player1_pokemon_attack_images[0]
    initial_position1 = (1050, 350) 
    image_rect1 = image1.get_rect()
    image_rect1.topleft = initial_position1

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
        
        if(sum(player0_healths) == 300):
            current_pokemon_index0 = find_best_pokemon_index(0, current_pokemon_index1, field_type_value, player0_healths, elixir0)

        image0 = player0_pokemon_attack_images[current_pokemon_index0]
        image1 = player1_pokemon_attack_images[current_pokemon_index1]

        #-------------------------------------------------------Pokemon Fighting Images-------------------------------------------------------
        pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index0}_fight.png')
        pokemon_fight_image0 = pygame.transform.scale(pokemon_fight_image0, (130, 150))

        pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index1 + 3}_fight.png')
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
                for i, (img, num) in enumerate(pokemon_button_images1):
                    if pokemon_choose_button_x1[i] <= mouse_x <= pokemon_choose_button_x1[i] + 65 and \
                            pokemon_choose_button_y1 <= mouse_y <= pokemon_choose_button_y1 + 65 and player1_healths[i] > 0:
                        current_pokemon_index1 = i
                        current_pokemon_index1 = player1_numbers[current_pokemon_index1]
                        attack_choose_button_texts1 = pokemon_data1[current_pokemon_index1]['attacks']
                        pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index1 + 3}_fight.png')

                        if current_pokemon_index1 < 3:
                            pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
                        else:
                            pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

                if event.button == 1:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if 1300 <= mouse_x <= 1300 + 120 and 550 <= mouse_y <= 550 + 100:
                        transparent_rect.fill(BLUE)
                        pygame.draw.rect(transparent_rect, BLACK, transparent_rect.get_rect(), 3)

                        if len(elixir1) != 0:
                            if player1_healths[current_pokemon_index1] + elixir1[0] >= 100:
                                player1_healths[current_pokemon_index1] = 100
                            else:
                                player1_healths[current_pokemon_index1] += elixir1[0]
                            elixir1.pop(0)

                if attack_choose_button_x_start1 <= mouse_x <= attack_choose_button_x_start1 + 2 * (attack_choose_button_width + attack_choose_button_spacing) and \
                        attack_choose_button_y_start1 <= mouse_y <= attack_choose_button_y_start1 + 2 * (attack_choose_button_height + attack_choose_button_spacing) and player_turn:

                    col = (mouse_x - attack_choose_button_x_start1) // (attack_choose_button_width + attack_choose_button_spacing)
                    row = (mouse_y - attack_choose_button_y_start1) // (attack_choose_button_height + attack_choose_button_spacing)
                    current_attack_choose_button_clicked1 = int(row * 2 + col)
                    action = attack_choose_button_texts1[current_attack_choose_button_clicked1]

                    computer_action_text1 = f"Ash chose {action}"
                    print(computer_action_text1)

                    if action == "Defense":
                        print(f"{pokemon_data1[current_pokemon_index1]['name']} used Defense!")
                        defense_used1 = True
                        circle_drawn1 = True
                        circle_start_time1 = time.time()

                    if action == "Attack":
                        button_clicked1 = True
                        image_visible1 = True
                        image_rect1.topleft = initial_position1  

                        attacker_type = pokemon_data1[current_pokemon_index1]['type']
                        defender_type = pokemon_data0[current_pokemon_index0]['type']
                        damage = attack_damage(attacker_type, defender_type, field_type_value)  

                        if defense_used0:
                            defense_used0 = False
                        else:    
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
                            draw_text(window, "Team Rocket is defeated!", font3, BLACK, WIDTH // 2, HEIGHT // 2)
                            pygame.display.flip()
                            time.sleep(3)
                            return "Me(Ash)"
                        
                        attack_choose_button_texts0 = pokemon_data0[current_pokemon_index0]['attacks']
                        pokemon_fight_image0 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index0}_fight.png')
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

            computer_action_text0 = f"Team Rocket chose {action}"
            print(computer_action_text0)

            if action == "Defense":
                print(f"{pokemon_data0[current_pokemon_index0]['name']} used Defense!")
                defense_used0 = True
                circle_drawn0 = True
                circle_start_time0 = time.time()

            if action == "Attack":
                button_clicked0 = True
                image_visible0 = True
                image_rect0.topleft = initial_position0 

                attacker_type = pokemon_data0[current_pokemon_index0]['type']
                defender_type = pokemon_data1[current_pokemon_index1]['type']
                damage = attack_damage(attacker_type, defender_type, field_type_value)  

                if defense_used1:
                    defense_used1 = False  
                else:
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
                    draw_text(window, "Ash is defeated!", font3, RED, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    time.sleep(3)
                    return "Team Rocket"

                current_pokemon_index1 = player1_numbers[current_pokemon_index1]
                attack_choose_button_texts1 = pokemon_data1[current_pokemon_index1]['attacks']
                pokemon_fight_image1 = pygame.image.load(f'Resources/pokemon_{current_pokemon_index1 + 3}_fight.png')
                if current_pokemon_index1 < 3:
                    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (130, 150))
                else:
                    pokemon_fight_image1 = pygame.transform.scale(pokemon_fight_image1, (260, 300))

            player_turn = True
        
        if button_clicked0:
            if image_rect0.x < target_x0:
                image_rect0.x += speed0
            if image_rect0.y < target_y0:
                image_rect0.y += speed0

            if image_rect0.x >= target_x0 and image_rect0.y >= target_y0:
                image_visible0 = False
                button_clicked0 = False

        if button_clicked1:
            if image_rect1.x > target_x1:
                image_rect1.x -= speed1
            if image_rect1.y > target_y1:
                image_rect1.y -= speed1

            if image_rect1.x <= target_x1 and image_rect1.y <= target_y1:
                image_visible1 = False
                button_clicked1 = False

        if circle_drawn0:
            if time.time() - circle_start_time0 < 1:
                pygame.draw.circle(window, RED, (WIDTH // 4 - 10, HEIGHT // 2), radius)
            else:
                circle_drawn0 = False

        if circle_drawn1:
            if time.time() - circle_start_time1 < 1:
                pygame.draw.circle(window, BLUE, ((3*WIDTH) // 4 + 30, HEIGHT // 2), radius)
            else:
                circle_drawn1 = False

        #-------------------------------------------------------Players-------------------------------------------------------
        window.blit(player0_image, (50, 80))
        window.blit(player1_image, (WIDTH - 270, 150))  

        #-------------------------------------------------------Health Display-------------------------------------------------------
        health_bar_x0 = attack_choose_button_x_start0 + 2 * (attack_choose_button_width + attack_choose_button_spacing)
        health_bar_x1 = health_bar_x0 + 580  
        health_bar_y = attack_choose_button_y_start0

        draw_health_bar(window, player0_healths[current_pokemon_index0], max_health, health_bar_x0 + 170, health_bar_y + 5, 250, 40)
        draw_health_bar(window, player1_healths[current_pokemon_index1], max_health, health_bar_x1 + 280, health_bar_y + 5, 250, 40)

        health_text_surface0 = font.render(f"Health Remain: {player0_healths[current_pokemon_index0]}%", True, BLACK)
        health_text_rect0 = health_text_surface0.get_rect()
        health_text_rect0.midtop = (health_bar_x0 + 300, health_bar_y + 12)  

        health_text_surface1 = font.render(f"Health Remain: {player1_healths[current_pokemon_index1]}%", True, BLACK)
        health_text_rect1 = health_text_surface1.get_rect()
        health_text_rect1.midtop = (health_bar_x1 + 405, health_bar_y + 12)  # Adjust position as needed

        window.blit(health_text_surface0, health_text_rect0)
        window.blit(health_text_surface1, health_text_rect1)

        computer_action_surface0 = font.render(computer_action_text0, True, WHITE)
        computer_action_rect0 = computer_action_surface0.get_rect(center=(WIDTH // 4, HEIGHT // 4))
        window.blit(computer_action_surface0, computer_action_rect0)

        computer_action_surface1 = font.render(computer_action_text1, True, WHITE)
        computer_action_rect1 = computer_action_surface1.get_rect(center=((3 * WIDTH) // 4, HEIGHT // 4))
        window.blit(computer_action_surface1, computer_action_rect1)

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

        #-------------------------------------------------------Elixir Information-------------------------------------------------------
        if len(elixir1) != 0:
            window.blit(transparent_rect, (1300, 550))

        if len(elixir1) == 4:
            window.blit(elixir0_image, (1305, 560))
        if len(elixir1) == 3:
            window.blit(elixir1_image, (1305, 560))
        if len(elixir1) == 2:
            window.blit(elixir2_image, (1305, 560))
        if len(elixir1) == 1:
            window.blit(elixir3_image, (1305, 560))

        #-------------------------------------------------------Pokemon Attack Buttons-------------------------------------------------------
        draw_attack_choose_buttons(window, attack_choose_button_texts1, attack_choose_button_x_start1, attack_choose_button_y_start1, current_attack_choose_button_clicked1)

        if len(elixir1) != 0:
            draw_text(window, f"+{elixir1[0]}", font2, BLACK, 1380, 600)
        
        if image_visible0:
            window.blit(image0, image_rect0.topleft)
        if image_visible1:
            window.blit(image1, image_rect1.topleft)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def draw_text(window, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

#play_screen([0, 1, 2], [0, 1, 2], 1, [40, 50, 45], [40, 45, 50])