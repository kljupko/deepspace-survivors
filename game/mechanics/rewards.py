"""A module containing the classes for the unlockable rewards."""

from ..utils import helper_funcs

class Reward():
    """A base class representing a reward."""

    def __init__(self, game, name="Base Reward", image=None):
        """Initialize the reward."""

        self.game = game
        self.name = name
        self.instructions = "You can't earn this base reward."
        self.is_unlocked = False

        if image is None:
            image = helper_funcs.load_image(None, 'gray', (10, 10))
        self.image = image
    
    def check_availability(self):
        """Return True if conditions are met for the reward to unlock."""

        # to be overwritten by child classes
        return False

    def unlock(self):
        """Unlocks the reward if conditions are met."""

        if self.check_availability():
            self.is_unlocked = True
            return True
        return False

class ClaimableReward(Reward):
    """A class representing a reward that can be claimed once."""

    def __init__(self, game, name="Claimable Reward", credits=None, image=None):
        """Initialize the reward."""
        
        super().__init__(game, name, image)
        self.instructions = "You can't earn this base claimable reward."
        self.is_claimed = False
        self.credits = credits
    
    def claim(self):
        """Claims the reward, if unlocked."""

        if self.is_claimed:
            return False

        if self.credits is not None:
            self.game.data['credits'] += self.credits
        
        # to be augmented by child classes maybe
        self.is_claimed = True
        return True

class ToggleableReward(Reward):
    """
    A class representing a reward that can be toggled.
    For instance, the player could toggle playing as a certain class of
    ship, after it is unlocked.
    """

    def __init__(self, game, name="Toggleable Reward", image=None):
        """Initialize the reward."""

        super().__init__(game, name, image)
        self.instructions = "You can't earn this base toggleable reward."
        self.is_toggled_on = False

    def toggle_on(self):
        """Turn the reward on."""

        self.is_toggled_on = True
        # to be augmented by child classes
        return True
    
    def toggle_off(self):
        """Turn the reward off."""

        self.is_toggled_on = False
        # to be augmented by child classes
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

    def __init__(self, game, name="Baker's Dozen", credits=1300, image=None):
        """Initialize the reward."""

        if image is None:
            image = helper_funcs.load_image(None, 'gold', (10, 10))
        
        super().__init__(game, name, credits, image)
        self.instructions = "Kill 13 aliens in a single session."

    # override the grandparent method
    def check_availability(self):
        """Check if the reward can be claimed."""

        if self.game.state.killcount >= 13:
            return True
        return False
    
    # no need to override the claim method, it's just a monetary reward

class SpearFishReward(ToggleableReward):
    """Toggleable reward, granting you the SpearFish class ship."""

    def __init__(self, game, name="SpearFish", image=None):
        """Initialize the reward."""

        if image is None:
            image = helper_funcs.load_image(None, 'darkslategray3', (10, 10))
        
        super().__init__(game, name, image)
        self.instructions = "End the session with a Fire Rate of 10 or more."
    
    # override the grandparent method
    def check_availability(self):
        """Check if the reward can be unlocked."""

        if self.game.ship.stats['Fire Rate'].value >= 10:
            return True
        return False
    
    def toggle_on(self):
        """Enable the SpearFish and disable other ships."""

        for ship_reward in self.game.toggleable_ships.values():
            ship_reward.toggle_off()
        
        # TODO: figure out how to avoid circular imports
        self.game.ship_class = SpearFish
        return super().toggle_on()
    
    def toggle_off(self):
        """Disable the SpearFish."""

        # TODO: figure out how to avoid circular imports
        self.game.ship_class = Ship
        return super().toggle_off()

__all__ = ["BakersDozen", "SpearFishReward"]