import pygame.font

class Config():
    """Represents a class which contains the developer configuration."""

    def __init__(self):
        """Initialize the config object."""

        self.base_speed = 100
        self.required_ability_charge = 2000 # in miliseconds

        self.mouse_wheel_magnitude = 5

        self.settings_path = "game/data/settings.json"
        self.main_save_path = "game/data/saves/main_save.json"
        self.back_save_path = "game/data/saves/backup_save.json"
        self.sounds_path = "game/audio/sounds/"
        self.sequences_path = "game/audio/sequences/"
        # TODO: add other file paths

        self.font_normal = pygame.font.SysFont(None, 14)
        self.font_large = pygame.font.SysFont(None, 21)

        self.framerates = (30, 60, 120, 144, 240)
        self.music_volumes = range(11)

        self.global_colorkey = pygame.Color(1,2,3)

__all__ = ["Config"]