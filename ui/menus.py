"""A module containing all the menus in the game."""

import pygame
from .base import *

class MainMenu(Menu):
    """A class which represents the game's main menu."""

    def __init__(self, game, name="main", background=None):
        """Initialize the main menu."""

        super().__init__(game, name, background)
        self._load_elements()
    
    def _load_elements(self):
        """Populate menu with UI Elements."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'play_btn',
                'content': 'Play',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 0,
                'anchor': None,
                'action': self.game.start_session
            }, {
                'type': 'label',
                'name': 'upgrade_btn',
                'content': 'Upgrade',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 11,
                'anchor': None,
                'action': lambda: self.game.menus['upgrade'].open()
            }, {
                'type': 'label',
                'name': 'unlock_btn',
                'content': 'Unlock',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 11,
                'anchor': None,
                'action': lambda: self.game.menus['unlock'].open()
            }, {
                'type': 'label',
                'name': 'settings_btn',
                'content': 'Settings',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 11,
                'anchor': None,
                'action': lambda: self.game.menus['settings'].open()
            }, {
                'type': 'label',
                'name': 'info_btn',
                'content': 'Info',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 11,
                'anchor': None,
                'action': lambda: self.game.menus['info'].open()
            }, {
                'type': 'label',
                'name': 'quit_btn',
                'content': 'Quit',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 11,
                'anchor': None,
                'action': self.game.quit
            },
        )

        self._add_elements_from_dicts(element_dicts)

class UpgradeMenu(Menu):
    """A class representing the upgrade menu."""

    def __init__(self, game, name="upgrade", background=None):
        """Initialize the upgrade menu."""

        super().__init__(game, name, background)
        self._load_elements()
    
    def _load_elements(self):
        """Populate the menu with upgrades."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 0,
                'anchor': None,
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Upgrades',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 22,
                'anchor': None,
                'action': None
            },
        )

        self._add_elements_from_dicts(element_dicts)

class UnlockMenu(Menu):
    """A class representing the unlock menu."""

    def __init__(self, game, name="unlock", background=None):
        """Initialize the unlock menu."""

        super().__init__(game, name, background)
        self._load_elements()
    
    def _load_elements(self):
        """Populate the menu with unlockables."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 0,
                'anchor': None,
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Unlocks',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 22,
                'anchor': None,
                'action': None
            },
        )

        self._add_elements_from_dicts(element_dicts)

class SettingsMenu(Menu):
    """A class representing the game's settings menu."""

    def __init__(self, game, name="settings",
                 width=None, height=None, background=None):
        """Initialize the settings menu."""

        super().__init__(game, name, width, height, background)
        
        self._load_elements()
    
    def _load_elements(self):
        """Populate the menu with the values from the settings."""

        data = self.game.settings.data

        
        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 0,
                'anchor': None,
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Upgrades',
                'font': None, 'wraplen': 0,
                'x_offset': 0, 'y_offset': 22,
                'anchor': None,
                'action': None
            },
        )

        self._add_elements_from_dicts(element_dicts)
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

            ("audio_header", "Audio", 22, None),
            ("music_vol_label", "Music Volume", 22, None),
            ("music_vol_value", str(data['music_volume']), 0, None),

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
                self.game, name, self, content, False,
                position=(x_pos, y_pos),
                anchor=anchor, action=action
            )

        # the touple of touples below is used to generate the unions
        # keybinding/ union name, action
        union_data = (
            ("fps", self._cycle_framerates),
            ("show_fps", self._toggle_fps_display),
            ("music_vol", self._cycle_music_volume)
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

    def _cycle_music_volume(self):
        """Cycle through available music volume."""

        id = 0
        n_options = len(self.game.config.music_volumes)
        for i in range(n_options):
            volume = self.game.config.music_volumes[i]
            if self.game.settings.data['music_volume'] == volume:
                id = i
                break

        next_id = (n_options + id + 1) % n_options
        next_volume = self.game.config.music_volumes[next_id]
        self.game.settings.data['music_volume'] = next_volume
        self.game.music_player.set_volume()
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
            self.game, el_name, self, self.text, False,
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

class InfoMenu(Menu):
    """A class representing the info page/ menu."""

    def __init__(self, game, name="info",
                 width=None, height=None, background=None):
        """Initialize the info menu."""

        super().__init__(game, name, width, height, background)

        self.update()
    
    def _load_elements(self):
        """Populate the menu with information."""

        y_pos = 0
        element_data = (
            ("back_btn", "< BACK", 1, lambda: self.close("main")),
            ("about", "Created by @kljupko in Pygame as a demo project",
             22, None),
        )

        for element in element_data:
            name = element[0]
            content = element[1]
            height_increment = element[2]
            y_pos += height_increment
            action = element[3]

            anchor = "topleft"
            x_pos = self.rect.width // 10

            self.elements[name] = UIElement(
                self.game, name, self, content, False,
                position=(x_pos, y_pos),
                anchor=anchor, action=action
            )   

class PauseMenu(Menu):
    """A class representing the game's pause menu."""

    def __init__(self, game, name='pause',
                 width=None, height=None, background=None):
        """Initialize the pause menu."""

        super().__init__(game, name, width, height, background)
        self.update()
    
    def _load_elements(self):
        """Populate the menu with buttons."""
       
        y_pos_adjustment = -11
        element_data = (
            ("continue_button", "Continue", 0, self._continue_session),
            ("restart_button", "Restart", 11, self._restart_session),
            ("quit_button", "Quit to Main Menu", 11, self.game.quit_session)
        )

        self.elements = {}
        for data in element_data:
            name = data[0]
            text = data[1]
            y_pos_adjustment += data[2]
            action = data[3]

            self.elements[name] = UIElement(
                self.game, name, self, text, position=(
                    self.rect.width // 10,
                    self.rect.height // 2 + y_pos_adjustment
                ), action=action
            )

    def open(self):
        """Pause the game and open the menu."""

        self.game.state.session_running = False
        self.game.music_player.pause()
        return super().open()

    def _continue_session(self):
        """Close the menu and continue the session."""

        self.game.state.session_running = True
        self.game.state.last_session_tick = pygame.time.get_ticks()
        self.close()
        # draw the bottom tray just to overwrite the part of the menu
        self.game.bot_tray.draw()
        self.game.music_player.unpause()
    
    def _restart_session(self):
        """Close the menu and restart the session."""

        self.game.quit_session()
        self.game.start_session()
        self.close()
