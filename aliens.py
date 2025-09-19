"""
A module containing all the aliens.
"""

import pygame
from entity import Entity

class Alien(Entity):
    """Base class that manages the aliens."""

    def __init__(self, game_screen):
        """Initialize the alien."""

        super().__init__(game_screen)

        # TODO: load alien as an image
        self.color = "red"

        # spawn enemy above the screen
        self.topbound = - self.rect.height
        self.rect.midbottom = self.screen_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the alien to move downwards
        self.base_speed_y = 25
        self.speed_x, self.speed_y = self._calculate_relative_speed()
        self.moving_down = True

        # alien stats
        self.hp = 2
        self.speed = 1
        self.damage = 1
        self.credits = 10
    
