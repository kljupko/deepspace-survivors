"""A module containing the Bullet class."""

import pygame
from .entity import Entity

class Bullet(Entity):
    """A class that represents a bullet fired from the ship."""

    def __init__(self, game):
        """Initialize the bullet."""

        super().__init__(game)

        # TODO: load the bullet as an image
        self.color = "orange"
        self.rect = pygame.Rect(0, 0, 4, 4)

        # spawn bullet on top of the ship
        self._calculate_bounds(pad_top=-self.rect.height)
        self.rect.midtop = self.game.ship.rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the bullet to move upwards
        self.base_speed_y = self.game.config.base_speed * 0.5
        self._calculate_relative_speed()
        self.destination = (self.x, self.bounds["top"])

        # TODO: determine if bullet will have any stats

    # override Entity update method
    def update(self):
        """Update the bullet."""

        self._move()
        self._check_alien_collisions()
        self._check_top()
    
    def _check_alien_collisions(self):
        """Check if the bullet is colliding with any aliens."""

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        alien = collisions[0]
        alien.take_damage(self.game.ship.fire_power)
        
        self.destroy()
        return True
    
    def _check_top(self):
        """Check if the bullet has moved past the top of the screen."""

        if self.y > self.bounds["top"]:
            return False
        
        self.destroy()
        return True

__all__ = ["Bullet"]