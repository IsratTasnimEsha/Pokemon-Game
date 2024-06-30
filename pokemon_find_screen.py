import pygame
import sys
import random
import heapq
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font initialization for displaying text
font = pygame.font.SysFont(None, 50)
font2 = pygame.font.SysFont(None, 30)

player_0_pokemon_indices = []
player_1_pokemon_indices = []

# Arrays to store costs for each player to catch 3 pokemons
player_0_costs = [0, 0, 0]  # Initialize with zeros
player_1_costs = [0, 0, 0]  # Initialize with zeros

player0_image = pygame.image.load('Resources/dashboard_player_0.png')
player0_image = pygame.transform.scale(player0_image, (80, 80))
player1_image = pygame.image.load('Resources/dashboard_player_1.png')
player1_image = pygame.transform.scale(player1_image, (80, 80))

# Helper function to draw text on screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# A* algorithm function to find the shortest path
def astar(adjacency_list, start, goal):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (0, start, []))  # (f_cost, node, path)

    while open_list:
        current_cost, current_node, path = heapq.heappop(open_list)

        if current_node == goal:
            return path + [current_node]

        if current_node in closed_set:
            continue

        closed_set.add(current_node)

        for neighbor, cost in adjacency_list[current_node]:
            if neighbor not in closed_set:
                heapq.heappush(open_list, (current_cost + cost, neighbor, path + [current_node]))

    return None  # No path found

