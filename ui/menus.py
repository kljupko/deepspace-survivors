"""A module containing all the menus in the game."""

import pygame
from .base import UIElement, ElemUnion, Menu

class MainMenu(Menu):
    """A class which represents the game's main menu."""

    def __init__(self, game, name="main",
                 width=None, height=None, background=None):
        """Initialize the main menu."""

        super().__init__(game, name, width, height, background)

        self.visible = True
        self.update()
    
    def _populate_values(self):
        """Populate menu with UI Elements."""

        el_name = "play_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Play", position=(
                self.rect.width * 1/3,
                self.rect.height * 1/3
            ), action=self.game.start_session
        )
        el_name = "upgrade_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Upgrade", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 1
            )
        )
        el_name = "unlock_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Unlock",position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 2
            )
        )
        el_name = "settings_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Settings", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 3
            ), action=lambda: self.game.menus["settings"].open()
        )
        el_name = "info_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Info", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 4
            )
        )
        el_name = "quit_btn"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Quit", position=(
                self.rect.width * 1/3,
                self.elements["play_btn"].rect.y +
                (self.elements["play_btn"].rect.height + 5) * 5
            ), action=self.game.quit
        )

class SettingsMenu(Menu):
    """A class representing the game's settings menu."""

    def __init__(self, game, name="settings",
                 width=None, height=None, background=None):
        """Initialize the settings menu."""

        super().__init__(game, name, width, height, background)
        
        self.update()
    
    def _populate_values(self):
        """Populate the menu with the values from the settings."""

        data = self.game.settings.data

        # the touple of touples below is used to generate the elements
        # element name, display name, height increment, action
        y_pos = 0
        element_data = (
            ("back_button", "< BACK", 1, lambda: self.close("main")),

            ("fps_label", "Target FPS", 22, None),
            ("fps_value", str(data['fps']), 0, None),
            ("show_fps_label", "Show FPS", 11, None),
            ("show_fps_value", str(data['show_fps']), 0, None),

            ("keybinds_header", "Keybinds", 22, None),
            ("key_confirm_label", "Confirm", 22, None),
            ("key_confirm_value", pygame.key.name(data['key_confirm']), 0, None),
            ("key_cancel_label", "Cancel", 11, None),
            ("key_cancel_value", pygame.key.name(data['key_cancel']), 0, None),

            ("key_move_left_label", "Move Left", 11, None),
            ("key_move_left_value", pygame.key.name(data['key_move_left']), 0, None),
            ("key_move_right_label", "Move Right", 11, None),
            ("key_move_right_value", pygame.key.name(data['key_move_right']), 0, None),
            ("key_fire_label", "Fire", 11, None),
            ("key_fire_value", pygame.key.name(data['key_fire']), 0, None),

            ("key_active_1_label", "On/Off Active 1", 11, None),
            ("key_active_1_value", pygame.key.name(data['key_active_1']), 0, None),
            ("key_active_2_label", "On/Off Active 2", 11, None),
            ("key_active_2_value", pygame.key.name(data['key_active_2']), 0, None),
            ("key_active_3_label", "On/Off Active 3", 11, None),
            ("key_active_3_value", pygame.key.name(data['key_active_3']), 0, None),

            ("key_passive_1_label", "On/Off Passive 1", 11, None),
            ("key_passive_1_value", pygame.key.name(data['key_passive_1']), 0, None),
            ("key_passive_2_label", "On/Off Passive 2", 11, None),
            ("key_passive_2_value", pygame.key.name(data['key_passive_2']), 0, None),
            ("key_passive_3_label", "On/Off Passive 3", 11, None),
            ("key_passive_3_value", pygame.key.name(data['key_passive_3']), 0, None),
            ("key_passive_4_label", "On/Off Passive 4", 11, None),
            ("key_passive_4_value", pygame.key.name(data['key_passive_4']), 0, None),

            ("restore_defaults", "Restore Defaults", 22, self._trigger_restore_defaults)
        )

        for element in element_data:
            name = element[0]
            content = element[1]
            height_increment = element[2]
            y_pos += height_increment
            action = element[3]

            anchor = "topleft" # label, left aligned
            x_pos = self.rect.width // 10
            if height_increment == 0:
                anchor = "topright" # value, right aligned
                x_pos = self.rect.width // 10 * 9

            self.elements[name] = UIElement(
                self.game, name, self.surface, content, False,
                position=(x_pos, y_pos),
                anchor=anchor, action=action
            )

        # the touple of touples below is used to generate the unions
        # keybinding/ union name, action
        union_data = (
            ("fps", self._cycle_framerates),
            ("show_fps", self._toggle_fps_display)
        )

        for union in union_data:
            name = union[0]
            label_name = name + "_label"
            value_name = name + "_value"
            action = union[1]

            self.elements[name] = ElemUnion(
                self.game, name,
                self.elements[label_name], self.elements[value_name],
                action=action
            )

        # similar to above, but for keybinds
        # keybinding/ union name, control name
        union_data = (
            ("key_confirm", "Confirm"),
            ("key_cancel", "Cancel"),
            ("key_move_left", "Move Left"),
            ("key_move_right", "Move Right"),
            ("key_fire", "Fire"),
            ("key_active_1", "Toggle Active 1"),
            ("key_active_2","Toggle Active 2"),
            ("key_active_3","Toggle Active 3"),
            ("key_passive_1","Toggle Passive 1"),
            ("key_passive_2","Toggle Passive 2"),
            ("key_passive_3","Toggle Passive 3"),
            ("key_passive_4","Toggle Passive 4") 
        )

        for union in union_data:
            name = union[0]
            label_name = name + "_label"
            value_name = name + "_value"
            control_name = union[1]
            action = (lambda cn=control_name, kbn=name:
                      self.game.menus['remap'].open(cn, kbn))

            self.elements[name] = ElemUnion(
                self.game, name,
                self.elements[label_name], self.elements[value_name],
                action=action
            )
    
    def _trigger_restore_defaults(self):
        """Restore default settings and rewrite the menu."""

        self.game.settings.restore_to_defaults()
        self.game.settings.save_data()
        self.update()
    
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
        self.game.settings.save_data()
        self.update()
    
    def _toggle_fps_display(self):
        """Switch between showing and hiding the framerate."""

        data = self.game.settings.data

        data['show_fps'] = not data['show_fps']
        self.game.settings.save_data()
        self.update()
    
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

        self.text = "Press a key to..."
        self.text += f'\nremap "{self.control}"'
        self.text += f"\ncurrently: {key_name}"

        self.elements = {}
        el_name = "prompt"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self.text, False,
            position=(self.rect.width // 2, self.rect.height // 2),
            anchor="center"
        )
        self.update()
        return super().open()
    
    def listen_for_key(self, key):
        """Listen for a keypress and remap the key."""

        if not self.visible:
            return False
        
        self.game.settings.data[self.keybind] = key
        self.game.menus['settings'].update()
        self.game.settings.save_data()
        self.close(next_menu="settings")
