"""
A module containing the classes for the active and passive abilities.
"""

from ..systems import helper_funcs

class Ability():
    """A grandparent class representing a ship's ability."""

    def __init__(self, game):
        """Initialize the ability."""

        self.game = game
        self.name = "Base Ability"
        self.description = "Ability description."
        self.enabled = False
    
    def toggle(self):
        """
        Hook for toggling the ability. Always sets to false.
        Overridden by child classes.
        """

        self.enabled = False
    
    def fire(self):
        """
        Hook for firing the ability. Does nothing.
        Overridden by grandchild classes.
        """

        return False
    
class Active(Ability):
    """A base class that represents a ship's active ability."""

    def __init__(self, game):
        """Initialize the ability."""

        super().__init__(game)

        self.name = "Base Active Ability"
        self.description = "Active ability description."
        self.is_active = True
    
    def toggle(self):
        """Toggle the ability On/Off."""

        self.enabled = not self.enabled
    
    def _remove(self):
        """Remove the active ability from the ship."""

        self_idx = self.game.ship.active_abilities.index(self)
        self.game.ship.active_abilities[self_idx] = Blank(self.game)

class Passive(Ability):
    """A class that represents a ship's passive ability."""

    def __init__(self, game):
        """Initialize the passive ability."""

        super().__init__(game)

        self.name = "Base Passive Ability"
        self.description = "Passive ability description."
        self.is_active = False
        self.level = 1
        self.enabled = True

    # override the Ability method
    def toggle(self):
        """Toggle the ability On/Off."""

        self.enabled = not self.enabled
    
    def _remove(self):
        """Remove the passive ability from the ship."""

        self_idx = self.game.ship.passive_abilities.index(self)
        self.game.ship.passive_abilities[self_idx] = Blank(self.game)
    
    def level_up(self):
        """Increase the level of the passive ability."""

        self.level += 1

class Blank(Ability):
    """A class that represents a blank ability. Does nothing."""

    def __init__(self, game):
        """Initialize the blank ability."""

        super().__init__(game)

        self.name = "Blank Ability"
        self.description = "Collect a powerup to add an ability to this slot."

        self.icon = helper_funcs.load_image(
            dflt_color="gray", dflt_size=(10, 10)
        )
        
class Locked(Ability):
    """A class that represents a locked ability. Does nothing."""

    def __init__(self, game):
        """Initialize the locked ability."""

        super().__init__(game)

        self.name = "Locked Ability"
        self.description = "Unlock this ability slot in the progress menu."

        self.icon = helper_funcs.load_image(
            dflt_color="black", dflt_size=(10, 10)
        )

# region ACTIVE ABILITIES
# -----------------------------------------------------------------------

class DeathPulse(Active):
    """
    A class that represents the Death Pulse active ability, which deals
    a large amount of damage to all enemies on the screen.
    """

    def __init__(self, game):
        """Initialize the Death Pulse ability."""

        super().__init__(game)

        self.name = "Death Pulse"
        self.fp_bonus = 50
        self.description = f"Deals {self.fp_bonus}x Fire Power to all enemies" \
        " on the screen."

        self.icon = helper_funcs.load_image(
            dflt_color="red", dflt_size=(10, 10)
        )
    
    def fire(self):
        """Fire the Death Pulse ability."""

        for alien in self.game.aliens:
            alien.take_damage(self.game.ship.fire_power * self.fp_bonus)
        
        self._remove()

# -----------------------------------------------------------------------
# endregion

# region PASSIVE ABILITIES
# -----------------------------------------------------------------------

class Spear(Passive):
    """
    A class that represents the Spear passive ability, which increases
    the ship's fire rate and allows it to continuously fire.
    """

    def __init__(self, game):
        """Initialize the Spear ability."""

        super().__init__(game)

        self.name = "Spear"
        self.fr_bonus = 1
        self.description = "Fires a continuous stream of bullets." \
        f" Each level increases fire rate by {self.fr_bonus}."

        self.icon = helper_funcs.load_image(
            dflt_color="purple", dflt_size=(10, 10)
        )
    
    def fire(self):
        """Fire the Spear ability."""

        self.game.ship.fire_bullet(self.fr_bonus * self.level)
    
    def level_up(self):
        """Increase the fire rate bonus (autocalculated by level)."""
        return super().level_up()

# -----------------------------------------------------------------------
# endregion

__all__ = ["Blank","Locked", "DeathPulse", "Spear"]