"""A module containing the base classes for the User Interface."""

import pygame

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(
            self, game, name, parent, content="", symbol=None,
            symbol_is_left=True, position=(0, 0), anchor="topleft", font=None,
            action=None
    ):
        """Initialize the UI element."""

        self.game = game
        self.name = name
        self.parent = parent
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
        
        wraplength = int(self.parent.surface.width * 0.9)

        self.content = font.render(
            str(content), False, 'white', 'black', wraplength
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

        self.parent.surface.blit(self.symbol, self.symbol_rect)
        self.parent.surface.blit(self.content, self.content_rect)

class ElemUnion():
    """A class representing a union of multiple UI Elements."""

    def __init__(self, game, name, *elems, action=None):
        """Initialize the union."""

        self.game = game
        self.name = name
        self.elems = elems
        self.action = action

        self.update()

    
    def update(self):
        """Update the rectangle of the union."""

        self.rect = self.elems[0].rect
        for element in self.elems[1:]:
            self.rect = pygame.Rect.union(self.rect, element.rect)

    def trigger(self):
        """Hook for doing something when the element is activated."""

        if self.action is None:
            return False
        
        self.action()
        return True
    
    def draw(self):
        """Hook for drawing the union. Does nothing currently."""

        # does nothing; exists so the code does not break
        # may have some other functional use in the future
        return

class Menu():
    """A base class representing a menu."""

    def __init__(self, game, name, width=None, height=None,background=None):
        """Initialize the menu."""

        self.game = game
        self.name = name
        self.visible = False # determines if menu is shown

        self.inner_pos = None # inner coordinates where the user clicked
        self.scrolled = False

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
    
    def _populate_values(self):
        """A hook for populating the menu with UI Elements."""

        # this is just a hook to be overwritten by child classes
        pass
    
    def update(self, element_name=None, content=None, symbol=None,
               symbol_is_left=None, position=None, anchor=None, font=None):
        """Re-renders the menu with current values."""

        # TODO: is this needed anymore???
        if element_name is not None and content is not None:
            self.elements[element_name].update(
                content, symbol, symbol_is_left, position, anchor, font
            )

        self._populate_values()

        # update the height and surface if elements are below view
        height = self.rect.height
        for element in self.elements.values():
            el_bottom = element.rect.y + element.rect.height
            height = el_bottom if el_bottom > height else height
        self.surface = pygame.Surface((self.rect.width, height))
        prev_pos = self.rect.x, self.rect.y
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = prev_pos
        self.surface.blit(self.background, self.background.get_rect())

        for element in self.elements.values():
            element.draw()
        
        # TODO: decide if you do NOT want to immediately draw the menu
        self.draw()
    
    def open(self):
        """Make the menu visible and interactive."""

        if self.visible:
            return False

        for menu in self.game.menus.values():
            menu.close()

        self.visible = True
        self.update()

    def close(self, next_menu=None):
        """Make the menu hidden and non-interactive."""

        if not self.visible:
            return False

        self.visible = False

        if next_menu:
            self.game.menus[next_menu].open()
    
    def start_touch(self, position):
        """Register a touch on the menu."""

        if not self.visible:
            return False

        self.inner_pos = (
            position[0] - self.rect.x,
            position[1] - self.rect.y
        )
        self.scrolled = False
    
    def interact(self):
        """
        Triggers any elements touched/ clicked if the menu is in focus.
        Can be called on touch/ mouse down or up.
        """

        if not self.visible:
            return False
        
        if self.scrolled:
            return False
        
        if not self.inner_pos:
            return False
        
        done = False
        for element in self.elements.values():
            if element.rect.collidepoint(self.inner_pos):
                if element.action is None:
                    continue
                element.trigger()
                done = True
                break
        return done
    
    def end_touch(self):
        """Stop registering the touch/ mouse on the menu."""

        self.inner_pos = None
    
    def scroll(self, position):
        """Scroll the menu."""

        if not self.visible:
            return False

        if not self.inner_pos:
            return False


        destination = position[1] - self.inner_pos[1]

        if self.rect.y == destination:
            return False
        
        top_limit = 0
        bottom_limit = self.game.screen.height - self.rect.height

        self.rect.y = destination
        self.scrolled = True

        if self.rect.y > top_limit:
            self.rect.y = top_limit      
        elif self.rect.y < bottom_limit:
            self.rect.y = bottom_limit
        
        self.draw()
        return True
        
    def draw(self):
        """Draw the menu to the screen."""

        if not self.visible:
            return False
        
        self.game.screen.blit(self.surface, self.rect)

class Tray(Menu):
    """A base class for the top and bottom trays."""

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the tray with a surface."""

        super().__init__(game, name, width, height, background)

        pygame.draw.rect(self.background, "white", self.background.get_rect())

        self.visible = True
