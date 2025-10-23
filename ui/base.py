"""A module containing the base classes for the User Interface."""

import pygame

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(self, container, name, content=None, position=(0, 0),
                 anchor="topleft", action=None):
        """Initialize the UI element."""

        self.container = container
        self.game = self.container.game
        self.name = name
        self.content = content

        self.initial_position = position
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

        draw_x = self.initial_position[0]
        if self.anchor in ["midtop", "center", "midbottom"]:
            draw_x -= self.rect.width // 2
        elif self.anchor in ["topright", "midright", "bottomright"]:
            draw_x -= self.rect.width
        
        draw_y = self.initial_position[1]
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

        content = self._process_image(content)
        super().__init__(container, name, content, position, anchor, action)
    
    def _process_image(self, image):
        """Process the image provided to be set as the Icon's content."""

        if image is None:
            image = pygame.Surface((10, 10))
            pygame.draw.rect(image, "pink", (0, 0, 10, 10))
        elif image is False:
            # image will be an empty surface with a size of 0
            image = pygame.Surface((0, 0))
        else:
            # TODO: load the image of the icon
            pass

        return image

class TextBox(UIElement):
    """A class representing a text box, with text wrapping."""

    def __init__(self, container, name, content, font=None, wraplength=None,
                 position=(0, 0), anchor="topleft", action=None):
        """Initialize the text box."""

        if font is None:
            font = container.game.config.font_normal
        
        if wraplength is None:
            wraplength = container.rect.width - container.padding['right']
        
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

    def __init__(self, game, name, background=None):
        """Initialize the menu."""

        self.game = game
        self.name = name
        self.is_visible = False # determines if menu is shown

        self.inner_pos = None # inner coordinates where the user clicked
        self.was_scrolled = False
        self.needs_redraw = True

        width = self.game.screen.width
        height = self.game.screen.height

        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.padding = {'top': 10, 'bottom': 10, 'left': 10, 'right': 10}

        if background is None:
            background = pygame.Surface((width, height))
            pygame.draw.rect(background, "black", background.get_rect())
        self.background = background

        self.elements = {}
    
    def _load_elements(self):
        """A hook for populating the menu with UI Elements."""

        # this is just a hook to be overwritten by child classes
        pass
    
    def _add_elements_from_dicts(self, dicts,
                                      x_origin=None, y_origin=None):
        """
        To be used in _load_elements.
        Takes a sequence of dictionaries containing element data, and
        adds the elements to the menu according to the data provided.
        """

        if x_origin is None:
            x_origin = self.padding['left']
        if y_origin is None:
            y_origin = self.padding['top']
        x_pos = x_origin
        y_pos = y_origin

        for d in dicts:
            x = x_pos + d['x_offset']
            y_pos += d['y_offset']
            y = y_pos

            if d['type'] == 'label':
                el = Label(self, d['name'], d['content'], d['font'],
                           0, (x, y), d['anchor'], d['action'])
            elif d['type'] == 'icon':
                el = Icon(self, d['name'], d['content'],
                          (x, y), d['anchor'], d['action'])
            elif d['type'] == 'textbox':
                el = TextBox(self, d['name'], d['content'], d['font'],
                           d['wraplen'], (x, y), d['anchor'], d['action'])

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

    def update(self):
        """Re-renders the menu with current values."""

        self._load_elements()

        # update the height and surface if elements are below view
        # TODO: organize this better
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
    
    def scroll(self, position):
        """Scroll the menu."""

        if not self.is_visible:
            return False

        if not self.inner_pos:
            return False


        destination = position[1] - self.inner_pos[1]

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
        
        self.game.screen.blit(self.surface, self.rect)
        self.needs_redraw = False

class Tray(Menu):
    """A base class for the top and bottom trays."""

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the tray with a surface."""

        super().__init__(game, name, width, height, background)

        pygame.draw.rect(self.background, "white", self.background.get_rect())

        self.is_visible = True
