"""
A module containing the classes for the active and passive abilities.
"""

class Ability():
    """A base class that represents a ship's ability."""

    def __init__(self, game):
        """Initialize the ability."""

        self.game = game
        self.name = "Base Ability"
        self.description = "Ability description."
        self.enabled = False
    
    def toggle(self):
        """Toggle the ability On/Off."""

        self.enabled = not self.enabled

    def fire(self):
        """Fire the ability"""

        print(f"Hook for firing: {self.name}.")

class PassiveAbility(Ability):
    """A class that represents a ship's passive ability."""

    def __init__(self, game):
        """Initialize the passive ability."""

        super().__init__(game)

        self.name = "Base Passive Ability"
        self.description = "Passive ability description."
        self.level = 1
        self.enabled = True

class Spear(PassiveAbility):
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
    
    def fire(self):
        """Fire the Spear ability."""

        self.game.ship.fire_bullet(self.fr_bonus)

class DeathPulse(Ability):
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
    
    def fire(self):
        """Fire the Death Pulse ability."""

        for alien in self.game.aliens:
            alien.hp -= self.game.ship.fire_power * self.fp_bonus
            if alien.hp <= 0:
                alien.destroy()