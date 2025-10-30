"""
A module containing the RandomDropManager class, which manages
the random drops of powerups.
"""

from random import randint, choices

from ..entities import powerups
from ..mechanics import abilities, stats, upgrades

class RandomDropManager():
    """A class which manages random powerup drops."""

    def __init__(self, game):
        """Initialize the random drop."""

        self.game = game

        # TODO: load weights from saved upgrades
        # all choice weights are non-cumulative
        self.powerup_choices = {
            powerups.AddAbility: 1,
            powerups.ImproveStat: 1
        }

        self.ability_choices = {
            abilities.DeathPulse: 1,
            abilities.Spear: 3
        }

        self.stat_choices = {
            stats.HitPoints: 3,
            stats.Thrust: 1,
            stats.FirePower: 3,
            stats.FireRate: 2
        }

    def try_drop(self, chance, position):
        """
        Rolls for a drop and if successful, returns a random one
        at the given position.
        """

        if not self._is_dropping(chance):
            return None
        
        powerup = choices(
            list(self.powerup_choices.keys()),
            list(self.powerup_choices.values())
        )[0]
        
        if powerup == powerups.AddAbility:
            return self._drop_ability(position)
        else:
            return self._drop_stat(position)
    
    def _is_dropping(self, chance):
        """Roll for a random drop."""

        chance += self.game.upgrades[upgrades.Luck.name].level
        maximum = 100
        while chance % 1 != 0:
            chance *= 10
            maximum *= 10
        
        if randint(1, maximum) > chance:
            return False
        return True
    
    def _drop_ability(self, position):
        """Drops an AddAbility powerup."""
        
        ability_class = choices(
            list(self.ability_choices.keys()),
            list(self.ability_choices.values())
        )[0]
        
        return powerups.AddAbility(self.game, position, ability_class)
    
    def _drop_stat(self, position):
        """Drops an ImproveStat powerup."""
        
        stat_class = choices(
            list(self.stat_choices.keys()),
            list(self.stat_choices.values())
        )[0]
        
        return powerups.ImproveStat(self.game, position, stat_class)

__all__ = ["RandomDropManager"]