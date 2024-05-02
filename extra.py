import pygame

# Initialize Pygame
pygame.init()

# Load the sound file
sound = pygame.mixer.Sound('Resources/sound_electric.mp3')

print(sound.get_length())