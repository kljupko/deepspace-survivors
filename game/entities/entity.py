"""
A module containing the base Entity class, parent to Ship, Alien, etc.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

import pygame
from pygame.sprite import Sprite
from ..utils import helper_funcs

class BoundsDict(TypedDict):
    """A class representing a dictionary containing entity bounds."""

    top: int
    bottom: int
    left: int
    right: int

class Entity(Sprite):
    """
    Class that manages the base game entities. Serves as the base from
    which other game objects inherit methods and properties.
    """

    name = "Base Entity"
    default_image: pygame.Surface = helper_funcs.load_image()

    def __init__(self,
                 game: Game,
                 image: pygame.Surface | None = None
                 ):
        """Initialize the entity."""
        
        super().__init__()
        self.game = game

        if image is None:
            image = helper_funcs.copy_image(Entity.default_image)
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()

        # start at the center of the screen
        self.rect.center = self.game.play_rect.center

        # set the entity's bounds
        self._calculate_bounds()

        # set the entity's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # set the entity's speed
        self.base_speed_x = 0
        self.base_speed_y = 0
        self.calculate_relative_speed()

        # set default as not moving
        self.destination = None

    def _calculate_bounds(self,
                          pad_top: int = 0,
                          pad_bot: int = 0,
                          pad_left: int = 0,
                          pad_right: int = 0
                          ):
        """Calculate the bounds within which the entity can be."""

        bounds: BoundsDict = {
            'top': self.game.play_rect.top + pad_top,
            'bottom': self.game.play_rect.bottom - self.rect.height - pad_bot,
            'left': self.game.play_rect.left + pad_left,
            'right': self.game.play_rect.right - self.rect.width - pad_right
        }

        self.bounds = bounds
        
    def calculate_relative_speed(self):
        """
        Calculate entity's relative speed, regardless of aspect ratio.
        """

        x_mult = self.game.play_rect.width / 100
        y_mult = self.game.play_rect.height / 100

        self.speed_x = self.base_speed_x * x_mult
        self.speed_y = self.base_speed_y * y_mult

    def _calculate_relative_position(self, old_screen_rect: pygame.Rect):
        """
        Calculate the entity's relative position
        when the screen is resized.
        """

        rel_x = self.rect.x / old_screen_rect.width
        rel_y = self.rect.y / old_screen_rect.height
        
        if self.rect.x == 0:
            x = 0
        elif self.rect.right == old_screen_rect.right:
            x = self.game.play_rect.right
        else:
            x = self.game.play_rect.width * rel_x

        if self.rect.y == 0:
            y = 0
        elif self.rect.bottom == old_screen_rect.bottom:
            y = self.game.play_rect.bottom
        else:
            y = self.game.play_rect.height * rel_y
        
        self.x = float(x)
        self.y = float(y)
    
    def update(self):
        """Update the entity."""

        self._move()

    def _move(self):
        """Move the entity."""

        if self.destination == None:
            return False
        
        move_x = self.speed_x * self.game.dt
        move_y = self.speed_y * self.game.dt
        dx = self.destination[0] - self.x
        dy = self.destination[1] - self.y
        
        if dx < -move_x: # if destination is more than one step left
            move_x = -move_x
        elif -move_x <= dx <= move_x: # if destination is within one step
            move_x = dx
        if dy < -move_y:
            move_y = -move_y
        elif -move_y <= dy <= move_y:
            move_y = dy

        self.x += move_x
        self.y += move_y
        
        # return to screen if out of bounds
        if self.x < self.bounds["left"]:
            self.x = self.bounds["left"]
        elif self.x > self.bounds["right"]:
            self.x = self.bounds["right"]
        if self.y < self.bounds["top"]:
            self.y = self.bounds["top"]
        elif self.y > self.bounds["bottom"]:
            self.y = self.bounds["bottom"]
        
        # update the rectangle
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    
    def draw(self):
        """Draw the entity to the screen."""

        self.game.play_surf.blit(self.image, self.rect)
    
    def destroy(self):
        """
        Destroy the entity.
        Entities with sounds and animations should overwrite this.
        """

        self.kill() # remove from all sprite groups
    
    def handle_resize(self) -> None:
        """Handle what happens when the game window is resized."""

        old_rect = self.game.play_rect
        self.game.play_rect = self.game.play_surf.get_rect()

        self._calculate_bounds()

        self.calculate_relative_speed()
        self._calculate_relative_position(old_rect)

__all__ = ["Entity"]