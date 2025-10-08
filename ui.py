"""
A module that contains the classes which control the User Interface.
"""

import pygame

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(
            self, game, name, parent_surface, content="", symbol=None,
            symbol_is_left=True, position=(0, 0), anchor="topleft", font=None,
            action=None
    ):
        """Initialize the UI element."""

        self.game = game
        self.name = name
        self.parent_surface = parent_surface
        self.action = action

        self._load_content(content, font)
        self._load_symbol(symbol, symbol_is_left)

        self.anchor_position = position
        self.anchor = anchor
        self.rect = pygame.Rect(0, 0 ,0, 0)

        self._calculate_size()
        self._calculate_draw_position()
        self._calculate_rect_positions()

    def _load_content(self, content, font):
        """Load the text content to display."""

        if font is None:
            font = self.game.config.font_normal

        self.content = font.render(
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
        
        self.rect.width = width
        self.rect.height = height
    
    def _calculate_draw_position(self):
        """
        Calculate the position at which the UI element will be drawn,
        based on the anchor and whether there is a symbol.
        """

        draw_x = self.anchor_position[0]
        if self.anchor in ["midtop", "center", "midbottom"]:
            draw_x -= self.rect.width // 2
        elif self.anchor in ["topright", "midright", "bottomright"]:
            draw_x -= self.rect.width
        
        draw_y = self.anchor_position[1]
        if self.anchor in ["midleft", "center", "midright"]:
            draw_y -= self.rect.height // 2
        elif self.anchor in ["bottomleft", "midbottom", "bottomright"]:
            draw_y -= self.rect.height
        
        self.rect.x = draw_x
        self.rect.y = draw_y
    
    def _calculate_rect_positions(self):
        """Calculate the positions of the symbol and the text rects."""

        self.content_rect.x, self.content_rect.y = self.rect.topleft
        self.symbol_rect.x, self.symbol_rect.y = self.rect.topleft

        if self.symbol_rect.width > 0:
            padding = 3 # px
        else:
            padding = 0

        if self.symbol_is_left:
            self.content_rect.x += self.symbol_rect.width + padding
        else:
            self.symbol_rect.x += self.content_rect.width + padding
    
    def trigger(self):
        """Hook for doing something when the element is activated."""

        if self.action is None:
            return False
        
        self.action()
        return True
    
    def update(self, content=None, symbol=None, symbol_is_left=None,
                 position=None, anchor=None, font=None):
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
            position = self.anchor_position
        if anchor is None:
            anchor = self.anchor

        self._load_content(content, font)
        self._load_symbol(symbol, symbol_is_left)

        self.anchor = anchor

        self._calculate_size()
        self._calculate_draw_position()
        self._calculate_rect_positions()
    
    def draw(self):
        """Draw the element to the parent surface."""

        self.parent_surface.blit(self.symbol, self.symbol_rect)
        self.parent_surface.blit(self.content, self.content_rect)

class Menu():
    """A base class representing a menu."""

    def __init__(self, game, width=None, height=None, background=None):
        """Initialize the menu."""

        self.game = game
        self.visible = False # determines if menu is shown
        self.focused = False # determines if menu can be interacted with

        if width is None:
            width = self.game.screen.width
        if height is None:
            height = self.game.screen.height

        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()

        if background is None:
            background = pygame.Surface((width, height))
            pygame.draw.rect(background, "black", background.get_rect())
        self.background = background

        self.elements = {}
    
    def show(self):
        """Make the menu visible and interactive."""

        self.visible = True
        self.focused = True

    def hide(self):
        """Make the menu hidden and non-interactive."""

        self.visible = False
        self.focused = False
    
    def focus(self):
        """Make only this menu interactive."""

        if not self.visible:
            return False
        
        self.focused = True

        # TODO: unfocus all other menus
    
    def unfocus(self):
        """Make the menu non-interactive."""

        self.focused = False
    
    def trigger(self, element_name):
        """Interact with an element in the menu."""

        if element_name not in self.elements:
            return False
        
        self.elements[element_name].trigger()
        return True
    
    def draw(self):
        """Draw the menu to the screen."""

        if not self.visible:
            return False
        
        self.surface.blit(self.background, self.background.get_rect())

        for element in self.elements.values():
            element.draw()
        
        self.game.screen.blit(self.surface, self.rect)

class MainMenu(Menu):
    """A class which represents the game's main menu."""

    def __init__(self, game, width=None, height=None, background=None):
        """Initialize the main menu."""

        super().__init__(game, width, height, background)

        self.visible = True
        self.focused = True

        el_name = "play_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Play", position=(
                self.rect.width * 1/3,
                self.rect.height * 1/3
            ), anchor="topleft"
        )
        el_name = "upgrade_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Upgrade", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 1
            ), anchor="topleft"
        )
        el_name = "unlock_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Unlock",position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 2
            ), anchor="topleft"
        )
        el_name = "settings_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Settings", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 3
            ), anchor="topleft"
        )
        el_name = "info_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Info", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 4
            ), anchor="topleft"
        )
        el_name = "quit_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Quit", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 5
            ), anchor="topleft"
        )


