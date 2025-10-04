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

        # TODO: add element anchor (similar to Rect virtual attributes)

        # TODO: use images for symbols instead of rectangles w. colors
        # TODO: implement solution for elements without symbols
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
    
    def calculate_positions(self, position=None, is_symbol_left=True):
        """Calculate the position of the symbol and the text."""

        if position is None:
            self.position = (0, 0)
        else:
            self.position = position

        self.symbol.topleft = self.position
        self.text_rect.topleft = self.position

        if is_symbol_left:
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
    
    def update(self, text=None, symbol=None, is_symbol_left=True):
        """
        Update the UI element. For better performance, this method should
        not run in the game's main loop, but only when called by an event
        that triggers it, such as when the player ship loses HP.
        """

        old_size = self.size

        if text is None:
            text = self.text
        self.text_image = self.game.config.font_normal.render(
            text, False, 'white', 'black'
        )
        self.text_rect = self.text_image.get_rect()

        if symbol is None:
            symbol = self.symbol
        # TODO: handle replacing the image

        self.calculate_size()

        # TODO: handle repositioning based on element anchor
        if is_symbol_left:
            x_diff = 0
        else:
            x_diff = old_size[0] - self.size[0]
        new_pos = (self.position[0] + x_diff, self.position[1])
        self.calculate_positions(new_pos, is_symbol_left)

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
        element = self.elements["fire_power"]
        element.calculate_positions((1, 1))

        text = str(self.game.ship.fire_rate)
        self.elements["fire_rate"] = UIElement(self.game, text)
        element = self.elements["fire_rate"]
        x = self.game.screen.width - element.size[0] - 1
        y = 1
        element.calculate_positions((x, y), False)

        text = "00:00"
        self.elements["session_duration"] = UIElement(self.game, text)
        element = self.elements["session_duration"]
        x = self.game.screen.get_rect().centerx - element.size[0] // 2
        y = 1
        element.calculate_positions((x, y))

        text = str(self.game.state.credits_earned)
        self.elements["credits_earned"] = UIElement(self.game, text)
        element = self.elements["credits_earned"]
        x = self.game.screen.get_rect().centerx - element.size[0] // 2
        y = 13
        element.calculate_positions((x, y))

        text = str(self.game.ship.hp)
        self.elements["hit_points"] = UIElement(self.game, text)
        element = self.elements["hit_points"]
        x = 1
        y = self.game.screen.height - element.size[1] - 1
        element.calculate_positions((x, y))

        text = str(self.game.ship.thrust)
        self.elements["thrust"] = UIElement(self.game, text)
        element = self.elements["thrust"]
        x = self.game.screen.width - element.size[0] - 1
        y = self.game.screen.height - element.size[1] - 1
        element.calculate_positions((x, y), False)

    
    def draw(self):
        """Draw the control panel."""

        for key, element in self.elements.items():
            element.draw()