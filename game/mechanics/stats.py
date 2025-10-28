"""A module containing the Stat class for the ship's HP, Thrust, etc."""

from ..utils import config, helper_funcs

class Stat():
    """A base class representing one of the ship's stats."""

    def __init__(self, entity, value, image=None):
        """Initialize the stat."""

        self.entity = entity

        self.name = "Base Stat"
        self.set_value(value)

        if image is None:
            image = helper_funcs.load_image(None, 'gray', (10, 10))
        
        self.image = image
    
    def set_value(self, value):
        """Sets the value for the stat."""

        self.value = value
    
    def modify_stat(self, diff):
        """
        Increases or decreases the stat's value by the given amount.
        Uses the set_value method.
        """

        new_value = self.value + diff
        self.set_value(new_value)
        self.entity.game.top_tray.update()
        self.entity.game.bot_tray.update()

class HitPoints(Stat):
    """A class representing an entity's health."""

    def __init__(self, entity, value, image=None):
        """Initialize hit points."""

        if image is None:
            image = helper_funcs.load_image(None, 'pink', (10, 10))

        super().__init__(entity, value, image)

        self.name = "Hit Points"

class Thrust(Stat):
    """A class representing the player ship's speed."""

    def __init__(self, entity, value, image=None):
        """Initialize thrust."""

        if image is None:
            image = helper_funcs.load_image(None, 'yellow', (10, 10))

        super().__init__(entity, value, image)

        self.name = "Thrust"

    def set_value(self, value):
        """Sets the ship's thrust and recalculates speed."""

        super().set_value(value)

        self.entity.base_speed_x = config.base_speed * self.value / 3
        self.entity._calculate_relative_speed()

class FirePower(Stat):
    """
    A class representing the damage done by the player ship's bullets.
    """

    def __init__(self, entity, value, image=None):
        """Initialize fire power."""

        if image is None:
            image = helper_funcs.load_image(None, 'red', (10, 10))

        super().__init__(entity, value, image)

        self.name = "Fire Power"

class FireRate(Stat):
    """A class representing the speed of the player ship's bullets."""

    def __init__(self, entity, value, image=None):
        """Initialize fire rate."""

        if image is None:
            image = helper_funcs.load_image(None, 'orange', (10, 10))

        super().__init__(entity, value, image)

        self.name = "Fire Rate"

__all__ = ["HitPoints", "Thrust", "FirePower", "FireRate"]