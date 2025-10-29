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

        self.description = "Description for the upgrade."

        if image is None:
            image = helper_funcs.load_image(None, 'gray', (10, 10))
        
        self.image = image

    def get_cost(self):
        """Returns the number of credits needed to buy the upgrade."""

        return self.base_cost * 2**self.level

    def is_available(self):
        """
        Return True if the player has enough credits to upgrade.
        Return False if max level is reached.
        """

        available = self.game.progress.data['credits']
        if available < self.get_cost():
            return False
        
        if self.max_level is not None and self.level >= self.max_level:
            return False
        
        return True
    
    def do_upgrade(self):
        """Increase the level of the upgrade."""

        if not self.is_available():
            return False
        
        cost = self.get_cost()
        self.level += 1
        self.game.progress.data['upgrades'][self.name] = self.level
        self.game.progress.data['credits'] -= cost
        self.game.progress.save_data()
        # child classes will do additional things
        return True
    
class UpgradeHitPoints(Upgrade):
    """A class representing the ship's Hit Point upgrades."""

    def __init__(self, game, name="Hit Points",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.HitPoints.get_image()

        super().__init__(game, name, max_level, base_cost, image)

        self.description = "Permanently increase the ship's HP by 1."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_stats()
    
class UpgradeThrust(Upgrade):
    """A class representing the ship's Thrust upgrades."""

    def __init__(self, game, name="Thrust",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.Thrust.get_image()

        super().__init__(game, name, max_level, base_cost, image)

        self.description = "Permanently increase the ship's Thrust by 1."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_stats()
    
class UpgradeFirePower(Upgrade):
    """A class representing the ship's Fire Power upgrades."""

    def __init__(self, game, name="Fire Power",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.FirePower.get_image()

        super().__init__(game, name, max_level, base_cost, image)

        self.description = "Permanently increase the ship's Fire Power by 1."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_stats()
    
class UpgradeFireRate(Upgrade):
    """A class representing the ship's Fire Rate upgrades."""

    def __init__(self, game, name="Fire Rate",
                 max_level=None, base_cost=1200, image=None):
        """Initialize the upgrade."""

        if image is None:
            image = stats.FireRate.get_image()

        super().__init__(game, name, max_level, base_cost, image)

        self.description = "Permanently increase the ship's Fire Rate by 1."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_stats()

class UpgradeActiveSlots(Upgrade):
    """A class representing the ship's Active Ability Slot upgrades."""

    def __init__(self, game, name="Active Ability Slots",
                 max_level=2, base_cost=36000, image=None):
        """Initialize the upgrade."""

        # TODO: load image
        super().__init__(game, name, max_level, base_cost, image)
        self.description = "Unlock an additional Active Ability Slot."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_abilities()

class UpgradePassiveSlots(Upgrade):
    """A class representing the ship's Passive Ability Slot upgrades."""

    def __init__(self, game, name="Passive Ability Slots",
                 max_level=3, base_cost=24000, image=None):
        """Initialize the upgrade."""

        # TODO: load image
        super().__init__(game, name, max_level, base_cost, image)
        self.description = "Unlock an additional Passive Ability Slot."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_abilities()

class UpgradeChargeTime(Upgrade):
    """
    A class representing an upgrade which reduces the time needed
    for an Active Ability to fire.
    """

    def __init__(self, game, name="Ability Charge Time",
                 max_level=None, base_cost=120, image=None):
        
        # TODO: load image
        super().__init__(game, name, max_level, base_cost, image)
        self.description = "Reduce the time required to charge and " \
        "fire an Active Ability by 10% of its current value."
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_charge_time()

class UpgradeLuck(Upgrade):
    """
    A class representing an upgrade which increases the chance of
    aliens dropping powerups.
    """

    def __init__(self, game, name="Luck",
                 max_level=None, base_cost=480, image=None):
        
        # TODO: load image
        super().__init__(game, name, max_level, base_cost, image)
        self.description = "Increase the chance of aliens dropping powerups by 1%."

        # no need to augment the do_upgrade method

__all__ = [
    "UpgradeHitPoints", "UpgradeThrust", "UpgradeFirePower", "UpgradeFireRate",
    "UpgradeActiveSlots", "UpgradePassiveSlots", "UpgradeChargeTime",
    "UpgradeLuck"
]