# Main function for the Pokemon field screen
def pokemon_find_screen():
    global player_0_costs, player_1_costs, player_0_pokemon_indices, player_1_pokemon_indices

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Pokemon Field Screen")

    # Load and scale background image
    background_image = pygame.image.load('Resources/board_pokemon_find.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Define positions for players and pokemons
    positions = [
        (305, 220), (660, 198), (850, 202), (1175, 235), (435, 374), (650, 364),
        (838, 369), (1032, 370), (314, 531), (641, 526), (841, 528), (1170, 537)
    ]

    random_numbers = random.sample(range(12), 8)

    pokemon_positions = [positions[random_numbers[0]], positions[random_numbers[1]], positions[random_numbers[2]],
                         positions[random_numbers[3]], positions[random_numbers[4]], positions[random_numbers[5]]]
    player_0_position = positions[random_numbers[6]]
    player_1_position = positions[random_numbers[7]]

    # Adjacency list representation of the graph
    adjacency_list = {
        0: [(4, 3), (8, 4), (5, 2)], 
        1: [(2, 5), (5, 3), (6, 2), (4, 4)], 
        2: [(1, 5), (3, 4), (6, 2)], 
        3: [(2, 4), (6, 5), (7, 2)], 
        4: [(0, 3), (1, 4), (5, 1), (8, 3), (9, 2)], 
        5: [(0, 2), (1, 3), (4, 1), (6, 2), (9, 3), (10, 5)], 
        6: [(1, 2), (2, 2), (3, 5), (5, 2), (7, 3), (9, 4), (10, 2), (11, 3)], 
        7: [(3, 2), (6, 3), (10, 1), (11, 4)], 
        8: [(0, 4), (4, 3)], 
        9: [(4, 2), (5, 3), (6, 4)], 
        10: [(5, 5), (6, 2), (7, 1), (11, 1)], 
        11: [(6, 3), (7, 4), (10, 1)]
    }

    # Start node for player 1
    player_0_node = random_numbers[6]
    player_1_node = random_numbers[7]
    
    # Function to get the next target for Player 0
    def get_next_target():
        for i, pos in enumerate(pokemon_positions):
            if pos is not None:
                return i
        return None

    # Find path from player_0_node to the next pokemon
    current_target_index = get_next_target()
    path_to_pokemon = astar(adjacency_list, player_0_node, random_numbers[current_target_index]) if current_target_index is not None else []

    #if path_to_pokemon:
    #    print("Shortest path found:", path_to_pokemon)

    # Boolean to track if space was pressed
    space_pressed = False

    def get_node_from_position(pos):
        for index, node_pos in enumerate(positions):
            node_rect = pygame.Rect(node_pos[0] - 45, node_pos[1] - 45, 90, 90)  # Define the 90x90 area
            if node_rect.collidepoint(pos):
                return index
        return None

    # Counter for traversing the path
    path_counter = 0

    # Timestamp for player 0's next move
    player_0_next_move_time = 100  # Delay for Player 0's movement

    # Game loop
    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                clicked_node = get_node_from_position(mouse_pos)
                if clicked_node is not None and clicked_node != player_1_node and len(player_1_pokemon_indices) < 3:
                    # Check if the clicked node is adjacent
                    if any(adj_node == clicked_node for adj_node, cost in adjacency_list[player_1_node]):
                        for adj_node, cost_value in adjacency_list[player_1_node]:
                            if adj_node == clicked_node:
                                player_1_costs[len(player_1_pokemon_indices)] += cost_value
                                break
                        player_1_node = clicked_node
                        space_pressed = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not space_pressed:
                    space_pressed = True
                    # Check if Player 1's node overlaps with any Pokemon's position
                    for j, pokemon_pos in enumerate(pokemon_positions):
                        if pokemon_pos is not None and positions[player_1_node] == pokemon_pos:
                            # Display the Pokemon index (j) on the screen
                            pokemon_positions[j] = None
                            player_1_pokemon_indices.append(j)

        window.fill(WHITE)
        window.blit(background_image, (0, 0))

        # Draw pokemons
        pokemon_images = [
            pygame.transform.scale(pygame.image.load('Resources/pokemon_0.png'), (70, 70)),
            pygame.transform.scale(pygame.image.load('Resources/pokemon_1.png'), (70, 70)),
            pygame.transform.scale(pygame.image.load('Resources/pokemon_2.png'), (70, 70)),
            pygame.transform.scale(pygame.image.load('Resources/pokemon_3.png'), (70, 70)),
            pygame.transform.scale(pygame.image.load('Resources/pokemon_4.png'), (70, 70)),
            pygame.transform.scale(pygame.image.load('Resources/pokemon_5.png'), (70, 70))
        ]

        for j, (img, pos) in enumerate(zip(pokemon_images, pokemon_positions)):
            if pos is not None:
                window.blit(img, pos)

        # Draw the static player image 1
        player_image_0 = pygame.transform.scale(pygame.image.load('Resources/dashboard_player_0.png'), (70, 70))
        player_image_1 = pygame.transform.scale(pygame.image.load('Resources/dashboard_player_1.png'), (70, 70))
        
        if current_time >= player_0_next_move_time and len(player_0_pokemon_indices) < 3:
            if path_counter < len(path_to_pokemon):
                next_node = path_to_pokemon[path_counter]
                for adj_node, cost_value in adjacency_list[player_0_node]:
                    if adj_node == next_node:
                        player_0_costs[len(player_0_pokemon_indices)] += cost_value
                        break
                player_0_node = next_node
                path_counter += 1
                # Check if the current target is still available
                if positions[random_numbers[current_target_index]] != pokemon_positions[current_target_index]:
                    # Recalculate path if the target Pokémon has been caught
                    current_target_index = get_next_target()
                    if current_target_index is not None:
                        path_to_pokemon = astar(adjacency_list, player_0_node, random_numbers[current_target_index])
                        path_counter = 0
            else:
                player_0_node = path_to_pokemon[-1]  # Ensure final position is shown
                
                # Check if Player 0 has reached a Pokemon
                for j, pokemon_pos in enumerate(pokemon_positions):
                    if pokemon_pos is not None and positions[player_0_node] == pokemon_pos:
                        # Player 0 catches the Pokemon
                        pokemon_positions[j] = None
                        player_0_pokemon_indices.append(j)
                        
                        # Get the next target and find a new path
                        current_target_index = get_next_target()
                        if current_target_index is not None:
                            path_to_pokemon = astar(adjacency_list, player_0_node, random_numbers[current_target_index])
                            path_counter = 0
                        break
            
            player_0_next_move_time = current_time + 2500  # Set next move time for Player 0

        window.blit(player_image_0, positions[player_0_node])
        window.blit(player_image_1, positions[player_1_node])

        if len(player_0_pokemon_indices) == 1:
            window.blit(pokemon_images[player_0_pokemon_indices[0]], (80, 20))
        elif len(player_0_pokemon_indices) == 2:
            window.blit(pokemon_images[player_0_pokemon_indices[0]], (80, 20))
            window.blit(pokemon_images[player_0_pokemon_indices[1]], (275, 20))
        elif len(player_0_pokemon_indices) == 3:
            window.blit(pokemon_images[player_0_pokemon_indices[0]], (80, 20))
            window.blit(pokemon_images[player_0_pokemon_indices[1]], (275, 20))
            window.blit(pokemon_images[player_0_pokemon_indices[2]], (470, 20))

        # Display caught pokemons for player 1
        if len(player_1_pokemon_indices) == 1:
            window.blit(pokemon_images[player_1_pokemon_indices[0]], (950, 20))
        elif len(player_1_pokemon_indices) == 2:
            window.blit(pokemon_images[player_1_pokemon_indices[0]], (950, 20))
            window.blit(pokemon_images[player_1_pokemon_indices[1]], (1145, 20))
        elif len(player_1_pokemon_indices) == 3:
            window.blit(pokemon_images[player_1_pokemon_indices[0]], (950, 20))
            window.blit(pokemon_images[player_1_pokemon_indices[1]], (1145, 20))
            window.blit(pokemon_images[player_1_pokemon_indices[2]], (1340, 20))

        window.blit(player0_image, (662, 25))
        window.blit(player1_image, (760, 25))

        ######################################################### Define positions for players and pokemons

        #player_image = pygame.image.load('Resources/board_toss.jpg')
        #player_image = pygame.transform.scale(player_image, (70, 70))
        #window.blit(player_image, (1170, 537))
        #, , , , 
        #
########################################################

        pygame.display.flip()

        # Check if all 6 pokemons are caught
        if len(player_0_pokemon_indices) + len(player_1_pokemon_indices) == 6:
            pygame.time.wait(2000)  # Wait for 2000ms
            return player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs

# Run the main function and get the result
player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs = pokemon_find_screen()
print("Player 0 Pokemon Indices:", player_0_pokemon_indices)
print("Player 1 Pokemon Indices:", player_1_pokemon_indices)
print("Player 0 Costs:", player_0_costs)
print("Player 1 Costs:", player_1_costs)