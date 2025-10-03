"""
A module that contains the classes which control the User Interface.
"""

import pygame

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(self, game, text=None, position=None):
        """Initialize the UI element."""

        self.game = game
        self.position = position
        self.size = None

        # TODO: use images for symbols instead of rectangles w. colors
        self.symbol = pygame.Rect(0, 0, 10, 10)
        self.color = 'yellow'

        if text is None:
            self.text = "Text missing."
        else:
            self.text = text
        self.text_image = self.game.config.font_normal.render(
            self.text, False, 'white', 'black'
        )
        self.text_rect = self.text_image.get_rect()

        self.calculate_positions(self.position)
        self.calculate_size()
    
    def calculate_positions(self, position=None, symbol_is_left=True):
        """Calculate the position of the symbol and the text."""

        if position is None:
            self.position = (0, 0)
        else:
            self.position = position

        self.symbol.topleft = self.position
        self.text_rect.topleft = self.position

        if symbol_is_left:
            self.text_rect.x += self.symbol.width + 3
        else:
            self.symbol.x += self.text_rect.width + 3

    
    def calculate_size(self):
        """Calculate the size of the UI element."""

        width = self.symbol.width + 3 + self.text_rect.width
        height = self.symbol.height
        if self.text_rect.height > self.symbol.height:
            height = self.text_rect.height
        
        self.size = (width, height)
        print(self.size)
    
    def draw(self):
        """Draw the UI element."""

        # TODO: use the image for the symbol instead of the rectangle
        pygame.draw.rect(self.game.screen, self.color, self.symbol)
        self.game.screen.blit(self.text_image, self.text_rect)

class ControlPanel():
    """
    A class for the control panel which displays the game state
    and buttons for touch controls (abilities).
    """

    def __init__(self, game):
        """Initialize the control panel."""

        self.game = game
        self.elements = {}

        text = str(self.game.ship.fire_power)
        self.elements["fire_power"] = UIElement(self.game, text)
        self.elements["fire_power"].calculate_positions((1, 1))

        text = str(self.game.ship.fire_rate)
        self.elements["fire_rate"] = UIElement(self.game, text)
        x = self.game.screen.width - self.elements["fire_rate"].size[0] - 1
        y = 1
        self.elements["fire_rate"].calculate_positions((x, y), False)
    
    def draw(self):
        """Draw the control panel."""

        for key, element in self.elements.items():
            element.draw()