class Tray(Menu):
    """A base class for the top and bottom trays."""

    def __init__(self, game, width=None, height=None, background=None):
        """Initialize the tray with a surface."""

        super().__init__(game, width, height, background)

        pygame.draw.rect(self.background, "white", self.background.get_rect())

        self.visible = True
        self.focused = True


class TopTray(Tray):
    """A class representing the top tray."""

    def __init__(self, game, width=None, height=None, background=None):
        """Initialize the top tray."""

        super().__init__(game, width, height, background)

        el_name = "fire_power"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self.game.ship.fire_power,
            position=(1, 1)
        )

        el_name = "fire_rate"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self.game.ship.fire_rate,
            position=(self.rect.width - 1, 1), symbol_is_left=False,
            anchor="topright"
        )

        el_name = "session_duration"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "00:00", False,
            position=(self.rect.centerx, 1), anchor="midtop"
        )

        el_name = "credits_earned"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            self.game.state.credits_earned,
            position=(self.rect.centerx, 12), anchor="midtop"
        )

class BottomTray(Tray):
    """A class representing the bottom tray."""

    def __init__(self, game, width=None, height=None, background=None):
        """Initialize the bottom tray."""

        super().__init__(game, width, height, background)
        self.rect.y = self.game.screen.height - self.rect.height

        el_name = "ship_hp"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self.game.ship.hp,
            position=(1, 1)
        )

        el_name = "ship_thrust"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self.game.ship.thrust,
            symbol_is_left=False, position=(self.rect.width - 1, 1),
            anchor="topright"
        )

        # temporary image for the abilities
        # TODO: replace with real image
        image = pygame.Surface((18, 18))
        pygame.draw.rect(image, "gray", (0, 0, 18, 18))

        el_name = "active_1"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 4 * 1, 12), anchor="midtop",
            action=self.game.ship.active_abilities[0].toggle
        )

        el_name = "active_2"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 4 * 2, 12), anchor="midtop",
            action=self.game.ship.active_abilities[1].toggle
        )

        el_name = "active_3"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 4 * 3, 12), anchor="midtop",
            action=self.game.ship.active_abilities[2].toggle
        )

        el_name = "passive_1"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 8 * 1, self.rect.height - 1),
            anchor="midbottom",
            action=self.game.ship.passive_abilities[0].toggle
        )

        el_name = "passive_2"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 8 * 3, self.rect.height - 1),
            anchor="midbottom",
            action=self.game.ship.passive_abilities[1].toggle
        )

        el_name = "passive_3"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 8 * 5, self.rect.height - 1),
            anchor="midbottom",
            action=self.game.ship.passive_abilities[2].toggle
        )

        el_name = "passive_4"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, symbol=image,
            position=(self.rect.width // 8 * 7, self.rect.height - 1),
            anchor="midbottom",
            action=self.game.ship.passive_abilities[3].toggle
        )