"""A module containing the base classes for the User Interface."""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game
    from .menu_setups import ElementDict, UnionDict

import pygame

from ..utils import config, helper_funcs

class Menu():
    """A base class representing a menu."""

    def __init__(self,
                 game: Game,
                 name: str,
                 background: pygame.Surface | None = None,
                 width: int | None = None,
                 height: int | None = None,
                 padding: tuple[int, int, int, int] | None = None
                 ):
        """Initialize the menu."""

        self.game = game
        self.name = name
        self.is_visible = False # determines if menu is shown

        # inner coordinates where the user clicked
        self.inner_pos: tuple[int, int] | None = None
        self.was_scrolled = False
        self.needs_redraw = True

        self._set_surface(width, height)
        if padding is None:
            padding = (10, 10, 10, 10)
        self._set_padding(padding)
        self._set_background(background)

        self.elements: dict[str, UIElement | ElemUnion] = {}
        self._load_elements()
    
    def _set_surface(self,
                     width: int | None = None,
                     height: int | None = None
                     ):
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

    def _set_padding(self,
                     padding: tuple[int, int, int, int] | None = None
                     ):
        """Sets the padding for the menu: (top, bottom, left, right)."""

        if padding is None:
            padding = (0, 0, 0, 0)

        self.padding = {
            'top': padding[0], 'bottom': padding[1],
            'left': padding[2], 'right': padding[3]
        }
    
    def _set_background(self,
                        background: pygame.Surface | None = None
                        ):
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
    
    def _add_elements_from_dicts(self,
                                 dicts: list[ElementDict],
                                 origin: tuple[int, int] = (0, 0)
                                 ):
        """
        To be used in _load_elements.
        Takes a sequence of dictionaries containing element data, and
        adds the elements to the menu according to the data provided.
        """

        for element in dicts:
            el_type = element['type']
            name = element['name']
            content = element['content']

            font = element['font']
            wraplength = element['wraplength']

            x_offset = element['x_offset']
            y_offset = element['y_offset']
            x = origin[0] + x_offset
            y = origin[1] + y_offset

            # region POSITION ACCORDING TO LINKED ELEMENT
            # -----------------------------------------------------------

            linked_elem_name = element['linked_to']
            if linked_elem_name:
                linked_to = self.elements.get(linked_elem_name, None)

                ignore_linked_x = element['ignore_linked_x']
                ignore_linked_y = element['ignore_linked_y']
                linked_anchor = element['linked_anchor']

                if linked_to and not ignore_linked_x:
                    x = linked_to.rect.x + x_offset
                    # adjust x to anchor point in linked element
                    if linked_anchor in ["midtop", "center", "midbottom"]:
                        x += linked_to.rect.width // 2
                    elif linked_anchor in ["topright", "midright", "bottomright"]:
                        x += linked_to.rect.width
                
                if linked_to and not ignore_linked_y:
                    y = linked_to.rect.y + y_offset
                    # adjust y to anchor point in linked element
                    if linked_anchor in ["midleft", "center", "midright"]:
                        y += linked_to.rect.height // 2
                    elif linked_anchor in ["bottomleft", "midbottom", "bottomright"]:
                        y += linked_to.rect.height
                
            # -----------------------------------------------------------
            # endregion POSITION ACCORDING TO LINKED ELEMENT

            # adjust for padding
            left_limit = self.padding['left']
            right_limit = self.rect.width - self.padding['right']
            top_limit = self.padding['top']
            x = x if x > left_limit else left_limit
            x = x if x < right_limit else right_limit
            y = y if y > top_limit else top_limit

            anchor = element.get('anchor', None)
            action = element.get('action', None)

            if el_type == 'icon' and type(content) == pygame.Surface:
                Icon(
                    self, name, content, (x, y), anchor, action
                )
            elif el_type == 'label' and type(content) == str:
                Label(
                    self, name, content, font, 0, (x, y), anchor, action
                )
            elif el_type == 'textbox' and type(content) == str:
                TextBox(
                    self, name, content, font, wraplength, (x, y), anchor, action
                )
            else:
                print(f"Failed to add element{name}!")
                print("\tPerhaps the content or element type is invalid?")

    def _add_element_unions_from_dicts(self, dicts: list[UnionDict]):
        """
        To be used in _load_elemets.
        Takes a sequence of dictionaries containing union data, and adds
        the unions to the menu according to the data provided.
        """

        for d in dicts:
            elems: list[UIElement] = []
            for name in d['elem_names']:
                el = self.elements[name]
                if isinstance(el, UIElement):
                    elems.append(el)
            
            ElemUnion(self, d['name'], *elems, action=d['action'])

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
        self.update()

    def close(self,
              next_menu: str | None = None
              ):
        """Make the menu hidden and non-interactive."""

        if not self.is_visible:
            return

        self.is_visible = False

        if next_menu:
            self.game.menus[next_menu].open()
    
    def start_touch(self,
                    position: tuple[int, int]
                    ):
        """Register a touch on the menu."""

        if not self.is_visible:
            return

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
    
    def scroll(self,
               position: tuple[int, int],
               is_mousewheel_scroll: bool = False
               ):
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
        self.surface.blit(self.background, self.rect)
        self.game.screen.blit(self.background, back_draw_rect)

        from . import trays
        if self.name in [trays.TopTray.name, trays.BottomTray.name]:
            # draw background to tray so it's visible on play_surf
            self.surface.blit(self.background, self.background.get_rect())
        
        for element in self.elements.values():
            element.draw()
        self.game.screen.blit(self.surface, self.rect)

        self.needs_redraw = False

