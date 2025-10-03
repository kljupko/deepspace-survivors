import pygame.font

class Config():
    """Represents a class which contains the developer configuration."""

    def __init__(self):
        """Initialize the config object."""

        self.base_speed = 100
        self.required_ability_charge = 2000 # in miliseconds
        # TODO: add file paths
        self.font_normal = pygame.font.SysFont(None, 14)
        self.font_large = pygame.font.SysFont(None, 21)