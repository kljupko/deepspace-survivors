"""
A module containing the classes for the active and passive abilities.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

import pygame

from ..utils import helper_funcs

class Ability():
    """A grandparent class representing a ship's ability."""

    name: str = "Base Ability"
    description: str = "Base Ability description."
    image: pygame.Surface = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 description: str | None = None,
                 image: pygame.Surface | None = None,
                 ):
        """Initialize the ability and add it to the given slot."""

        self.game = game

        if name is None:
            name = Ability.name
        self.name = name

        if description is None:
            description = Ability.description
        self.description = description

        if image is None:
            image = Ability.image
        self.image = image
    
    def fire(self):
        """
        Hook for firing the ability. Does nothing.
        Overridden by grandchild classes.
        """

        return None
    
    def _remove(self):
        """Remove the ability from the slot."""

        for slot in self.game.ship.ability_slots.values():
            if not isinstance(slot, Slot):
                continue

            if slot.ability is self:
                slot.set_ability(None)
                break
    
class Active(Ability):
    """A base class that represents a ship's active ability."""

    name = "Base Active Ability"
    description = "Base Active Ability description."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 description: str | None = None,
                 image: pygame.Surface | None = None,
                 ):
        """Initialize the active ability."""

        if name is None:
            name = Active.name
        
        if description is None:
            description = Active.description
        
        if image is None:
            image = Active.image
        
        super().__init__(game, name, description, image)
    
    def fire(self):
        """
        Fire the active ability, and remove from the containing slot.
        """

        super().fire()
        self._remove()

class Passive(Ability):
    """A class that represents a ship's passive ability."""

    name = "Base Passive Ability"
    description = "Base Passive Ability description."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 description: str | None = None,
                 image: pygame.Surface | None = None,
                 ):
        """Initialize the passive ability."""

        if name is None:
            name = Active.name
        
        if description is None:
            description = Active.description
        
        if image is None:
            image = Active.image
        
        super().__init__(game, name, description, image)

        self.level = 1
    
    def level_up(self):
        """Increase the level of the passive ability."""

        self.level += 1

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

    def __init__(self,
                 game: Game,
                 ):
        """Initialize the Death Pulse ability."""

        name = DeathPulse.name
        img = DeathPulse.image
        super().__init__(game, name, None, img)

        self.fp_bonus = 50
        self.description = f"Deals {self.fp_bonus}x Fire Power to all enemies" \
        " on the screen."
    
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

    def __init__(self,
                 game: Game,
                 ):
        """Initialize the Spear ability."""

        name = Spear.name
        img = Spear.image
        super().__init__(game, name, None, img)

        self.fr_bonus = 1
        self.description = "Fires a continuous stream of bullets." \
        f" Each level increases fire rate by {self.fr_bonus}."
    
    def fire(self):
        """Fire the Spear ability."""

        self.game.ship.fire_bullet(self.fr_bonus * self.level)
    
    # level up handled by parent class -- only incease level

# -----------------------------------------------------------------------
# endregion

class Slot():
    """
    A class representing a ship's slot which can hold a single ability.
    """

    class SlotImagesDict(TypedDict):
        """A class representing a dictionary of slot images."""

        blank_active: pygame.Surface
        blank_passive: pygame.Surface
        locked_active: pygame.Surface
        locked_passive: pygame.Surface
    
    img_options: SlotImagesDict = {
        'blank_active': helper_funcs.load_image(None, 'grey', (12, 12)),
        'blank_passive': helper_funcs.load_image(None, 'grey', (12, 12)),
        'locked_active': helper_funcs.load_image(None, 'black', (12, 12)),
        'locked_passive': helper_funcs.load_image(None, 'black', (12, 12)),
    }

    def __init__(self,
                 game: Game,
                 ability_type: type[Active | Passive] = Passive,
                 is_locked: bool = False,
                 ) -> None:
        """Initialize the slot."""

        self.game = game
        self.ability_type = ability_type
        self.ability: Ability | None = None
        self.is_locked = is_locked
        self.is_enabled = False

        if not self.is_locked:
            if self.ability_type is Active:
                self.image = Slot.img_options["blank_active"]
            else:
                self.image = Slot.img_options["blank_passive"]
        else:
            if self.ability_type is Active:
                self.image = Slot.img_options["locked_active"]
            else:
                self.image = Slot.img_options["locked_passive"]
    
    def can_accept_ability(self, ability_class: type[Ability]):
        """
        Return True if an ability of the given class can be set to
        this slot. The ability cannot be added if:
          - the slot is locked
          - the ablility type is incorrect (Active vs. Passive)
          - the slot already contains an active ability
          - the slot contains a different passive ability
        """

        if self.is_locked:
            return False
        
        ability = ability_class(self.game)

        if not isinstance(ability, self.ability_type):
            return False
        
        if self.ability_type is Active and self.ability is not None:
            return False
        
        if self.ability_type is Passive and self.ability is not None:
            if self.ability.name != ability.name:
                return False
        
        return True
    
    def set_ability(self, ability_class: type[Ability] | None):
        """
        Set the slot's ability to the one given, or levels up the
        identical passive ability.
        """

        if ability_class is None:
            self.ability = None
            return
        
        ability = ability_class(self.game)
        if isinstance(self.ability, Passive) and type(self.ability) is type(ability):
            self.ability.level_up()
            self.game.bot_tray.update()
            return
        
        self.ability = ability_class(self.game)
        self.game.bot_tray.update()

        if isinstance(self.ability, Passive):
            self.toggle(True)
            return
    
    def toggle(self, state: bool | None = None):
        """Enable or disable the slot."""

        if self.ability is None:
            self.is_enabled = False
            return
        
        if state:
            self.is_enabled = state
        else:
            self.is_enabled = not self.is_enabled
    
    def fire_ability(self):
        """Fire the ability, if present."""

        if self.ability is None or not self.is_enabled:
            return
        
        self.ability.fire()

        if self.ability_type is Active:
            self.toggle(False)
    
    def get_ability_image(self):
        """
        Return the image of the slot's ability. If the slot is empty,
        return a default image.
        """

        dflt_img = helper_funcs.load_image(None, 'black', (10, 10))

        if self.ability:
            return self.ability.image
        return dflt_img

__all__ = [
    "DeathPulse",
    "Spear",
    "Slot"
]