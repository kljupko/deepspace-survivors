import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Class that manages the player ship."""

    def __init__(self, game_screen):
        super().__init__()
        """Initialize the ship."""
        self.game_screen = game_screen
        self.screen_rect = game_screen.get_rect()

        # show the ship as a rectangle
        # TODO: load ship as an image
        self.rect = pygame.Rect(20, 20, 20, 20)
        self.color = "green"

        # start at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # set the ship's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # set the ship's speed
        self.speed = 100
        self.speed_x, self.speed_y = self._calculate_relative_speed()


        # set default as not moving
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
    
    def update(self, dt):
        """Update the ship."""
        # move left or right
        if self.moving_left:
            self.x -= self.speed_x * dt
        if self.moving_right:
            self.x += self.speed_x * dt
        # move up or down
        if self.moving_up:
            self.y -= self.speed_y * dt
        if self.moving_down:
            self.y += self.speed_y * dt
        
        # return to screen if out of bounds
        if self.x < 0:
            self.x = 0
        elif self.x > self.screen_rect.width - self.rect.width:
            self.x = self.screen_rect.width - self.rect.width
        if self.y < 0:
            self.y = 0
        elif self.y > self.screen_rect.height - self.rect.height:
            self.y = self.screen_rect.height - self.rect.height
        
        # update the rectangle
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    
    def draw(self):
        """Draw the ship to the screen."""
        pygame.draw.rect(self.game_screen, self.color, self.rect)
    
    def handle_resize(self, game_screen):
        """Handles what happens when the game window is resized."""
        old_rect = self.screen_rect
        
        self.game_screen = game_screen
        self.screen_rect = self.game_screen.get_rect()

        self.speed_x, self.speed_y = self._calculate_relative_speed()
        self.x, self.y = self._calculate_relative_position(old_rect)
        
    
    def _calculate_relative_speed(self):
        """
        Calculate ship's relative speed, regardless of aspect ratio.
        """
        x_mult = self.screen_rect.width / 100
        y_mult = self.screen_rect.height / 100
        return self.speed * x_mult, self.speed * y_mult

    def _calculate_relative_position(self, old_screen_rect):
        """
        Recalculates the ship's relative position when screen is resized.
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
