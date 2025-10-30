"""A module containing the Stat class for the ship's HP, Thrust, etc."""

from ..utils import config, helper_funcs

class Stat():
    """A base class representing one of the ship's stats."""

    name = "Base Stat"
    description = "An abstract base stat."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self, entity, value, name=None, description=None, image=None):
        """Initialize the stat."""

        self.entity = entity
        self.set_value(value)

        if name is None:
            name = Stat.name
        self.name = name

        if description is None:
            description = Stat.description
        self.description = description

        if image is None:
            image = Stat.image
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

    name = "Hit Points"
    description = "Represents how much damage the ship can take before being destroyed."
    image = helper_funcs.load_image(None, 'pink', (10, 10))

    def __init__(self, entity, value):
        """Initialize hit points."""

        name = HitPoints.name
        description = HitPoints.description
        image = HitPoints.image
        super().__init__(entity, value, name, description, image)

class Thrust(Stat):
    """A class representing the player ship's speed."""

    name = "Thrust"
    description = "Represents how quickly the ship can move."
    image = helper_funcs.load_image(None, 'yellow', (10, 10))

    def __init__(self, entity, value):
        """Initialize thrust."""

        name = Thrust.name
        description = Thrust.description
        image = Thrust.image
        super().__init__(entity, value, name, description, image)

    def set_value(self, value):
        """Sets the ship's thrust and recalculates speed."""

        super().set_value(value)

        self.entity.base_speed_x = config.base_speed * self.value / 3
        self.entity._calculate_relative_speed()

class FirePower(Stat):
    """
    A class representing the damage done by the player ship's bullets.
    """

    name = "Fire Power"
    description = "Represents the damage dealt by the ship's bullets."
    image = helper_funcs.load_image(None, 'red', (10, 10))

    def __init__(self, entity, value, image=None):
        """Initialize fire power."""

        name = FirePower.name
        description = FirePower.description
        image = FirePower.image
        super().__init__(entity, value, name, description, image)

class FireRate(Stat):
    """A class representing the speed of the player ship's bullets."""

    name = "Fire Rate"
    description = "Represents how quickly the ship can fire bullets."
    image = helper_funcs.load_image(None, 'orange', (10, 10))

    def __init__(self, entity, value, image=None):
        """Initialize fire rate."""

        name = FireRate.name
        description = FireRate.description
        image = FireRate.image
        super().__init__(entity, value, name, description, image)

__all__ = ["HitPoints", "Thrust", "FirePower", "FireRate"]