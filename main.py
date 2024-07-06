import pygame
import sys
import random
from pokemon_find_screen import pokemon_find_screen
from play_screen import play_screen
from pokemon_round_1_screen import pokemon_round_1_screen
from result_pokemon_find_screen import result_pokemon_find_screen
from player_1_elixir_screen import player_1_elixir_screen
from player_0_elixir_screen import player_0_elixir_screen

player_0_pokemon_indices, player_1_pokemon_indices, player_0_costs, player_1_costs, winner = pokemon_find_screen()
if winner != None:
    result_pokemon_find_screen(winner)
    exit

print("Player_0 pokemons and cost:")
print(player_0_pokemon_indices)
print(player_0_costs)
print("Player_1 pokemons and cost:")
print(player_1_pokemon_indices)
print(player_1_costs)

elixir_price_power1, remaining_original1, player1_best_elixirs = player_1_elixir_screen()
print(player1_best_elixirs)
elixir_price_power0, remaining0, player0_best_elixirs = player_0_elixir_screen(elixir_price_power1, remaining_original1)
print(player0_best_elixirs)

round_1_pokemon1 = None

round_1_pokemon1 = pokemon_round_1_screen(player_0_pokemon_indices, player_1_pokemon_indices)

play_screen([0, 1, 2], [0, 1, 2], round_1_pokemon1 - 3, player0_best_elixirs, player1_best_elixirs)