import pygame
from pygame.sprite import Sprite

class Entity(Sprite):
    """
    Class that manages the base game entities. Serves as the base from
    which other game objects inherit methods and properties.
    """

    def __init__(self, game):
        """Initialize the entity."""
        
        super().__init__()
        self.game = game
        self.game_screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # show the entity as a rectangle
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.color = "pink"

        # start at the center of the screen
        self.rect.center = self.screen_rect.center

        # set the entity's bounds
        self.bounds = self._calculate_bounds()

        # set the entity's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # set the entity's speed
        self.base_speed_x = 0
        self.base_speed_y = 0
        self.speed_x, self.speed_y = self._calculate_relative_speed()

        # set default as not moving
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
    
    def update(self, dt):
        """Update the entity."""

        self._move(dt)

    def _move(self, dt):
        """Move the entity."""
        
        if self.moving_left:
            self.x -= self.speed_x * dt
        if self.moving_right:
            self.x += self.speed_x * dt
        if self.moving_up:
            self.y -= self.speed_y * dt
        if self.moving_down:
            self.y += self.speed_y * dt
        
        # return to screen if out of bounds
        if self.x < self.bounds["left"]:
            self.x = self.bounds["left"]
        elif self.x > self.bounds["right"]:
            self.x = self.bounds["right"]
        if self.y < self.bounds["top"]:
            self.y = self.bounds["top"]
        elif self.y > self.bounds["bottom"]:
            self.y = self.bounds["bottom"]
        
        # update the rectangle
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    
    def draw(self):
        """Draw the entity to the screen."""

        pygame.draw.rect(self.game_screen, self.color, self.rect)
    
    def handle_resize(self):
        """Handle what happens when the game window is resized."""

        old_rect = self.screen_rect
        self.screen_rect = self.game_screen.get_rect()

        self.bounds = self._calculate_bounds()

        self.speed_x, self.speed_y = self._calculate_relative_speed()
        self.x, self.y = self._calculate_relative_position(old_rect)
    
    def _calculate_bounds(self):
        """Calculate the bounds within which the entity can be."""

        bounds = {}
        bounds["top"] = self.screen_rect.top
        bounds["right"] = self.screen_rect.right - self.rect.width
        bounds["bottom"] = self.screen_rect.bottom - self.rect.height
        bounds["left"] = self.screen_rect.left

        return bounds
        
    def _calculate_relative_speed(self):
        """
        Calculate entity's relative speed, regardless of aspect ratio.
        """

        x_mult = self.screen_rect.width / 100
        y_mult = self.screen_rect.height / 100

        return self.base_speed_x * x_mult, self.base_speed_y * y_mult

    def _calculate_relative_position(self, old_screen_rect):
        """
        Calculate the entity's relative position
        when the screen is resized.
        """

        rel_x = self.rect.x / old_screen_rect.width
        rel_y = self.rect.y / old_screen_rect.height
        
        if self.rect.x == 0:
            x = 0
        elif self.rect.right == old_screen_rect.right:
            x = self.screen_rect.right
        else:
            x = float(self.screen_rect.width * rel_x)

        if self.rect.y == 0:
            y = 0
        elif self.rect.bottom == old_screen_rect.bottom:
            y = self.screen_rect.bottom
        else:
            y = float(self.screen_rect.height * rel_y)
        
        return x, y