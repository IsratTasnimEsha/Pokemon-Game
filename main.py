import pygame
import sys
import random
from toss_screen import toss_screen
from play_screen import play_screen
from battle_field_screen import battle_field_screen

toss_result = toss_screen()

selected_field = None
field_options = ["Aquatic Field", "Infernal Field", "Electric Field"]

if toss_result:
    if toss_result == 'Team Rocket' and selected_field is None:
            selected_field = random.choice(field_options)
    else:
        selected_field = battle_field_screen('Ash(Me)')
                    
    play_screen(toss_result, selected_field)

