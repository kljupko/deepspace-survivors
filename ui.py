"""
A module that contains the classes which control the User Interface.
"""

import pygame

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(self, game, content, symbol=None, symbol_is_left=True,
                 position=(0, 0), anchor="topleft"):
        """Initialize the UI element."""

        self.game = game

        self._load_content(content)
        self._load_symbol(symbol, symbol_is_left)

        self.position = position
        self.anchor = anchor

        self._calculate_size()
        self._calculate_draw_position()
        self._calculate_rect_positions()
    
    def _load_content(self, content):
        """Load the text content to display."""

        self.content = self.game.config.font_normal.render(
            str(content), False, 'white', 'black'
        )
        self.content_rect = self.content.get_rect()
    
    def _load_symbol(self, symbol, symbol_is_left):
        """Load the symbol to display."""

        if symbol is None:
            symbol = pygame.Surface((10, 10))
            pygame.draw.rect(symbol, "pink", (0, 0, 10, 10))
        elif symbol is False:
            # element will be an empty surface with a size of 0
            symbol = pygame.Surface((0, 0))
        else:
            # TODO: load the image of the symbol, assign it to symbol
            pass

        self.symbol = symbol
        self.symbol_rect = self.symbol.get_rect()
        self.symbol_is_left = symbol_is_left
    
    def _calculate_size(self):
        """Calculate the size of the UI element."""

        padding = 3

        width = self.content_rect.width
        if self.symbol_rect.width > 0:
            width += self.symbol_rect.width + padding

        height = self.content_rect.height
        if self.symbol_rect.height > self.content_rect.height:
            height = self.symbol_rect.height
        
        self.size = (width, height)
    
    def _calculate_draw_position(self):
        """
        Calculate the position at which the UI element will be drawn,
        based on the anchor and whether there is a symbol.
        """

        draw_x = self.position[0]
        if self.anchor in ["midtop", "center", "midbottom"]:
            draw_x -= self.size[0] // 2
        elif self.anchor in ["topright", "midright", "bottomright"]:
            draw_x -= self.size[0]
        
        draw_y = self.position[1]
        if self.anchor in ["midleft", "center", "midright"]:
            draw_y -= self.size[1] // 2
        elif self.anchor in ["bottomleft", "midbottom", "bottomright"]:
            draw_y -= self.size[1]
        
        self.draw_position = (draw_x, draw_y)
    
    def _calculate_rect_positions(self):
        """Calculate the positions of the symbol and the text rects."""

        self.content_rect.x, self.content_rect.y = self.draw_position
        self.symbol_rect.x, self.symbol_rect.y = self.draw_position

        if self.symbol_rect.width > 0:
            padding = 3 # px
        else:
            padding = 0

        if self.symbol_is_left:
            self.content_rect.x += self.symbol_rect.width + padding
        else:
            self.symbol_rect.x += self.content_rect.width + padding
    
    def update(self, content=None, symbol=None, symbol_is_left=None,
                 position=None, anchor=None):
        """
        Update the UI element. For better performance, this method should
        not run in the game's main loop, but only when called by an event
        that triggers it, such as when the player ship loses HP.
        """

        if content is None:
            content = self.content
        if symbol is None:
            symbol = self.symbol
        if symbol_is_left is None:
            symbol_is_left = self.symbol_is_left
        if position is None:
            position = self.position
        if anchor is None:
            anchor = self.anchor

        self._load_content(content)
        self._load_symbol(symbol, symbol_is_left)

        self.position = position
        self.anchor = anchor

        self._calculate_size()
        self._calculate_draw_position()
        self._calculate_rect_positions()

    def draw(self):
        """Draw the UI element."""
        
        self.game.screen.blit(self.symbol, self.symbol_rect)
        self.game.screen.blit(self.content, self.content_rect)

class ControlPanel():
    """
    A class for the control panel which displays the game state
    and buttons for touch controls (abilities).
    """

    def __init__(self, game):
        """Initialize the control panel."""

        self.game = game
        self.elements = {}

        self.elements["fire_power"] = UIElement(
            self.game, self.game.ship.fire_power, position=(1, 1)
        )

        self.elements["fire_rate"] = UIElement(
            self.game, self.game.ship.fire_rate, position=(
                self.game.screen.width - 1, 1
            ), symbol_is_left=False, anchor="topright"
        )

        self.elements["session_duration"] = UIElement(
            self.game, "00:00", False, position=(
                self.game.screen.get_rect().centerx, 1
            ),
            anchor="midtop"
        )

        self.elements["credits_earned"] = UIElement(
            self.game, self.game.state.credits_earned, position=(
                self.game.screen.get_rect().centerx,
                self.elements["session_duration"].draw_position[1] +
                self.elements["session_duration"].size[1] + 1
            ), anchor="midtop"
        )

        self.elements["ship_hp"] = UIElement(
            self.game, self.game.ship.hp, position=(
                1, self.game.screen.height - 1
            ),
            anchor="bottomleft"
        )

        self.elements["ship_thrust"] = UIElement(
            self.game, self.game.ship.thrust, symbol_is_left=False, position=(
                self.game.screen.width - 1, self.game.screen.height - 1
            ), anchor="bottomright"
        )

    
    def draw(self):
        """Draw the control panel."""

        for element in self.elements.values():
            element.draw()