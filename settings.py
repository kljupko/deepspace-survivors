"""
A module containing the classes for user-defined controls and settings.
"""

import pygame

class Settings():
    """A class representing the user settings."""

    def __init__(self):
        """Initialize the user settings object."""

        # TODO: determine how to load user settings
        self.fps = 60
        # TODO: determine how to load user controls
        self.controls = Controls()

class Controls():
    """A class representing the user controls."""

    def __init__(self):
        """Initialize the user controls object."""

        self.move_left = pygame.K_LEFT
        self.move_right = pygame.K_RIGHT

        self.fire = pygame.K_SPACE

        # TODO: change the defaults for a QWERTY layout
        self.active_1 = pygame.K_w
        self.active_2 = pygame.K_f
        self.active_3 = pygame.K_p
        self.passive_1 = pygame.K_a
        self.passive_2 = pygame.K_r
        self.passive_3 = pygame.K_s
        self.passive_4 = pygame.K_t

