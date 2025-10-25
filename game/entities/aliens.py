"""
A module containing all the aliens.
"""

import pygame

from .entity import Entity
from ..mechanics import abilities
from . import powerups

class Alien(Entity):
    """Base class that manages the aliens."""

    def __init__(self, game):
        """Initialize the alien."""

        super().__init__(game)

        # TODO: load alien as an image
        self.image = pygame.Surface((24, 24))
        # remove this draw after you start using images
        pygame.draw.rect(self.image, 'red', self.image.get_rect())
        self.rect = self.image.get_rect()

        # spawn enemy above the screen
        self.rect.midbottom = self.game.play_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self._calculate_bounds(pad_bot=-self.rect.height)

        # allow the alien to move downwards
        self.base_speed_y = self.game.config.base_speed * 0.25
        self._calculate_relative_speed()
        self.destination = (self.x, self.bounds["bottom"])

        # alien stats
        self.hp = 2
        self.speed = 1
        self.damage = 1
        self.credits = 10
    
    # override Entity update method
    def update(self):
        """Update the alien."""

        self._move()
        self._check_bottom()
    
    def _check_bottom(self):
        """
        Check if the alien is past the bottom of the screen.
        If so, destroy alien and reduce player ship hit points.
        """

        if self.y < self.bounds["bottom"]:
            return False
        
        self.game.ship.take_damage(self.damage)
        self.destroy()
        
        return True
    
    def take_damage(self, damage):
        """
        Reduce the alien's HP by the given amount.
        The alien is destroyed if HP is 0 or less. Returns True.
        Handle powerup drops.
        """

        self.hp -= damage
        if self.hp > 0:
            return False
        
        # TODO: add random chance to drop powerup, choose random powerup
        powerup = powerups.ImproveStat(self.game, self.rect.center, "Fire Power")
        powerup = powerups.AddAbility(self.game, self.rect.center, abilities.DeathPulse)
        self.game.powerups.add(powerup)
        self.game.state.credits_earned += self.credits
        self.game.top_tray.update()

        self.destroy()
        return True
    
    def destroy(self):
        """Destroy the alien. Handle sounds, animations, etc."""

        # TODO: play sounds and animations
        self.kill()

__all__ = ["Alien"]