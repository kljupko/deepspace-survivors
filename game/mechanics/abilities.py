"""
A module containing the classes for the active and passive abilities.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game

import pygame

from ..utils import helper_funcs

class Ability():
    """A grandparent class representing a ship's ability."""

    name: str = "Base Ability"
    description: str = "Base Ability description."
    image: pygame.Surface = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self, game: Game):
        """Initialize the ability."""

        self.game = game
        self.name = Ability.name
        self.description = Ability.description
        self.image = helper_funcs.copy_image(Ability.image)
        self.is_enabled = False
    
    def toggle(self):
        """
        Hook for toggling the ability. Always sets to false.
        Overridden by child classes.
        """

        self.is_enabled = False
    
    def fire(self):
        """
        Hook for firing the ability. Does nothing.
        Overridden by grandchild classes.
        """

        return None
    
class Active(Ability):
    """A base class that represents a ship's active ability."""

    name = "Base Active Ability"
    description = "Base Active Ability description."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self, game: Game):
        """Initialize the ability."""

        super().__init__(game)

        self.name = Active.name
        self.description = Active.description
        self.image = helper_funcs.copy_image(Active.image)
        self.is_active = True
    
    def toggle(self):
        """Toggle the ability On/Off."""

        self.is_enabled = not self.is_enabled
        print(f"Ability: {self.name} set to {self.is_enabled}")
    
    def _remove(self):
        """Remove the active ability from the ship."""

        self_idx = self.game.ship.active_abilities.index(self)
        self.game.ship.active_abilities[self_idx] = Blank(self.game)

class Passive(Ability):
    """A class that represents a ship's passive ability."""

    name = "Base Passive Ability"
    description = "Base Passive Ability description."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self, game: Game):
        """Initialize the passive ability."""

        super().__init__(game)

        self.name = Passive.name
        self.description = Passive.description
        self.image = helper_funcs.copy_image(Passive.image)
        self.is_active = False
        self.level = 1
        self.is_enabled = True

    # override the Ability method
    def toggle(self):
        """Toggle the ability On/Off."""

        self.is_enabled = not self.is_enabled
    
    def _remove(self):
        """Remove the passive ability from the ship."""

        self_idx = self.game.ship.passive_abilities.index(self)
        self.game.ship.passive_abilities[self_idx] = Blank(self.game)
    
    def level_up(self):
        """Increase the level of the passive ability."""

        self.level += 1

class Blank(Ability):
    """A class that represents a blank ability. Does nothing."""

    name = "Blank Ability Slot"
    description = "Collect a powerup to add an ability to this slot."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self, game: Game):
        """Initialize the blank ability."""

        super().__init__(game)

        self.name = Blank.name
        self.description = Blank.description
        self.image = helper_funcs.copy_image(Blank.image)
        
class Locked(Ability):
    """A class that represents a locked ability. Does nothing."""

    name = "Locked Ability Slot"
    description = "Unlock this ability slot in the progress menu."
    image = helper_funcs.load_image(None, 'black', (10, 10))

    def __init__(self, game: Game):
        """Initialize the locked ability."""

        super().__init__(game)

        self.name = Locked.name
        self.description = Locked.description
        self.image = helper_funcs.copy_image(Locked.image)

# region ACTIVE ABILITIES
# -----------------------------------------------------------------------

class DeathPulse(Active):
    """
    A class that represents the Death Pulse active ability, which deals
    a large amount of damage to all enemies on the screen.
    """

    name = "Death Pulse"
    description = "Deals damage to all enemies on screen."
    image = helper_funcs.load_image(None, 'red', (10, 10))

    def __init__(self, game: Game):
        """Initialize the Death Pulse ability."""

        super().__init__(game)

        self.name = DeathPulse.name
        self.fp_bonus = 50
        self.description = f"Deals {self.fp_bonus}x Fire Power to all enemies" \
        " on the screen."
        self.image = DeathPulse.image
    
    def fire(self):
        """Fire the Death Pulse ability."""

        base_fp = self.game.ship.stats['fire_power'].value

        for alien in self.game.aliens:
            alien.take_damage(base_fp * self.fp_bonus)
        
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

    name = "Spear"
    description = "Fires a continuous stream of bullets."
    image = helper_funcs.load_image(None, 'purple', (10, 10))

    def __init__(self, game: Game):
        """Initialize the Spear ability."""

        super().__init__(game)

        self.name = Spear.name
        self.fr_bonus = 1
        self.description = "Fires a continuous stream of bullets." \
        f" Each level increases fire rate by {self.fr_bonus}."
        self.image = Spear.image
    
    def fire(self):
        """Fire the Spear ability."""

        self.game.ship.fire_bullet(self.fr_bonus * self.level)
    
    def level_up(self):
        """Increase the fire rate bonus (autocalculated by level)."""
        return super().level_up()

# -----------------------------------------------------------------------
# endregion

__all__ = ["Blank","Locked", "DeathPulse", "Spear"]