"""A module containing the developer configuration."""

import pygame
pygame.font.init()

base_speed = 100
required_ability_charge = 2000 # in miliseconds

mouse_wheel_magnitude = 5

settings_path = "game/data/settings.json"
main_save_path = "game/data/saves/main_save.json"
back_save_path = "game/data/saves/backup_save.json"
sounds_path = "game/audio/sounds/"
sequences_path = "game/audio/sequences/"
images_path = "game/images/"
# TODO: add other file paths

font_normal = pygame.font.SysFont(None, 14)
font_large = pygame.font.SysFont(None, 21)

framerates = (30, 60, 120, 144, 240)
music_volumes = range(11)

global_colorkey = pygame.Color(1,2,3)
