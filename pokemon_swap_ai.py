import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

def setup_fuzzy_logic():
    # Define fuzzy variables
    health = ctrl.Antecedent(np.arange(0, 101, 1), 'health')
    attack_power = ctrl.Antecedent(np.arange(0, 101, 1), 'attack_power')
    field_type = ctrl.Antecedent(np.arange(0, 3, 1), 'field_type')  # 0: Electric, 1: Infernal, 2: Aquatic
    suitability = ctrl.Consequent(np.arange(0, 101, 1), 'suitability')

    health.automf(3)  # Low, Medium, High
    attack_power.automf(3)  # Weak, Moderate, Strong
    field_type.automf(3)  # Electric, Infernal, Aquatic
    suitability.automf(3)  # Low, Medium, High

    rules = [
        ctrl.Rule(health['poor'] & attack_power['good'], suitability['good']),
        ctrl.Rule(health['average'] & attack_power['average'], suitability['average']),
        ctrl.Rule(health['good'] & attack_power['poor'], suitability['poor']),
        ctrl.Rule(field_type['poor'] & attack_power['average'], suitability['average']),
        ctrl.Rule(health['average'] & attack_power['good'], suitability['good']),
        ctrl.Rule(health['good'] & attack_power['average'], suitability['average']),
        ctrl.Rule(health['poor'] & attack_power['poor'], suitability['poor']),
        ctrl.Rule(health['average'] & attack_power['poor'], suitability['poor']),
        ctrl.Rule(health['good'] & attack_power['good'], suitability['good'])
    ]

    suitability_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(suitability_ctrl)

fuzzy_sim = setup_fuzzy_logic()

def select_pokemon(pokemon_numbers, pokemon_healths, opponent_pokemon, field_type):
    field_type_mapping = {
        "Electric Field": 0,
        "Infernal Field": 1,
        "Aquatic Field": 2
    }

    field_type_value = field_type_mapping.get(field_type, 0)  # Default to 0 if field type not found

    best_pokemon = None
    best_suitability = -1

    for i, pokemon in enumerate(pokemon_numbers):
        if pokemon_healths[i] > 0:
            fuzzy_sim.input['health'] = pokemon_healths[i]
            fuzzy_sim.input['attack_power'] = np.random.choice([30, 50, 70, 90])  # Example values to ensure activation of rules
            fuzzy_sim.input['field_type'] = field_type_value

            fuzzy_sim.compute()

            suitability = fuzzy_sim.output['suitability']
            if suitability > best_suitability:
                best_suitability = suitability
                best_pokemon = i

    return best_pokemon
