"""A module containing the base classes for the User Interface."""

import pygame

from ..systems import config, helper_funcs

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(self, container, name, content=None, position=(0, 0),
                 anchor="topleft", action=None):
        """Initialize the UI element."""

        self.container = container
        self.game = self.container.game
        self.name = name
        self.content = content

        self.anchor_pos = position
        self.anchor = anchor
        self._set_rect()
        self._set_rect_position()

        self.content = content
        self.action = action

        self.container.elements[self.name] = self # does this work?
    
    def _set_rect(self):
        """Set the rect for the UI Element based on the content."""

        self.rect = self.content.get_rect()
    
    def _set_rect_position(self):
        """
        Calculate the position at which the UI element will be drawn,
        based on the anchor.
        """

        draw_x = self.anchor_pos[0]
        if self.anchor in ["midtop", "center", "midbottom"]:
            draw_x -= self.rect.width // 2
        elif self.anchor in ["topright", "midright", "bottomright"]:
            draw_x -= self.rect.width
        
        draw_y = self.anchor_pos[1]
        if self.anchor in ["midleft", "center", "midright"]:
            draw_y -= self.rect.height // 2
        elif self.anchor in ["bottomleft", "midbottom", "bottomright"]:
            draw_y -= self.rect.height
        
        self.rect.x = draw_x
        self.rect.y = draw_y
    
    def trigger(self):
        """Hook for doing something when the element is activated."""

        if self.action is None:
            return False
        
        self.action()
        return True
    
    def draw(self):
        """Draw the element to the container surface."""

        self.container.surface.blit(self.content, self.rect)

class Icon(UIElement):
    """A class representing an icon in the UI."""

    def __init__(self, container, name, content=None, position=(0, 0),
                 anchor="topleft", action=None):
        """Initialize the icon."""

        content = helper_funcs.load_image(content, "pink", (10, 10))
        super().__init__(container, name, content, position, anchor, action)

class TextBox(UIElement):
    """A class representing a text box, with text wrapping."""

    def __init__(self, container, name, content, font=None, wraplength=None,
                 position=(0, 0), anchor="topleft", action=None):
        """Initialize the text box."""

        if font is None:
            font = config.font_normal
        
        if wraplength is None:
            wraplength = container.rect.width - \
                container.padding['left'] - container.padding['right']
        
        content = font.render(
            str(content), False, 'white', 'black', wraplength
        )
        
        super().__init__(container, name, content, position, anchor, action)

class Label(TextBox):
    """A class representing a label, with no text wrap."""

    def __init__(self, container, name, content, font=None, wraplength=0,
                 position=(0, 0), anchor="topleft", action=None):
        """Initialize the label."""

        super().__init__(container, name, content, font, wraplength, position, anchor, action)

