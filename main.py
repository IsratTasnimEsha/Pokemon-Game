import pygame
import sys
import random
import cv2
from pokemon_screen import pokemon_screen
from toss_screen import toss_screen
from play_screen import play_screen
from battle_field_screen import battle_field_screen

player0_numbers, player1_numbers = pokemon_screen()
toss_result = toss_screen()

selected_field = None
field_options = ["Aquatic Field", "Infernal Field", "Electric Field"]

if toss_result:
    if toss_result == 'Team Rocket' and selected_field is None:
            selected_field = random.choice(field_options)
    else:
        selected_field = battle_field_screen(player0_numbers, player1_numbers)
                    
    play_screen(toss_result, selected_field, player0_numbers, player1_numbers)