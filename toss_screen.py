import pygame
import sys
import random
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1500, 770
WINDOW_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 50)
spinner_sound = pygame.mixer.Sound('Resources/sound_spinner.mp3')

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Updated toss function
def toss(selected_index):
    if selected_index == 0:
        return "Team Rocket"
    elif selected_index == 1:
        return "Me(Ash)"

# Function to calculate fitness values for all Pokémon
def calculate_fitness(player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs):
    fitness_values_0 = []
    fitness_values_1 = []

    for i in range(len(player_0_pokemon_indices)):
        fitness = (((player_0_pokemon_indices[i] + 1) * 5) + player_0_costs[i])
        fitness_values_0.append(fitness)

    for i in range(len(player_1_pokemon_indices)):
        fitness = (((player_1_pokemon_indices[i] + 1) * 5) + player_1_costs[i])
        fitness_values_1.append(fitness)
    
    total_fitness_0 = sum(fitness_values_0)
    total_fitness_1 = sum(fitness_values_1)

    return total_fitness_0, total_fitness_1

# Function to perform rank selection and print ranks
def rank_selection(fitness_values):
    sorted_indices = np.argsort(fitness_values)[::1]  # Sort indices based on fitness values in descending order
    total_ranks = sum(range(1, len(fitness_values) + 1))
    selection_probabilities = [rank / total_ranks for rank in range(len(fitness_values), 0, -1)]
    
    # Print the ranks of the Pokémon based on their fitness values
    ranks = np.argsort(sorted_indices)
    print("Ranks based on fitness values (higher rank means better fitness):")
    for idx, rank in enumerate(ranks):
        print(f"Pokémon Index {idx}: Rank {rank + 1}, Fitness Value {fitness_values[sorted_indices[idx]]}")
    
    selected_index = sorted_indices[0]  # Selecting the highest fitness value
    return selected_index

# Main function to encapsulate the entire toss and selection process
def toss_screen(player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs):
    angle = 0
    rotation_speed = 1  
    toss_result = None
    toss_started = False
    spin_duration = 0
    current_toss = None

    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Toss Screen")
 
    background_image = pygame.image.load('Resources/board_toss.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    spinner_img = pygame.image.load('Resources/spinner_toss.png')
    spinner_img = pygame.transform.scale(spinner_img, (350, 350))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not toss_started:   
                toss_started = True
                rotation_speed = 10 
                fitness_values = calculate_fitness(player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs)
                selected_index = rank_selection(fitness_values)
                current_toss = toss(selected_index)
                spinner_sound.play() 

        if toss_started:
            angle += rotation_speed
            angle %= 360

            if rotation_speed > 0:
                spin_duration += 1
                if spin_duration >= 200:  
                    rotation_speed = 0
                    toss_result = current_toss
                    spinner_sound.stop() 
                    
            if spin_duration % 15 == 0:  
                current_toss = toss(selected_index)

        window.fill(WHITE)
        window.blit(background_image, (0, 0))

        spinner_rotated = pygame.transform.rotate(spinner_img, -angle)
        spinner_rect = spinner_rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 55))
        window.blit(spinner_rotated, spinner_rect)
        
        if not toss_started:
            draw_text("Press any button to toss", font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 170)
        elif toss_result is None:
            draw_text("Tossing: " + current_toss, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 170)
        else:
            draw_text("Toss Result: " + toss_result, font, BLACK, window, WIDTH // 2, HEIGHT // 2 + 170)
            
            pygame.time.delay(2000)  # Delay before returning

            return toss_result, selected_index

        pygame.display.flip()
        clock.tick(60)

# Example usage
#player_0_pokemon_indices = [2, 4, 5]  # Example indices
#player_0_costs = [10, 15, 20]  # Example costs
#
#player_1_pokemon_indices = [1, 3, 0]  # Example indices
#player_1_costs = [5, 10, 15]  # Example costs
#
#toss_result, selected_index = toss_screen(player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs)
#print(f"Toss Winner: {toss_result}, Selected Pokemon Index: {selected_index}")