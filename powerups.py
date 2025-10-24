"""
A module containing the powerups dropped by destroyed aliens.
"""

import pygame
from entity import Entity

class PowerUp(Entity):
    """A base class representing a powerup."""

    def __init__(self, game, position):
        """Initialize the powerup."""

        super().__init__(game)

        self.name = "Base Powerup"
        self.description = "Powerup description."

        # TODO: load the powerup as an image
        self.rect = pygame.Rect(0, 0, 12, 12)
        self.color = "teal"

        self.rect.center = position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self._calculate_bounds(pad_bot=-self.rect.height)

        self.base_speed_y = self.game.config.base_speed * 0.15
        self._calculate_relative_speed()
        self.destination = (self.x, self.bounds["bottom"])

    # override Entity update method
    def update(self):
        """Update the powerup."""

        self._move()
        self._check_bottom()
    
    def _check_bottom(self):
        """
        Check if the powerup is past the bottom of the screen.
        If so, destroy it.
        """

        if self.y < self.bounds["bottom"]:
            return False
        
        self.destroy()
        return True
    
    def apply(self):
        """Apply the powerup on pickup."""

        print(f"Hook for picking up the {self.name} powerup.")
        print(self.description)
        self.destroy()
    
class BonusHP(PowerUp):
    """A class representing a powerup that increases the ship's HP."""

    def __init__(self, game, position):
        """Initialize the powerup."""

        super().__init__(game, position)

        self.name = "BonusHP"
        self.hp_bonus = 1
        self.description = f"Increases the player ship's HP by {self.hp_bonus}."

    def apply(self):
        """Apply the powerup on pickup."""

        self.game.ship.hp += self.hp_bonus
        self.game.powerups.remove(self)
        return True

class AddAbility(PowerUp):
    """A class representing a powerup that grants the ship an ability."""

    def __init__(self, game, position, ability, isActive=False):
        """Initialize the powerup."""

        super().__init__(game, position)

        self.ability = ability
        self.isActive = isActive
        self.name = f"Add {self.ability.name}"
        self.description = f"Gives the player the {self.ability.name}" \
        " ability."
    
    def apply(self):
        """Apply the powerup on pickup."""

        if self.isActive:
            self.game.ship.add_active_ability(self.ability)
        else:
            self.game.ship.add_passive_ability(self.ability)
        
        self.game.powerups.remove(self)
        return True