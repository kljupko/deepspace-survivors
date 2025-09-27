import pygame
from entity import Entity

class Bullet(Entity):
    """A class that represents a bullet fired from the ship."""

    def __init__(self, game):
        """Initialize the bullet."""

        super().__init__(game)

        # TODO: load the bullet as an image
        self.color = "orange"
        self.rect = pygame.Rect(0, 0, 4, 4)

        # spawn bullet on top of the ship
        self.bounds = self._calculate_bounds()
        self.rect.midtop = self.game.ship.rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the bullet to move upwards
        self.base_speed_y = 50
        self.speed_x, self.speed_y = self._calculate_relative_speed()
        self.destination = (self.x, self.bounds["top"])

        # TODO: determine if bullet will have any stats

    # override Entity update method
    def update(self, dt):
        """Update the bullet."""

        self._move(dt)
        self._check_alien_collisions()
        self._check_top()
    
    def _check_alien_collisions(self):
        """Check if the bullet is colliding with any aliens."""

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        print(f"Hit {len(collisions)} aliens.")
        for alien in collisions:
            alien.hp -= self.game.ship.fire_power
            print(f"\tCurrent alien hp: {alien.hp}",
                  f"(-{self.game.ship.fire_power})")
            if alien.hp <= 0:
                alien.destroy()
        
        self.destroy()
        return True
    
    def _check_top(self):
        """Check if the bullet has moved past the top of the screen."""

        if self.y > self.bounds["top"]:
            return False
        
        self.destroy()
        return True
    
    # override Entity bounds
    def _calculate_bounds(self):
        """Calculate the bounds within which the bullet can be."""

        bounds = {}
        bounds["top"] = self.screen_rect.top - self.rect.height
        bounds["right"] = self.screen_rect.right - self.rect.width
        bounds["bottom"] = self.screen_rect.bottom
        bounds["left"] = self.screen_rect.left

        return bounds

    def destroy(self):
        """Destroy the bullet."""

        self.game.bullets.remove(self)
        print("Bullet removed.")