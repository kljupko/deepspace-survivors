"""A module containing all the upgrades a ship can get."""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game
    import pygame

from ..utils import helper_funcs
from . import abilities, stats

class Upgrade():
    """A base class representing a ship's upgrade."""

    name = "Base Upgrade"
    description = "An abstract base upgrade."
    max_level = None
    base_cost = 0
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 description: str | None = None,
                 max_level: int | None = None,
                 base_cost: int | None = None,
                 image: pygame.Surface | None = None
                 ):
        """Initialize the upgrade."""

        self.game = game

        if name is None:
            name = Upgrade.name
        self.name = name

        if description is None:
            description = Upgrade.description
        self.description = description
        
        self.level = 0
        if max_level is None:
            self.max_level = Upgrade.max_level
        self.max_level = max_level

        if base_cost is None:
            base_cost = Upgrade.base_cost
        self.base_cost = base_cost

        if image is None:
            image = Upgrade.image
        self.image = image

    def get_cost(self) -> int:
        """Returns the number of credits needed to buy the upgrade."""

        return self.base_cost * 2**self.level

    def is_available(self) -> bool:
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
    
    def do_upgrade(self) -> bool:
        """Increase the level of the upgrade."""

        if not self.is_available():
            return False
        
        cost = self.get_cost()
        self.level += 1
        self.game.progress.data['upgrades'][self.name]['level'] = self.level
        self.game.progress.data['credits'] -= cost
        self.game.progress.save_data()
        # child classes will do additional things
        return True

class StatUpgrade(Upgrade):
    """A base class representing an upgrade to one of the ship's stats."""

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 description: str | None = None,
                 max_level: int | None = None,
                 base_cost: int | None = None,
                 image: pygame.Surface | None = None
                 ):
        """Initialize the upgrade."""

        super().__init__(game, name, description, max_level, base_cost, image)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        success = super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_stat_upgrades()

        return success

class HitPoints(StatUpgrade):
    """A class representing the ship's Hit Point upgrades."""

    name = "Hit Points Upgrade"
    description = "Permanently increase the ship's HP by 1."
    max_level = None
    base_cost = 1200
    image = stats.HitPoints.image

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = HitPoints.name
        description = HitPoints.description
        max_level = HitPoints.max_level
        base_cost = HitPoints.base_cost
        image = HitPoints.image
        super().__init__(game, name, description, max_level, base_cost, image)
    
class Thrust(StatUpgrade):
    """A class representing the ship's Thrust upgrades."""

    name = "Thrust Upgrade"
    description = "Permanently increase the ship's Thrust by 1."
    max_level = None
    base_cost = 1200
    image = stats.Thrust.image

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = Thrust.name
        description = Thrust.description
        max_level = Thrust.max_level
        base_cost = Thrust.base_cost
        image = Thrust.image
        super().__init__(game, name, description, max_level, base_cost, image)
    
class FirePower(StatUpgrade):
    """A class representing the ship's Fire Power upgrades."""

    name = "Fire Power Upgrade"
    description = "Permanently increase the ship's Fire Power by 1."
    max_level = None
    base_cost = 1200
    image = stats.FirePower.image

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = FirePower.name
        description = FirePower.description
        max_level = FirePower.max_level
        base_cost = FirePower.base_cost
        image = FirePower.image
        super().__init__(game, name, description, max_level, base_cost, image)
    
class FireRate(StatUpgrade):
    """A class representing the ship's Fire Rate upgrades."""

    name = "Fire Rate Upgrade"
    description = "Permanently increase the ship's Fire Rate by 1."
    max_level = None
    base_cost = 1200
    image = stats.FireRate.image

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = FireRate.name
        description = FireRate.description
        max_level = FireRate.max_level
        base_cost = FireRate.base_cost
        image = FireRate.image
        super().__init__(game, name, description, max_level, base_cost, image)

class ActiveSlots(Upgrade):
    """A class representing the ship's Active Ability Slot upgrades."""

    name = "Active Ability Slot Upgrade"
    description = "Unlock an additional Active Ability slot."
    max_level = 2
    base_cost = 36000
    image = abilities.Active.image

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = ActiveSlots.name
        description = ActiveSlots.description
        max_level = ActiveSlots.max_level
        base_cost = ActiveSlots.base_cost
        image = ActiveSlots.image
        super().__init__(game, name, description, max_level, base_cost, image)

    def do_upgrade(self):
        """Upgrade and apply to ship."""

        success = super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_abilities()

        return success

class PassiveSlots(Upgrade):
    """A class representing the ship's Passive Ability Slot upgrades."""

    name = "Passive Ability Slot Upgrade"
    description = "Unlock an additional Passive Ability slot."
    max_level = 3
    base_cost = 24000
    image = abilities.Passive.image

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = PassiveSlots.name
        description = PassiveSlots.description
        max_level = PassiveSlots.max_level
        base_cost = PassiveSlots.base_cost
        image =PassiveSlots.image
        super().__init__(game, name, description, max_level, base_cost, image)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        success = super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_abilities()
        
        return success

class ChargeTime(Upgrade):
    """
    A class representing an upgrade which reduces the time needed
    for an Active Ability to fire.
    """

    name = "Active Ability Charge Time Upgrade"
    description = "Reduce the time required to charge and " \
        "fire an Active Ability by 10% of its current value."
    max_level = None
    base_cost = 120
    image = helper_funcs.load_image(None, 'salmon', (10, 10))

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = ChargeTime.name
        description = ChargeTime.description
        max_level = ChargeTime.max_level
        base_cost = ChargeTime.base_cost
        image =ChargeTime.image
        super().__init__(game, name, description, max_level, base_cost, image)
    
    def do_upgrade(self):
        """Upgrade and apply to ship."""

        success = super().do_upgrade()
        if self.game.ship:
            self.game.ship.load_req_charge_time()
        
        return success

class Luck(Upgrade):
    """
    A class representing an upgrade which increases the chance of
    aliens dropping powerups.
    """

    name = "Luck Upgrade"
    description = "Increase the chance of aliens dropping powerups by 1%."
    max_level = None
    base_cost = 480
    image = helper_funcs.load_image(None, 'chartreuse3', (10, 10))

    def __init__(self, game: Game):
        """Initialize the upgrade."""

        name = Luck.name
        description = Luck.description
        max_level = Luck.max_level
        base_cost = Luck.base_cost
        image =Luck.image
        super().__init__(game, name, description, max_level, base_cost, image)

    # no need to augment the do_upgrade method

__all__ = [
    "HitPoints", "Thrust", "FirePower", "FireRate",
    "ActiveSlots", "PassiveSlots", "ChargeTime",
    "Luck"
]