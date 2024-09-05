def fuzzify_score(score):
    """Fuzzify the score into fuzzy membership values."""
    if score <= -8:
        return {'low': 1.0, 'medium': 0.0, 'high': 0.0}
    elif -8 < score < 0:
        return {'low': (0 - score) / 8, 'medium': 1 - abs(score) / 8, 'high': 0.0}
    elif 0 <= score <= 8:
        return {'low': 0.0, 'medium': score / 8, 'high': 1.0}
    else:
        return {'low': 0.0, 'medium': 0.0, 'high': 1.0}

def rule_evaluation(fuzzy_values):
    """Evaluate fuzzy rules to get fuzzy results."""
    # Simple rule: higher score should correspond to higher suitability
    return fuzzy_values['medium'] * 0.5 + fuzzy_values['high'] * 1.0

def defuzzify(suitability):
    """Convert fuzzy suitability to a crisp value."""
    return suitability

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

def find_best_pokemon_index(player0_current_pokemon_index, player1_current_pokemon_index, current_field_index, player0_healths, elixir0):
    """Finds the best Pokémon index for player0 using fuzzy logic."""
    
    # Map field types to indices
    field_mapping = {'electric': 0, 'fire': 1, 'water': 2}
    current_field_index = field_mapping.get(current_field_index, -1)

    if current_field_index == -1:
        return None

    best_suitability = float('-inf')

    suitabilities = []

    for player0_index in range(3):
        if player0_healths[player0_index] == 0 and player0_index != player0_current_pokemon_index:
            continue
        score = get_score(current_field_index, player0_index, player1_current_pokemon_index)
        fuzzy_values = fuzzify_score(score)
        suitability = rule_evaluation(fuzzy_values)
        crisp_suitability = defuzzify(suitability)
        print(f"Suitability for player0_index {player0_index}: {crisp_suitability}")
        suitabilities.append((player0_index, crisp_suitability))

    # Sort the indices according to suitability
    sorted_indices = [index for index, suitability in sorted(suitabilities, key=lambda x: x[1], reverse=True)]

    print(f"Sorted player0_indices according to suitability: {sorted_indices}")
    if len(sorted_indices) == 0:
        return None
    else:
        return sorted_indices[0]

#best_pokemon_index = find_best_pokemon_index(0, 0, 'electric', [100, 20, 70], [40, 30, 50])
#print("Best Pokémon index for player0:", best_pokemon_index)