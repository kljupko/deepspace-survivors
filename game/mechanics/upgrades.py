"""A module containing all the upgrades a ship can get."""

from ..utils import helper_funcs
from . import stats

class Upgrade():
    """A base class representing a ship's upgrade."""

    def __init__(self, game, name, max_level, base_cost, image=None):
        """Initialize the upgrade."""

        self.game = game
        self.name = name
        
        self.level = 0
        self.max_level = max_level
        self.base_cost = base_cost

        if image is None:
            image = helper_funcs.load_image(None, 'gray', (10, 10))

    def is_available(self):
        """
        Return True if the player has enough credits to upgrade.
        Return False if max level is reached.
        """

        cost = self.base_cost * 2**self.level
        if self.game.progress.data['credits'] < cost:
            return False
        
        if self.max_level is not None and self.level >= self.max_level:
            return False
        
        return True
    
    def do_upgrade(self):
        """Increase the level of the upgrade."""

        if not self.is_available():
            return False
        
        self.level += 1
        # child classes will do additional things
    
class HitPointUpgrade(Upgrade):
    """A class representing the ship's Hit Point upgrades."""

    def __init__(self, game, name="Hit Point Upgrade",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.HitPoints.get_image()

        super().__init__(game, name, max_level, base_cost)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        self.game.ship.load_stats()
    
class ThrustUpgrade(Upgrade):
    """A class representing the ship's Thrust upgrades."""

    def __init__(self, game, name="Thrust Upgrade",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.Thrust.get_image()

        super().__init__(game, name, max_level, base_cost)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        self.game.ship.load_stats()
    
class FirePowerUpgrade(Upgrade):
    """A class representing the ship's Fire Power upgrades."""

    def __init__(self, game, name="Fire Power Upgrade",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.FirePower.get_image()

        super().__init__(game, name, max_level, base_cost)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        self.game.ship.load_stats()
    
class FireRateUpgrade(Upgrade):
    """A class representing the ship's Fire Rate upgrades."""

    def __init__(self, game, name="Fire Rate Upgrade",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.FireRate.get_image()

        super().__init__(game, name, max_level, base_cost)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        self.game.ship.load_stats()

__all__ = [
    "HitPointUpgrade", "ThrustUpgrade", "FirePowerUpgrade", "FireRateUpgrade"
]