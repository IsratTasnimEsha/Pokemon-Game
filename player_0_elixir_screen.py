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

player0_best_elixirs = [0, 0, 0, 0, 0]

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

# Genetic Algorithm parameters
population_size = 50
max_generations = 100
mutation_rate = 0.1

# Function to generate an initial population randomly
def generate_initial_population(population_size, num_items):
    population = []
    for _ in range(population_size):
        chromosome = [random.randint(0, 1) for _ in range(num_items)]
        population.append(chromosome)
    return population

# Function to evaluate fitness of a chromosome (solution)
def fitness(chromosome, weight_profit, capacity):
    total_weight = 0
    total_profit = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_weight += weight_profit[i][0]
            total_profit += weight_profit[i][1]
    if total_weight > capacity:
        return 0  # Penalize solutions that exceed capacity
    else:
        return total_profit

# Function to perform tournament selection
def tournament_selection(population, fitness_values, tournament_size):
    selected = []
    for _ in range(len(population)):
        candidates = random.sample(list(enumerate(population)), tournament_size)
        winner = max(candidates, key=lambda x: fitness_values[x[0]])
        selected.append(winner[1])
    return selected

# Function to perform crossover (single-point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Function to perform mutation
def mutation(chromosome, mutation_rate):
    mutated_chromosome = []
    for gene in chromosome:
        if random.random() < mutation_rate:
            mutated_chromosome.append(1 - gene)  # Flip the bit
        else:
            mutated_chromosome.append(gene)
    return mutated_chromosome

# Function to evolve the population using genetic algorithm
def genetic_algorithm(weight_profit, capacity, population_size, max_generations, mutation_rate):
    num_items = len(weight_profit)
    population = generate_initial_population(population_size, num_items)
    
    for generation in range(max_generations):
        fitness_values = [fitness(chromosome, weight_profit, capacity) for chromosome in population]
        
        # Select parents for crossover
        selected_population = tournament_selection(population, fitness_values, 5)
        
        # Perform crossover to create offspring
        offspring_population = []
        for i in range(0, population_size, 2):
            child1, child2 = crossover(selected_population[i], selected_population[i+1])
            offspring_population.append(child1)
            offspring_population.append(child2)
        
        # Mutate some offspring
        mutated_offspring = [mutation(chromosome, mutation_rate) for chromosome in offspring_population]
        
        # Replace the population with the new generation (offspring)
        population = mutated_offspring
    
    # Find the best solution in the final population
    final_fitness_values = [fitness(chromosome, weight_profit, capacity) for chromosome in population]
    best_index = final_fitness_values.index(max(final_fitness_values))
    best_solution = population[best_index]
    best_profit = max(final_fitness_values)
    
    return best_solution

def player_0_elixir_screen(elixir_price_power, remaining):
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

    clicked_positions = [False] * 5
    sum_of_power = 0

    best_solution = genetic_algorithm(elixir_price_power, remaining, population_size, max_generations, mutation_rate)
    #print(best_solution)

    for i in range (len(best_solution)):
        if best_solution[i] == 1:
            window.blit(owned_images[i], elixir_positions[i])

    def draw_static_elements(remaining):

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

        # Redraw the owned images
        sum_of_power = 0

        for i in range(5):
            if best_solution[i] == 1:
                window.blit(owned_images[i], elixir_positions[i])
                remaining -= elixir_price_power[i][0]
                player0_best_elixirs[i] = elixir_price_power[i][1]
                sum_of_power += elixir_price_power[i][1]
        
        draw_text_with_outline(f"Remaining:", font2, WHITE, BLACK, window, 1270, 330)
        draw_text_with_outline(f"{remaining}", font3, WHITE, BLACK, window, 1270, 370)

        draw_text_with_outline(f"Power:", font2, WHITE, BLACK, window, 1270, 430)
        draw_text_with_outline(f"{sum_of_power}", font3, WHITE, BLACK, window, 1270, 470)

        window.blit(owned_images[i], elixir_positions[i])

    draw_static_elements(remaining)

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

        pygame.display.flip()

        pygame.time.wait(2000)  # Wait for 2000ms
        return elixir_price_power, remaining, player0_best_elixirs

#print(player_0_elixir_screen([(9, 3), (9, 15), (7, 18), (10, 17), (3, 11)], 19))