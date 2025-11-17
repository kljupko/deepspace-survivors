"""A module containing the Bullet class."""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game

import pygame

from .entity import Entity
from .aliens import Alien
from ..utils import config, helper_funcs

class Bullet(Entity):
    """A class that represents a bullet fired from the ship."""

    name: str = "Base Bullet"
    image: pygame.Surface = helper_funcs.load_image(None, 'orange', (4, 4))

    def __init__(self, game: Game) -> None:
        """Initialize the bullet."""

        image: pygame.Surface = helper_funcs.copy_image(Bullet.image)
        super().__init__(game, image)

        # spawn bullet on top of the ship
        self._calculate_bounds(pad_top=-self.rect.height)
        self.rect.midbottom = self.game.ship.rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the bullet to move upwards
        self.base_speed_y: float = config.base_speed * 0.5
        self.calculate_relative_speed()
        self.destination = (self.x, float(self.bounds["top"]))

        self.damage: int = self.game.ship.stats["fire_power"].value

    # override Entity update method
    def update(self) -> None:
        """Update the bullet."""

        self._move()
        self._check_alien_collisions()
        self._check_top()
    
    def _check_alien_collisions(self) -> bool:
        """
        Check if the bullet is colliding with any aliens.
        If so, deal damage to the alien and remove the bullet.
        """

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        alien = collisions[0]
        # ensure the alien is indeed a subclass of Alien
        if not isinstance(alien, Alien):
            return False
        
        alien.take_damage(self.damage)
        
        self.destroy()
        return True
    
    def _check_top(self) -> bool:
        """
        Check if the bullet has moved past the top of the screen.
        If so, remove it.
        """

        if self.y > self.bounds["top"]:
            return False
        
        self.destroy()
        return True

__all__ = ["Bullet"]
