"""
A module containing all the playable ships.
"""

import pygame
from entity import Entity

class Ship(Entity):
    """Base class that manages the player ship."""

    def __init__(self, game):
        """Initialize the ship."""
        
        super().__init__(game)

        # TODO: load ship as an image
        self.color = "green"

        # overwrite Entity's center position
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the ship to move horizontally
        self.base_speed_x = 100
        self.speed_x, self.speed_y = self._calculate_relative_speed()

        # ship stats
        self.hp = 3
        self.thrust = 1
        self.fire_rate = 1
        self.fire_power = 1
        self.active_abilities = [None, False, False]
        self.passive_abilities = [None, False, False, False]
    
    # override Entity update method
    def update(self, dt):
        """Update the ship."""

        self._move(dt)
        self._check_alien_collisions()
    
    def _check_alien_collisions(self):
        """Check if the ship is colliding with any aliens."""

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        print(f"We're hit! {len(collisions)} aliens hit the ship.")
        for alien in collisions:
            self.hp -= alien.damage
            print(f"\tCurrent hp: {self.hp} (-{alien.damage})")
            alien.destroy()
        
        return False