"""
A module containing the powerups dropped by destroyed aliens.
"""

from .entity import Entity
from ..utils import config, helper_funcs

class PowerUp(Entity):
    """A base class representing a powerup."""

    name = "Base Powerup"
    image = helper_funcs.load_image(None, "teal", (12, 12))

    def __init__(self, game, position, image=None):
        """Initialize the powerup."""

        if image is None:
            image = helper_funcs.copy_image(PowerUp.image)
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

        self.destroy()
    
class ImproveStat(PowerUp):
    """
    A class representing a powerup that improves one of the ship's stats.
    """

    name = "Improve Stat"
    image = helper_funcs.load_image(None, "cadetblue1", (12, 12))

    def __init__(self, game, position, stat_class, magnitude=1):
        """Initialize the powerup."""

        image = helper_funcs.copy_image(ImproveStat.image)
        super().__init__(game, position, image)

        self.stat_name = stat_class.name
        self.magnitude = magnitude
        self.name = f"Increase {self.stat_name}"
        self.description = f"Increases a player ship's {self.stat_name} " \
            f"by {self.magnitude}."

        self.image.blit(stat_class.image, (1, 1))

    def apply(self):
        """Apply the powerup on pickup."""

        for stat in self.game.ship.stats.values():
            if stat.name == self.stat_name:
                stat.modify_stat(self.magnitude)
                return super().apply()

class AddAbility(PowerUp):
    """A class representing a powerup that grants the ship an ability."""

    name = "Add Ability"
    image = helper_funcs.load_image(None, "peru", (12, 12))

    def __init__(self, game, position, ability_class):
        """Initialize the powerup."""

        image = helper_funcs.copy_image(AddAbility.image)
        super().__init__(game, position, image)

        self.ability = ability_class(self.game)
        self.name = f"Add {self.ability.name}"
        self.description = f"Gives the player the "
        self.description += f"{self.ability.name} ability."

        self.image.blit(self.ability.image, (1, 1))
    
    def apply(self):
        """Apply the powerup on pickup."""

        if self.ability.is_active:
            self.game.ship.add_active_ability(self.ability)
        else:
            self.game.ship.add_passive_ability(self.ability)
        
        self.game.powerups.remove(self)
        return True

__all__ = ["ImproveStat", "AddAbility"]