import pygame
from entity import Entity

class Ship(Entity):
    """Class that manages the player ship."""

    def __init__(self, game_screen):
        """Initialize the ship."""
        
        super().__init__(game_screen)

        # TODO: load ship as an image
        self.color = "green"

        # overwrite Entity's center position
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the ship to move horizontally
        self.base_speed_x = 100
        self.speed_x, self.speed_y = self._calculate_relative_speed()
        