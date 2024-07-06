def triangular_membership(x, a, b, c):
    """Triangular membership function."""
    if a == b and b == c:
        return 1 if x == a else 0
    elif a == b:
        return max(min(1, (c - x) / (c - b)), 0)
    elif b == c:
        return max(min((x - a) / (b - a), 1), 0)
    else:
        return max(min((x - a) / (b - a), (c - x) / (c - b)), 0)

def get_score(current_field_index, player0_index, player1_index):
    """Calculates the combined field and matchup score."""
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
    score = field_scores[current_field_index].get((player0_index, player1_index), float('-inf'))
    return score

def calculate_suitability(score):
    """Calculates suitability using a triangular membership function."""
    if score < 0:
        return triangular_membership(score, -10, -5, 0)
    elif score == 0:
        return 0.5  # Neutral score has a fixed membership value
    else:
        return triangular_membership(score, 0, 5, 10)

def find_best_pokemon_index(player0_current_pokemon_index, player1_current_pokemon_index, current_field_index, player0_healths, elixir0):
    """Finds the best Pokémon index for player0 using fuzzy logic."""
    
    # Map field types to indices
    field_mapping = {'electric': 0, 'fire': 1, 'water': 2}
    current_field_index = field_mapping.get(current_field_index, -1)

    if current_field_index == -1:
        return None

    best_index = None
    best_suitability = float('-inf')
    
    # Check all possible Pokémon indices for player0
    for player0_index in range(3):
        if player0_healths[player0_index] == 0:
            continue
        score = get_score(current_field_index, player0_index, player1_current_pokemon_index)
        suitability = calculate_suitability(score)
        print(f"Suitability for player0_index {player0_index}: {suitability}")
        if suitability > best_suitability:
            best_suitability = suitability
            best_index = player0_index

    # If current Pokémon has 0 HP, decide whether to drink elixir or switch Pokémon
    if player0_healths[player0_current_pokemon_index] == 0:
        if len(elixir0) != 0:
            print("Drinking elixir for current Pokémon")
            return player0_current_pokemon_index  # Drink elixir
        elif best_index is not None:
            print("Switching to another Pokémon with HP")
            return best_index  # Switch to another Pokémon with HP

    # Check if all Pokémon have 0 HP
    if best_index is not None:
        print("Switching to the best available Pokémon")
        return best_index

    print("All Pokémon have 0 HP")
    return None  # Return None if all Pokémon have 0 HP

# Example usage
#player0_current_pokemon = 0  # Example value
#player1_current_pokemon = 1  # Example value
#current_field = 'fire'  # Example value
#player0_healths = [0,0,0]  # Example health values
#elixir0 = [1]  # Example elixir values (can be empty)

#best_pokemon_index = find_best_pokemon_index(player0_current_pokemon, player1_current_pokemon, current_field, player0_healths, elixir0)
#print("Best Pokémon index for player0:", best_pokemon_index)