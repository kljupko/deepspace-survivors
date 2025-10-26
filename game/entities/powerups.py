"""
A module containing the powerups dropped by destroyed aliens.
"""

import pygame
from .entity import Entity
from ..systems import config, helper_funcs

class PowerUp(Entity):
    """A base class representing a powerup."""

    def __init__(self, game, position, image=None):
        """Initialize the powerup."""

        if image is None:
            image = helper_funcs.load_image(dflt_color="teal", dflt_size=(12, 12))
        super().__init__(game, image)

        self.name = "Base Powerup"
        self.description = "Powerup description."

        self.rect.center = position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self._calculate_bounds(pad_bot=-self.rect.height)

        self.base_speed_y = config.base_speed * 0.15
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

        image = helper_funcs.load_image(dflt_color="cadetblue1", dflt_size=(12, 12))
        super().__init__(game, position, image)

        self.stat_name = stat_name
        self.magnitude = magnitude
        self.name = f"Increase {self.stat_name}"
        self.description = f"Increases a player ship's {stat_name.lower()} "
        self.description += f"by {self.magnitude}."

        if self.stat_name.lower() == 'hp':
            icon = helper_funcs.load_image(dflt_color='deeppink', dflt_size=(10, 10))
        elif self.stat_name.lower() == 'thrust':
            icon = helper_funcs.load_image(dflt_color='yellow', dflt_size=(10, 10))
        elif self.stat_name.lower() == 'fire power':
            icon = helper_funcs.load_image(dflt_color='red', dflt_size=(10, 10))
        elif self.stat_name.lower() == 'fire rate':
            icon = helper_funcs.load_image(dflt_color='orange', dflt_size=(10, 10))
        self.image.blit(icon, (1, 1))

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

        image = helper_funcs.load_image(dflt_color="peru", dflt_size=(12, 12))
        super().__init__(game, position, image)

        self.ability = ability_class(self.game)
        self.name = f"Add {self.ability.name}"
        self.description = f"Gives the player the "
        self.description += f"{self.ability.name} ability."

        self.image.blit(self.ability.icon, (1, 1))
    
    def apply(self):
        """Apply the powerup on pickup."""

        if self.ability.is_active:
            self.game.ship.add_active_ability(self.ability)
        else:
            self.game.ship.add_passive_ability(self.ability)
        
        self.game.powerups.remove(self)
        return True

__all__ = ["ImproveStat", "AddAbility"]