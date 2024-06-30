import pygame
import sys
import random
from pokemon_find_screen import pokemon_find_screen
from toss_screen import toss_screen
from play_screen import play_screen
from battle_field_screen import battle_field_screen
from pokemon_round_1_screen import pokemon_round_1_screen

player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs = pokemon_find_screen()
print("Player_0 pokemons and cost:")
print(player_0_pokemon_indices)
print(player_0_costs)
print("Player_1 pokemons and cost:")
print(player_1_pokemon_indices)
print(player_1_costs)

toss_result, selected_index = toss_screen(player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs)
print(f"Toss Winner: {toss_result}, Selected Pokemon Index: {selected_index}")

selected_field = None
field_options = ["Electric Field", "Infernal Field", "Aquatic Field"]

round_1_pokemon0 = None
round_1_pokemon1 = None
round_2_pokemon0 = None
round_2_pokemon1 = None

if toss_result == 'Team Rocket':
    for i in range(3):
        if i + 3 in player_0_pokemon_indices:
            selected_field = field_options[i]
            round_1_pokemon0 = i + 3
            break
    else:
        for num in player_0_pokemon_indices:
            if num in range(3):
                selected_field = field_options[num]
                round_1_pokemon0 = num
                break

elif toss_result == 'Me(Ash)':
    selected_field = battle_field_screen(player_0_pokemon_indices, player_1_pokemon_indices)

round_1_pokemon1 = pokemon_round_1_screen(player_0_pokemon_indices, player_1_pokemon_indices, round_1_pokemon0)
play_screen(toss_result, selected_field, player_0_pokemon_indices, player_1_pokemon_indices, round_1_pokemon0, round_1_pokemon1, round_2_pokemon0, round_2_pokemon1)