import pygame
import sys
import random
import cv2
from pokemon_screen import pokemon_screen
from toss_screen import toss_screen
from play_screen import play_screen
from battle_field_screen import battle_field_screen
from pokemon_round_1_screen import pokemon_round_1_screen

player0_numbers, player1_numbers = pokemon_screen()
toss_result = toss_screen()

selected_field = None
field_options = ["Electric Field", "Infernal Field", "Aquatic Field"]

round_1_pokemon0 = None
round_1_pokemon1 = None
round_2_pokemon0 = None
round_2_pokemon1 = None

if toss_result == 'Team Rocket':
    for i in range(3):
        if i + 3 in player0_numbers:
            selected_field = field_options[i]
            round_1_pokemon0 = i + 3
            break
    else:
        for num in player0_numbers:
            if num in range(3):
                selected_field = field_options[num]
                round_1_pokemon0 = num
                break

elif toss_result == 'Me(Ash)':
    selected_field = battle_field_screen(player0_numbers, player1_numbers)

round_1_pokemon1 = pokemon_round_1_screen(player0_numbers, player1_numbers, round_1_pokemon0)
play_screen(toss_result, selected_field, player0_numbers, player1_numbers, round_1_pokemon0, round_1_pokemon1, round_2_pokemon0, round_2_pokemon1)