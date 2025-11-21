"""A module containing the developer configuration."""

import pygame
pygame.font.init()

base_speed: int = 5 # default: 100
required_ability_charge: int = 2000 # in miliseconds

mouse_wheel_magnitude: int = 15

settings_path: str = "game/data/settings.json"
main_save_path: str = "game/data/saves/main_save.json"
back_save_path: str = "game/data/saves/backup_save.json"
sounds_path: str = "game/audio/sounds/"
sequences_path: str = "game/audio/sequences/"
images_path: str = "game/images/"
# TODO: add other file paths

font_normal = pygame.font.SysFont(None, 14)
font_large = pygame.font.SysFont(None, 20)

framerates: tuple[int, ...] = (30, 60, 120, 144, 240)
resolutions: list[tuple[int, int]] = [
    (1080, 2340), (1080, 1920), (480, 640),
    (1080, 1080),
    (640, 480), (1920, 1080), (2340, 1080)
]
music_volumes: list[int] = list(range(11))

global_colorkey = pygame.Color(1,2,3)
