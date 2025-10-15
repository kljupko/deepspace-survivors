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
    
    def open(self):
        """Make the menu visible and interactive."""

        if self.visible:
            return False

        for menu in self.game.menus.values():
            menu.close()

        self.visible = True

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
        
        if self.rect.height <= self.game.screen.height:
            return False

        destination = position[1] - self.inner_pos[1]
        top_limit = 0
        bottom_limit = self.game.screen.height - self.rect.height

        self.rect.y = destination
        self.scrolled = True

        if self.rect.y > top_limit:
            self.rect.y = top_limit
            return True
        
        if self.rect.y < bottom_limit:
            self.rect.y = bottom_limit
            return True
        
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

    def __init__(self, game, name="main_menu",
                 width=None, height=None, background=None):
        """Initialize the main menu."""

        super().__init__(game, name, width, height, background)

        self.visible = True

        el_name = "play_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Play", position=(
                self.rect.width * 1/3,
                self.rect.height * 1/3
            ), anchor="topleft", action=self.game.start_session
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
            ), anchor="topleft", action=self.game.menus["settings_menu"].open
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
            ), anchor="topleft", action=self.game.quit
        )

class SettingsMenu(Menu):
    """A class representing the game's settings menu."""

    def __init__(self, game, name="settings_menu",
                 width=None, height=None, background=None):
        """Initialize the settings menu."""

        super().__init__(game, name, width, height, background)                
    
    def _populate_values(self):
        """Populate the menu with the values from the settings."""

        data = self.game.settings.data

        # TODO: find a way to do this programatically,
        # with the same amount of control

        el_name = "back_button"
        height = 1
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "< BACK",
            position=(self.rect.width // 2, height), anchor="midtop",
            action=self.close
        )

        el_name = "fps_label"
        height += 22
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "FPS Target", False,
            position=(self.rect.width // 10, height),
            action=self._cycle_framerates
        )
        el_name = "fps_value"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, str(data['fps']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "keybinds_header"
        height += 22
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Keybinds", False,
            position=(self.rect.width // 10, height),
            font=self.game.config.font_large
        )

        el_name = "key_confirm_label"
        height += 22
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Confirm", False,
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Confirm", "key_confirm")
        )
        el_name = "key_confirm"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_confirm']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_cancel_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Cancel", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_cancel"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_cancel']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_move_left_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Move Left", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_move_left"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_move_left']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_move_right_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Move Right", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_move_right"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_move_right']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_fire_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Fire", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_fire"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_fire']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_active_1_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Active 1", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_active_1"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_active_1']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_active_2_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Active 2", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_active_2"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_active_2']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_active_3_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Active 3", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_active_3"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_active_3']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_passive_1_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Passive 1", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_passive_1"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_passive_1']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_passive_2_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Passive 2", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_passive_2"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_passive_2']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_passive_3_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Passive 3", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_passive_3"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_passive_3']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "key_passive_4_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "On/Off Passive 4", False,
            position=(self.rect.width // 10, height)
        )
        el_name = "key_passive_4"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            pygame.key.name(data['key_passive_4']), False,
            position=(self.rect.width // 10*9, height), anchor="topright"
        )

        el_name = "default"
        height += 22
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Default",
            position=(self.rect.width // 2, height), anchor="midtop",
            action=self._trigger_restore_defaults
        )
    
    def open(self):
        self._populate_values()
        return super().open()

    def close(self, next_menu="main_menu"):
        return super().close(next_menu)
    
    def _trigger_restore_defaults(self):
        """Restore default settings and rewrite the menu."""

        self.game.settings.restore_to_defaults()
        self._populate_values()
    
    def _cycle_framerates(self):
        """Cycle through available framerates."""

        id = 0
        n_options = len(self.game.config.framerates)
        for i in range(n_options):
            framerate = self.game.config.framerates[i]
            if self.game.settings.data['fps'] == framerate:
                id = i
                break

        next_id = (n_options + id + 1) % n_options
        next_framerate = self.game.config.framerates[next_id]
        self.game.settings.data['fps'] = next_framerate

        self._populate_values()
    
class RemapKeyMenu(Menu):
    """A class representing the key remapping prompt."""

    def __init__(self, game, name="remap",
                 width=None, height=None, background=None):
        """Initialize the key remapping menu."""

        super().__init__(game, name, width, height, background)

        self.keybind = None
        self.control = None
        self.text = None
    
    def open(self, control, keybind):
        """Show the menu with the correct prompt."""

        self.control = control
        self.keybind = keybind
        key_name = pygame.key.name(self.game.settings.data[self.keybind])

        el_name = "prompt"
        self.text = "Press a key to..."
        self.text += f'\nremap "{self.control}"'
        self.text += f"\ncurrently: {key_name}"

        self.elements = {}
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self.text, False,
            position=(self.rect.width // 2, self.rect.height // 2),
            anchor="center"
        )

        return super().open()
    
    def listen_for_key(self, key):
        """Listen for a keypress and remap the key."""

        if not self.visible:
            return False
        
        self.game.settings.data[self.keybind] = key
        self.close(next_menu="settings_menu")

class Tray(Menu):
    """A base class for the top and bottom trays."""

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the tray with a surface."""

        super().__init__(game, name, width, height, background)

        pygame.draw.rect(self.background, "white", self.background.get_rect())

        self.visible = True


class TopTray(Tray):
    """A class representing the top tray."""

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the top tray."""

        super().__init__(game, name, width, height, background)
    
    def complete_init(self):
        """
        Completes the initialization.
        Called after the ship is initialized.
        """

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

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the bottom tray."""

        super().__init__(game, name, width, height, background)
        self.rect.y = self.game.screen.height - self.rect.height
    
    def complete_init(self):
        """
        Completes the initialization.
        Called after the ship is initialized.
        """

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