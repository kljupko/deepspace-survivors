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
            image = Stat.get_image()
        
        self.image = image
    
    @staticmethod
    def get_image():
        """Get the image representing the stat."""

        return helper_funcs.load_image(None, 'gray', (10, 10))
    
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
            image = HitPoints.get_image()

        super().__init__(entity, value, image)

        self.name = "Hit Points"
    
    @staticmethod
    def get_image():
        """Get the image representing the stat."""

        return helper_funcs.load_image(None, 'pink', (10, 10))

class Thrust(Stat):
    """A class representing the player ship's speed."""

    def __init__(self, entity, value, image=None):
        """Initialize thrust."""

        if image is None:
            image = Thrust.get_image()

        super().__init__(entity, value, image)

        self.name = "Thrust"
    
    @staticmethod
    def get_image():
        """Get the image representing the stat."""

        return helper_funcs.load_image(None, 'yellow', (10, 10))

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
            image = FirePower.get_image()

        super().__init__(entity, value, image)

        self.name = "Fire Power"
    
    @staticmethod
    def get_image():
        """Get the image representing the stat."""

        return helper_funcs.load_image(None, 'red', (10, 10))

class FireRate(Stat):
    """A class representing the speed of the player ship's bullets."""

    def __init__(self, entity, value, image=None):
        """Initialize fire rate."""

        if image is None:
            image = FireRate.get_image()

        super().__init__(entity, value, image)

        self.name = "Fire Rate"
    
    @staticmethod
    def get_image():
        """Get the image representing the stat."""

        return helper_funcs.load_image(None, 'orange', (10, 10))

__all__ = ["HitPoints", "Thrust", "FirePower", "FireRate"]