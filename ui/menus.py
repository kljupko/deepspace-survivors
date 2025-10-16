"""A module containing all the menus in the game."""

import pygame
from .base import UIElement, Menu

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

        # TODO: find a way to do this programatically,
        # with the same amount of control

        el_name = "back_button"
        height = 1
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "< BACK",
            position=(self.rect.width // 10, height),
            action=lambda: self.close("main")
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

        el_name = "show_fps_label"
        height += 11
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, "Show FPS", False,
            position=(self.rect.width // 10, height),
            action=self._toggle_fps_display
        )
        el_name = "show_fps_value"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, str(data['show_fps']), False,
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Cancel", "key_cancel")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Move Left", "key_move_left")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Move Right", "key_move_right")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Fire", "key_fire")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Active 1", "key_active_1")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Active 2", "key_active_2")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Active 3", "key_active_3")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Passive 1", "key_passive_1")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Passive 2", "key_passive_2")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Passive 3", "key_passive_3")
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
            position=(self.rect.width // 10, height),
            action=lambda : self.game.menus['remap'].open("Toggle Passive 4", "key_passive_4")
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
