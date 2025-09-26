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
        self.rect.midbottom = self.screen_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.bounds = self._calculate_bounds()

        # allow the alien to move downwards
        self.base_speed_y = 25
        self.speed_x, self.speed_y = self._calculate_relative_speed()
        self.moving_down = True

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
        self.destroy()
        print(f"Alien moved past ship! HP reduced to {self.game.ship.hp}",
                f"(-{self.damage})")
        return True
    
    # override Entity bounds
    def _calculate_bounds(self):
        """Calculate the bounds within which the alien can be."""

        bounds = {}
        bounds["top"] = self.screen_rect.top - self.rect.height
        bounds["right"] = self.screen_rect.right - self.rect.width
        bounds["bottom"] = self.screen_rect.bottom
        bounds["left"] = self.screen_rect.left

        return bounds
    
    def destroy(self):
        """Destroy the alien. Handle sounds, animations, etc."""

        # TODO: add random chance to drop powerup, choose random powerup
        self.game.powerups.add(
            powerups.AddAbility(
                self.game, self.rect.center,
                abilities.Spear(self.game)
            )
        )

        # TODO: play sounds and animations
        self.game.aliens.remove(self)