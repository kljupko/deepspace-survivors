"""
A module containing the powerups dropped by destroyed aliens.
"""

import pygame
from .entity import Entity

class PowerUp(Entity):
    """A base class representing a powerup."""

    def __init__(self, game, position):
        """Initialize the powerup."""

        super().__init__(game)

        self.name = "Base Powerup"
        self.description = "Powerup description."

        # TODO: load the powerup as an image
        self.image = pygame.Surface((12, 12))
        # remove this draw after you start using images
        pygame.draw.rect(self.image, 'teal', self.image.get_rect())
        self.rect = self.image.get_rect()

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
    
class ImproveStat(PowerUp):
    """
    A class representing a powerup that improves one of the ship's stats.
    """

    def __init__(self, game, position, stat_name, magnitude=1):
        """Initialize the powerup."""

        super().__init__(game, position)

        # TODO: load the image based on the stat
        self.image = pygame.Surface((12, 12))
        # remove this draw after you start using images
        pygame.draw.rect(self.image, 'deeppink', self.image.get_rect())

        self.stat_name = stat_name
        self.magnitude = magnitude
        self.name = f"Increase {self.stat_name}"
        self.description = f"Increases a player ship's {stat_name.lower()} "
        self.description += f"by {self.magnitude}."

    def apply(self):
        """Apply the powerup on pickup."""

        # loop through the options by name to figure out which one it is?
        name = self.stat_name.lower()
        success = False

        # check bottom tray stats
        if name == 'hp':
            self.game.ship.hp += self.magnitude
            success = True
        elif name == 'thrust':
            self.game.ship.thrust += self.magnitude
            success = True

        if success:
            self.game.bot_tray.update()
            self.game.powerups.remove(self)
            return True
        
        # check top tray stats
        if name == 'fire power':
            self.game.ship.fire_power += self.magnitude
            success = True
        if name == 'fire rate':
            self.game.ship.fire_rate += self.magnitude
            success = True

        if success:
            self.game.top_tray.update()
            self.game.powerups.remove(self)
            return True

        return False

class AddAbility(PowerUp):
    """A class representing a powerup that grants the ship an ability."""

    def __init__(self, game, position, ability_class):
        """Initialize the powerup."""

        super().__init__(game, position)

        # override the default image
        self.image = pygame.Surface((12, 12))
        # remove this draw after you start using images
        pygame.draw.rect(self.image, 'peru', self.image.get_rect())

        self.ability = ability_class(self.game)
        self.name = f"Add {self.ability.name}"
        self.description = f"Gives the player the "
        self.description += f"{self.ability.name} ability."
    
    def apply(self):
        """Apply the powerup on pickup."""

        if self.ability.is_active:
            self.game.ship.add_active_ability(self.ability)
        else:
            self.game.ship.add_passive_ability(self.ability)
        
        self.game.powerups.remove(self)
        return True

__all__ = ["ImproveStat", "AddAbility"]