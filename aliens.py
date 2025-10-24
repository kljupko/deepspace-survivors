"""
A module containing all the aliens.
"""

from entity import Entity
import abilities
import powerups

class Alien(Entity):
    """Base class that manages the aliens."""

    def __init__(self, game):
        """Initialize the alien."""

        super().__init__(game)

        # TODO: load alien as an image
        self.color = "red"

        # spawn enemy above the screen
        self.rect.midbottom = self.game.play_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self._calculate_bounds(pad_bot=-self.rect.height)

        # allow the alien to move downwards
        self.base_speed_y = self.game.config.base_speed * 0.25
        self._calculate_relative_speed()
        self.destination = (self.x, self.bounds["bottom"])

        # alien stats
        self.hp = 2
        self.speed = 1
        self.damage = 1
        self.credits = 10
    
    # override Entity update method
    def update(self, dt):
        """Update the alien."""

        self._move(dt)
        self._check_bottom()
    
    def _check_bottom(self):
        """
        Check if the alien is past the bottom of the screen.
        If so, destroy alien and reduce player ship hit points.
        """

        if self.y < self.bounds["bottom"]:
            return False
        
        self.game.ship.hp -= self.damage
        self.game.bot_tray.update()
        
        self.destroy()
        return True
    
    def take_damage(self, damage):
        """
        Reduce the alien's HP by the given amount.
        The alien is destroyed if HP is 0 or less. Returns True.
        Handle powerup drops.
        """

        self.hp -= damage
        if self.hp > 0:
            return False
        
        # TODO: add random chance to drop powerup, choose random powerup
        self.game.powerups.add(
            powerups.AddAbility(
                self.game, self.rect.center,
                abilities.Spear(self.game)
            )
        )
        self.game.state.credits_earned += self.credits
        self.game.top_tray.update()

        self.destroy()
        return True
    
    def destroy(self):
        """Destroy the alien. Handle sounds, animations, etc."""

        # TODO: play sounds and animations
        self.kill()