"""
A module containing all the aliens.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game

import pygame

from .entity import Entity
from ..utils import config, helper_funcs

class Alien(Entity):
    """Base class that manages the aliens."""

    name: str = "Base Alien"
    image: pygame.Surface = helper_funcs.load_image(dflt_color="red")

    def __init__(self, game: Game) -> None:
        """Initialize the alien."""

        image: pygame.Surface = helper_funcs.copy_image(Alien.image)
        super().__init__(game, image)

        # spawn enemy above the screen
        self.rect.midbottom = self.game.play_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self._calculate_bounds(pad_bot=-self.rect.height)

        # allow the alien to move downwards
        self.base_speed_y: float = config.base_speed * 0.25
        self.calculate_relative_speed()
        self.destination = (self.x, self.bounds["bottom"])

        # alien stats
        self.hp: int = 2
        self.speed: int = 1
        self.damage: int = 1
        self.credits: int = 10
        self.drop_chance: int = 1 # percent
    
    # override Entity update method
    def update(self) -> None:
        """Update the alien."""

        self._move()
        self._check_bottom()
    
    def _check_bottom(self) -> bool:
        """
        Check if the alien is past the bottom of the screen.
        If so, destroy alien and reduce player ship hit points.
        """

        if self.y < self.bounds["bottom"]:
            return False
        
        self.game.ship.take_damage(self.damage)
        self.destroy()
        
        return True
    
    def take_damage(self, damage: int) -> bool:
        """
        Reduce the alien's HP by the given amount. Return True if the
        alien is destroyed by the player, and try dropping a powerup.
        """

        self.hp -= damage
        if self.hp > 0:
            return False
        
        # try dropping a random powerup
        powerup = self.game.drop_manager.try_drop(
            self.drop_chance, self.rect.center
        )
        if powerup:
            self.game.powerups.add(powerup)
        
        self.game.state.killcount += 1
        self.game.state.credits_earned += self.credits
        self.game.top_tray.update()

        self.destroy()
        return True

    def destroy(self) -> None:
        """Destroy the alien. Handle sounds, animations, etc."""

        # TODO: play sounds and animations
        return super().destroy()    

__all__ = ["Alien"]