class ElemUnion():
    """A class representing a union of multiple UI Elements."""

    def __init__(self, container, name, *elems, action=None):
        """Initialize the union."""

        self.name = name
        self.container = container
        self.game = self.container.game
        self.elems = elems
        self.action = action

        self._unify_elements()

        self.container.elements[self.name] = self

    
    def _unify_elements(self):
        """Create the rectangle around the elements."""

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

    def __init__(self, game, name, background=None,
                 width=None, height=None, padding=None):
        """Initialize the menu."""

        self.game = game
        self.name = name
        self.is_visible = False # determines if menu is shown

        self.inner_pos = None # inner coordinates where the user clicked
        self.was_scrolled = False
        self.needs_redraw = True

        self._set_surface(width, height)
        if padding is None:
            padding = (10, 10, 10, 10)
        self._set_padding(padding)
        self._set_background(background)

        self.elements = {}
        self._load_elements()
    
    def _set_surface(self, width=None, height=None):
        """Set the surface for menu and derive the size."""

        if width is None:
            width = self.game.screen.width
        if height is None:
            height = self.game.screen.height
        
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        ck = config.global_colorkey
        self.surface.set_colorkey(ck)
        pygame.draw.rect(self.surface, ck, self.rect)

    def _set_padding(self, padding=None):
        """Sets the padding for the menu: (top, bottom, left, right)."""

        if padding is None:
            padding = (0, 0, 0, 0)

        self.padding = {
            'top': padding[0], 'bottom': padding[1],
            'left': padding[2], 'right': padding[3]
        }
    
    def _set_background(self, background=None):
        """Set the background for the menu."""

        if background is None:
            background = pygame.Surface((self.rect.width, self.rect.height))
            pygame.draw.rect(background, 'aquamarine', background.get_rect())
        # TODO: otherwise, load the background image
        self.background = background

    def _load_elements(self):
        """A hook for populating the menu with UI Elements."""

        # this is just a hook to be overwritten by child classes
        pass
    
    def _add_elements_from_dicts(self, dicts, x_incremental=False, x_origin=0,
                                 y_incremental=True, y_origin=0):
        """
        To be used in _load_elements.
        Takes a sequence of dictionaries containing element data, and
        adds the elements to the menu according to the data provided.
        """

        x_pos = x_origin
        y_pos = y_origin

        for d in dicts:
            x = d['x']
            y = d['y']

            if x_incremental:
                x_pos += x
                x = x_pos
            if y_incremental:
                y_pos += y
                y = y_pos
            
            # adjust for padding
            x += self.padding['left']
            y += self.padding['top']
            right_limit = self.rect.width - self.padding['right']
            x = right_limit if x > right_limit else x

            if d['type'] == 'label':
                el = Label(
                    self, d['name'], d['content'], d['font'],
                    0, (x, y), d['anchor'], d['action']
                )
            elif d['type'] == 'icon':
                el = Icon(
                    self, d['name'], d['content'],
                    (x, y), d['anchor'], d['action']
                )
            elif d['type'] == 'textbox':
                el = TextBox(
                    self, d['name'], d['content'], d['font'],
                    d['wraplen'], (x, y), d['anchor'], d['action']
                )

    def _add_element_unions_from_dicts(self, dicts):
        """
        To be used in _load_elemets.
        Takes a sequence of dictionaries containing union data, and adds
        the unions to the menu according to the data provided.
        """

        for d in dicts:
            elems = []
            for name in d['elem_names']:
                elems.append(self.elements[name])
            
            u = ElemUnion(self, d['name'], *elems, action=d['action'])

    def _expand_height(self):
        """
        To be used in _load_elements.
        Expands the rect height to include all elements + bottom padding.
        """
        
        width, height = self.rect.width, self.rect.height
        pos_x, pos_y = self.rect.x, self.rect.y

        bottom = 0
        for element in self.elements.values():
            el_bottom = element.rect.y + element.rect.height
            bottom = el_bottom if el_bottom > bottom else bottom
        
        lowest = bottom + self.padding['bottom']
        height = lowest if lowest > height else height

        self._set_surface(width, height)
        self.rect.x, self.rect.y = pos_x, pos_y

    def update(self):
        """Re-renders the menu with current values."""

        self._load_elements()        
        self.needs_redraw = True
    
    def open(self):
        """Make the menu visible and interactive."""

        if self.is_visible:
            return False

        for menu in self.game.menus.values():
            menu.close()

        self.is_visible = True
        self.update() # TODO: remove this?

    def close(self, next_menu=None):
        """Make the menu hidden and non-interactive."""

        if not self.is_visible:
            return False

        self.is_visible = False

        if next_menu:
            self.game.menus[next_menu].open()
    
    def start_touch(self, position):
        """Register a touch on the menu."""

        if not self.is_visible:
            return False

        self.inner_pos = (
            position[0] - self.rect.x,
            position[1] - self.rect.y
        )
        self.was_scrolled = False
    
    def interact(self):
        """
        Triggers any elements touched/ clicked if the menu is in focus.
        Can be called on touch/ mouse down or up.
        """

        if not self.is_visible:
            return False
        
        if self.was_scrolled:
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
    
    def scroll(self, position, is_mousewheel_scroll=False):
        """Scroll the menu."""

        if not self.is_visible:
            return False

        if self.inner_pos:
            # scrolling via mouse/ finger drag
            destination = position[1] - self.inner_pos[1]
        elif is_mousewheel_scroll:
            # scrolling via mouse wheel
            destination = self.rect.y + position[1]
        else:
            # not scrolling
            return False

        if self.rect.y == destination:
            return False
        
        top_limit = 0
        bottom_limit = self.game.screen.height - self.rect.height

        self.rect.y = destination
        self.was_scrolled = True

        if self.rect.y > top_limit:
            self.rect.y = top_limit      
        elif self.rect.y < bottom_limit:
            self.rect.y = bottom_limit
        
        self.needs_redraw = True
        return True
        
    def draw(self):
        """Draw the menu to the screen."""

        if not self.is_visible or not self.needs_redraw:
            return False
        
        if self.rect.height > self.game.screen.height:
            top = 0
        else:
            top = self.rect.y
        
        back_draw_rect = pygame.Rect(
            self.rect.x, top,
            self.background.width, self.background.height
        )

        if self.name in ["top_tray", "bot_tray"]:
            # draw background to tray so it's visible on play_surf
            self.surface.blit(self.background, self.rect)
        
        self.game.screen.blit(self.background, back_draw_rect)
        for element in self.elements.values():
            element.draw()
        self.game.screen.blit(self.surface, self.rect)

        self.needs_redraw = False

class Tray(Menu):
    """A base class for the top and bottom trays."""

    def __init__(self, game, name,background=None,
                 width=None, height=None, padding=None):
        """Initialize the tray with a surface."""

        if width is None:
            width = game.play_surf.width

        if background is None:
            background = pygame.Surface((width, height))
            pygame.draw.rect(background, 'white', background.get_rect())
        
        if padding is None:
            padding = (1, 1, 1, 1)

        super().__init__(game, name, background, width, height, padding)
        self.is_visible = True