class Tray(Menu):
    """A base class for the top and bottom trays."""

    def __init__(self,
                 game: Game,
                 name: str,
                 background: pygame.Surface | None = None,
                 width: int | None = None,
                 height: int | None = None,
                 padding: tuple[int, int, int, int] | None = None
                 ):
        """Initialize the tray with a surface."""

        if width is None:
            width = game.play_surf.width
        
        if height is None:
            height = game.play_surf.height

        if background is None:
            background = pygame.Surface((width, height))
            pygame.draw.rect(background, 'white', background.get_rect())
        
        if padding is None:
            padding = (1, 1, 1, 1)

        super().__init__(game, name, background, width, height, padding)
        self.is_visible = True

class UIElement():
    """A class that represents a single element of the user interface."""

    def __init__(self,
                 container: Menu,
                 name: str,
                 content: pygame.Surface,
                 position: tuple[int, int] = (0, 0),
                 anchor: str = "topleft",
                 action: object | None = None
                 ):
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

        if not callable(self.action):
            return False
        
        self.action()
        return True
    
    def draw(self):
        """Draw the element to the container surface."""

        self.container.surface.blit(self.content, self.rect)

class Icon(UIElement):
    """A class representing an icon in the UI."""

    def __init__(self,
                 container: Menu,
                 name: str,
                 content: pygame.Surface | None = None,
                 position: tuple[int, int] = (0, 0),
                 anchor: str = "topleft",
                 action: object | None = None
                 ):
        """Initialize the icon."""

        if content is None:
            content = helper_funcs.load_image(content, "pink", (10, 10))
        super().__init__(container, name, content, position, anchor, action)

class TextBox(UIElement):
    """A class representing a text box, with text wrapping."""

    def __init__(self,
                 container: Menu,
                 name: str,
                 content: str,
                 font: pygame.Font | None = None,
                 wraplength: int | None = None,
                 position: tuple[int, int] = (0, 0),
                 anchor: str = "topleft",
                 action: object | None = None
                 ):
        """Initialize the text box."""

        if font is None:
            font = config.font_normal
        
        if wraplength is None:
            wraplength = container.rect.width - \
                container.padding['left'] - container.padding['right']
        
        rendered_content = font.render(
            str(content), False, 'white', 'black', wraplength
        )
        
        super().__init__(container, name, rendered_content, position, anchor, action)

class Label(TextBox):
    """A class representing a label, with no text wrap."""

    def __init__(self,
                 container: Menu,
                 name: str,
                 content: str,
                 font: pygame.Font | None = None,
                 wraplength: int = 0,
                 position: tuple[int, int] = (0, 0),
                 anchor: str = "topleft",
                 action: object | None = None
                 ):
        """Initialize the label."""

        super().__init__(container, name, content, font, wraplength, position, anchor, action)

class ElemUnion():
    """A class representing a union of multiple UI Elements."""

    def __init__(self,
                 container: Menu,
                 name: str,
                 *elems: UIElement,
                 action: object | None = None
                 ):
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

        if not callable(self.action):
            return False
        
        self.action()
        return True
    
    def draw(self):
        """Hook for drawing the union. Does nothing currently."""

        # does nothing; exists so the code does not break
        # may have some other functional use in the future
        return
