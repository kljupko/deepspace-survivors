"""A module containing the classes for the unlockable rewards."""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game

import pygame
from ..utils import helper_funcs

class Reward():
    """A base class representing a reward."""

    name = "Base Reward"
    instructions = "You can't earn this base reward."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game : Game,
                 name: str | None = None,
                 instructions: str | None = None,
                 image: pygame.Surface | None = None
                 ):
        """Initialize the reward."""

        self.game = game

        if name is None:
            name = Reward.name
        self.name = name

        if instructions is None:
            instructions = Reward.instructions
        self.instructions = instructions

        if image is None:
            image = helper_funcs.copy_image(Reward.image)
        self.image = image

        self.is_unlocked = False
    
    def check_availability(self) -> bool:
        """Return True if conditions are met for the reward to unlock."""

        # to be overwritten by child classes
        return False

    def unlock(self):
        """Unlocks the reward if conditions are met."""

        if self.check_availability():
            self.is_unlocked = True
            self.game.progress.data['rewards'][self.name][0] = True
            self.game.progress.save_data()
            return True
        return False

class ClaimableReward(Reward):
    """A class representing a reward that can be claimed once."""

    name = "Base Claimable Reward"
    instructions = "You can't earn this base claimable reward."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 instructions: str | None = None,
                 image: pygame.Surface | None = None,
                 credits: int = 0
                 ):
        """Initialize the reward."""

        if name is None:
            name = ClaimableReward.name
        if instructions is None:
            instructions = ClaimableReward.instructions
        if image is None:
            image = ClaimableReward.image

        super().__init__(game, name, instructions, image)
        self.is_claimed = False
        self.credits = credits
    
    def claim(self):
        """Claims the reward, if unlocked."""

        if self.is_claimed:
            return False
        
        self.game.progress.data['credits'] += self.credits
        
        # to be augmented by child classes maybe
        self.is_claimed = True
        self.game.progress.data['rewards'][self.name][1] = True
        self.game.progress.save_data()
        return True

class ToggleableReward(Reward):
    """
    A class representing a reward that can be toggled.
    For instance, the player could toggle playing as a certain class of
    ship, after it is unlocked.
    """

    name = "Base Toggleable Reward"
    instructions = "You can't earn this base toggleable reward."
    image = helper_funcs.load_image(None, 'gray', (10, 10))

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 instructions: str | None = None,
                 image: pygame.Surface | None = None
                 ):
        """Initialize the reward."""

        if name is None:
            name = ToggleableReward.name
        if instructions is None:
            instructions = ToggleableReward.instructions
        if image is None:
            image = ToggleableReward.image

        super().__init__(game, name, instructions, image)
        self.is_toggled_on = False

    def toggle_on(self):
        """Turn the reward on."""

        # to be augmented by child classes
        self.is_toggled_on = True
        self.game.progress.data['rewards'][self.name][1] = True
        self.game.progress.save_data()
        return True
    
    def toggle_off(self):
        """Turn the reward off."""

        # to be augmented by child classes
        self.is_toggled_on = False
        self.game.progress.data['rewards'][self.name][1] = False
        self.game.progress.save_data()
        return False

    def toggle(self):
        """Toggles the reward on or off."""

        if self.is_toggled_on:
            self.toggle_off()
        else:
            self.toggle_on()
        return self.is_toggled_on

class BakersDozen(ClaimableReward):
    """Claimable reward for destroying 13 aliens in one session."""

    name = "Baker's Dozen"
    instructions = "Kill at least 13 aliens in a single session."
    image = helper_funcs.load_image(None, 'gold', (10, 10))

    def __init__(self, game: Game):
        """Initialize the reward."""
        
        name = BakersDozen.name
        instructions = BakersDozen.instructions
        image = BakersDozen.image
        credits = 1300
        super().__init__(game, name, instructions, image, credits)

    # override the grandparent method
    def check_availability(self):
        """Check if the reward can be claimed."""

        if self.game.state.killcount >= 13:
            return True
        return False
    
    # no need to override the claim method, it's just a monetary reward

class SpearFish(ToggleableReward):
    """Toggleable reward, granting you the SpearFish class ship."""

    name = "SpearFish"
    instructions = "End a session with a Fire Rate of 10 or more."
    # TODO: load the ship's image, without circular imports
    image = helper_funcs.load_image(None, 'darkslategray3', (10, 10))

    def __init__(self, game: Game):
        """Initialize the reward."""

        name = SpearFish.name
        instructions = SpearFish.instructions
        image = SpearFish.image
        super().__init__(game, name, instructions, image)
    
    # override the grandparent method
    def check_availability(self):
        """Check if the reward can be unlocked."""

        if self.game.ship.stats['fire_rate'].value >= 10:
            return True
        return False
    
    def toggle_on(self):
        """Enable the SpearFish and disable other ships."""


        for ship_reward in self.game.toggleable_ships:
            ship_reward.toggle_off()
        
        from ..entities import SpearFish
        self.game.ship_class = SpearFish
        return super().toggle_on()
    
    def toggle_off(self):
        """Disable the SpearFish."""

        self.game.ship_class = self.game.default_ship_class
        return super().toggle_off()

__all__ = ["BakersDozen", "SpearFish"]