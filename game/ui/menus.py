"""A module containing all the menus in the game."""

import pygame

from .base import Menu, TextBox
from ..systems import config

class MainMenu(Menu):
    """A class which represents the game's main menu."""

    def __init__(self, game, name="main", background=None,
                 width=None, height=None, padding=None):
        """Initialize the main menu."""

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):
        """Populate menu with UI Elements."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'play_btn',
                'content': 'Play',
                'action': self.game.start_session
            }, {
                'type': 'label',
                'name': 'upgrade_btn',
                'content': 'Upgrade',
                'linked_to' : 'play_btn',
                'y_offset': 1,
                'action': lambda: self.game.menus['upgrade'].open()
            }, {
                'type': 'label',
                'name': 'achievements_btn',
                'content': 'Achievements',
                'linked_to' : 'upgrade_btn',
                'y_offset': 1,
                'action': lambda: self.game.menus['achievements'].open()
            }, {
                'type': 'label',
                'name': 'settings_btn',
                'content': 'Settings',
                'linked_to' : 'achievements_btn',
                'y_offset': 1,
                'action': lambda: self.game.menus['settings'].open()
            }, {
                'type': 'label',
                'name': 'info_btn',
                'content': 'Info',
                'linked_to' : 'settings_btn',
                'y_offset': 1,
                'action': lambda: self.game.menus['info'].open()
            }, {
                'type': 'label',
                'name': 'quit_btn',
                'content': 'Quit',
                'linked_to' : 'info_btn',
                'y_offset': 1,
                'action': self.game.quit
            },
        )

        self._add_elements_from_dicts(element_dicts)
        self._expand_height()

class UpgradeMenu(Menu):
    """A class representing the upgrade menu."""

    def __init__(self, game, name="upgrade", background=None,
                 width=None, height=None, padding=None):
        """Initialize the upgrade menu."""

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):
        """Populate the menu with upgrades."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Upgrades',
                'font': config.font_large,
                'x_offset' : self.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            },
        )

        self._add_elements_from_dicts(element_dicts)
        self._expand_height()

class AchievementsMenu(Menu):
    """A class representing the achievements menu."""

    def __init__(self, game, name="achievements", background=None,
                 width=None, height=None, padding=None):
        """Initialize the achievements menu."""

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):
        """Populate the menu with achievements."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Achievements',
                'font': config.font_large,
                'x_offset' : self.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            },
        )

        self._add_elements_from_dicts(element_dicts)
        self._expand_height()

class SettingsMenu(Menu):
    """A class representing the game's settings menu."""

    def __init__(self, game, name="settings", background=None,
                 width=None, height=None, padding=None):
        """Initialize the settings menu."""

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):
        """Populate the menu with the values from the settings."""

        data = self.game.settings.data
        
        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Settings',
                'font': config.font_large,
                'x_offset' : self.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'fps_label',
                'content': 'Target FPS',
                'linked_to': 'title',
                'ignore_linked_x': True,
                'y_offset': 7
            }, {
                'type': 'label',
                'name': 'fps_value',
                'content': data['fps'],
                'linked_to': 'fps_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'show_fps_label',
                'content': 'Show FPS',
                'linked_to': 'fps_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'show_fps_value',
                'content': data['show_fps'],
                'linked_to': 'show_fps_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'keybinds_header',
                'content': 'Keybinds',
                'linked_to': 'show_fps_label',
                'ignore_linked_x': True,
                'x_offset' : self.rect.width // 2,
                'y_offset': 7,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'key_confirm_label',
                'content': 'Confirm',
                'linked_to': 'keybinds_header',
                'x_offset': -self.rect.width,
                'y_offset': 3
            }, {
                'type': 'label',
                'name': 'key_confirm_value',
                'content': pygame.key.name(data['key_confirm']),
                'linked_to': 'key_confirm_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_cancel_label',
                'content': 'Cancel',
                'linked_to': 'key_confirm_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_cancel_value',
                'content': pygame.key.name(data['key_cancel']),
                'linked_to': 'key_cancel_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_move_left_label',
                'content': 'Move Left',
                'linked_to': 'key_cancel_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_move_left_value',
                'content': pygame.key.name(data['key_move_left']),
                'linked_to': 'key_move_left_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_move_right_label',
                'content': 'Move Right',
                'linked_to': 'key_move_left_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_move_right_value',
                'content': pygame.key.name(data['key_move_right']),
                'linked_to': 'key_move_right_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_fire_label',
                'content': 'Fire',
                'linked_to': 'key_move_right_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_fire_value',
                'content': pygame.key.name(data['key_fire']),
                'linked_to': 'key_fire_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_active_1_label',
                'content': 'Toggle Active 1',
                'linked_to': 'key_fire_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_active_1_value',
                'content': pygame.key.name(data['key_active_1']),
                'linked_to': 'key_active_1_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_active_2_label',
                'content': 'Toggle Active 2',
                'linked_to': 'key_active_1_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_active_2_value',
                'content': pygame.key.name(data['key_active_2']),
                'linked_to': 'key_active_2_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_active_3_label',
                'content': 'Toggle Active 3',
                'linked_to': 'key_active_2_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_active_3_value',
                'content': pygame.key.name(data['key_active_3']),
                'linked_to': 'key_active_3_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_passive_1_label',
                'content': 'Toggle Passive 1',
                'linked_to': 'key_active_3_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_passive_1_value',
                'content': pygame.key.name(data['key_passive_1']),
                'linked_to': 'key_passive_1_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_passive_2_label',
                'content': 'Toggle Passive 2',
                'linked_to': 'key_passive_1_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_passive_2_value',
                'content': pygame.key.name(data['key_passive_2']),
                'linked_to': 'key_passive_2_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_passive_3_label',
                'content': 'Toggle Passive 3',
                'linked_to': 'key_passive_2_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_passive_3_value',
                'content': pygame.key.name(data['key_passive_3']),
                'linked_to': 'key_passive_3_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'key_passive_4_label',
                'content': 'Toggle Passive 4',
                'linked_to': 'key_passive_3_label',
                'y_offset': 1
            }, {
                'type': 'label',
                'name': 'key_passive_4_value',
                'content': pygame.key.name(data['key_passive_4']),
                'linked_to': 'key_passive_4_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'audio_header',
                'content': 'Audio',
                'linked_to': 'key_passive_4_label',
                'ignore_linked_x': True,
                'x_offset' : self.rect.width // 2,
                'y_offset': 7,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'music_vol_label',
                'content': 'Music Volume',
                'linked_to': 'audio_header',
                'x_offset': -self.rect.width,
                'y_offset': 3
            }, {
                'type': 'label',
                'name': 'music_vol_value',
                'content': data['music_volume'],
                'linked_to': 'music_vol_label',
                'linked_anchor': 'topright',
                'x_offset': self.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'other_header',
                'content': 'Other',
                'linked_to': 'music_vol_label',
                'ignore_linked_x': True,
                'x_offset' : self.rect.width // 2,
                'y_offset': 7,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'restore_defaults_btn',
                'content': 'Restore Defaults',
                'linked_to': 'other_header',
                'ignore_linked_x': True,
                'y_offset': 3,
                'action': self._trigger_restore_defaults
            },
        )

        self._add_elements_from_dicts(element_dicts)

        union_dicts = (
            {
                'name': 'cycle_fps_btn',
                'elem_names': ['fps_label', 'fps_value'],
                'action': self._cycle_framerates
            },
            {
                'name': 'show_fps_btn',
                'elem_names': ['show_fps_label', 'show_fps_value'],
                'action': self._toggle_fps_display
            },
            {
                'name': 'remap_confirm_btn',
                'elem_names': ['key_confirm_label', 'key_confirm_value'],
                'action': (lambda: self.game.menus['remap'].open('Confirm', 'key_confirm'))
            },
            {
                'name': 'remap_cancel_btn',
                'elem_names': ['key_cancel_label', 'key_cancel_value'],
                'action': (lambda: self.game.menus['remap'].open('Cancel', 'key_cancel'))
            },
            {
                'name': 'remap_move_left_btn',
                'elem_names': ['key_move_left_label', 'key_move_left_value'],
                'action': (lambda: self.game.menus['remap'].open('Move Left', 'key_move_left'))
            },
            {
                'name': 'remap_move_right_btn',
                'elem_names': ['key_move_right_label', 'key_move_right_value'],
                'action': (lambda: self.game.menus['remap'].open('Move Right', 'key_move_right'))
            },
            {
                'name': 'remap_fire_btn',
                'elem_names': ['key_fire_label', 'key_fire_value'],
                'action': (lambda: self.game.menus['remap'].open('Fire', 'key_fire'))
            },
            {
                'name': 'remap_active_1_btn',
                'elem_names': ['key_active_1_label', 'key_active_1_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Active 1', 'key_active_1'))
            },
            {
                'name': 'remap_active_2_btn',
                'elem_names': ['key_active_2_label', 'key_active_2_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Active 2', 'key_active_2'))
            },
            {
                'name': 'remap_active_3_btn',
                'elem_names': ['key_active_3_label', 'key_active_3_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Active 3', 'key_active_3'))
            },
            {
                'name': 'remap_passive_1_btn',
                'elem_names': ['key_passive_1_label', 'key_passive_1_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Passive 1', 'key_passive_1'))
            },
            {
                'name': 'remap_passive_2_btn',
                'elem_names': ['key_passive_2_label', 'key_passive_2_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Passive 2', 'key_passive_2'))
            },
            {
                'name': 'remap_passive_3_btn',
                'elem_names': ['key_passive_3_label', 'key_passive_3_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Passive 3', 'key_passive_3'))
            },
            {
                'name': 'remap_passive_4_btn',
                'elem_names': ['key_passive_4_label', 'key_passive_4_value'],
                'action': (lambda: self.game.menus['remap'].open('Toggle Passive 4', 'key_passive_4'))
            },
            {
                'name': 'cycle_music_vol_btn',
                'elem_names': ['music_vol_label', 'music_vol_value'],
                'action': self._cycle_music_volume
            },
        )

        self._add_element_unions_from_dicts(union_dicts)
        self._expand_height()
    
    def _trigger_restore_defaults(self):
        """Restore default settings and rewrite the menu."""

        self.game.settings.restore_to_defaults()
        self.game.settings.save_data()
        self.update()
    
    # TODO: merge the two cycle methods into one
    def _cycle_framerates(self):
        """Cycle through available framerates."""

        id = 0
        n_options = len(config.framerates)
        for i in range(n_options):
            framerate = config.framerates[i]
            if self.game.settings.data['fps'] == framerate:
                id = i
                break

        next_id = (n_options + id + 1) % n_options
        next_framerate = config.framerates[next_id]
        self.game.settings.data['fps'] = next_framerate
        self.game.settings.save_data()
        self.update()

    def _cycle_music_volume(self):
        """Cycle through available music volume."""

        id = 0
        n_options = len(config.music_volumes)
        for i in range(n_options):
            volume = config.music_volumes[i]
            if self.game.settings.data['music_volume'] == volume:
                id = i
                break

        next_id = (n_options + id + 1) % n_options
        next_volume = config.music_volumes[next_id]
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

    def __init__(self, game, name="remap", background=None,
                 width=None, height=None, padding=None):
        """Initialize the key remapping menu."""

        super().__init__(game, name, background, width, height, padding)

        self.keybind = None
    
    def open(self, control, keybind):
        """Show the menu with the correct prompt."""

        self.keybind = keybind
        key_name = pygame.key.name(self.game.settings.data[self.keybind])

        text = "Press a key to remap\n"
        text += f'"{control}"\n'
        text += f"\nCurrent keybinding: {key_name}"

        self.elements = {}
        tb = TextBox(self, 'prompt', text,
                     position=self.rect.center, anchor='center')
        
        return super().open()
    
    def listen_for_key(self, key):
        """Listen for a keypress and remap the key."""

        if not self.is_visible:
            return False
        
        self.game.settings.data[self.keybind] = key
        self.game.menus['settings'].update()
        self.game.settings.save_data()
        self.close(next_menu="settings")

class InfoMenu(Menu):
    """A class representing the info page/ menu."""

    def __init__(self, game, name="info", background=None,
                 width=None, height=None, padding=None):
        """Initialize the info menu."""

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):
        """Populate the menu with information."""

        element_dicts = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: self.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Info',
                'font': config.font_large,
                'x_offset' : self.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            }, {
                'type': 'textbox',
                'name': 'about',
                'content': 'Created by @kljupko as a demo project.',
                'linked_to': 'title',
                'ignore_linked_x': True,
                'y_offset': 7
            },
        )

        self._add_elements_from_dicts(element_dicts)
        self._expand_height()

class PauseMenu(Menu):
    """A class representing the game's pause menu."""

    def __init__(self, game, name='pause', background=None,
                 width=None, height=None, padding=None):
        """Initialize the pause menu."""

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):

        element_dicts = (
            {
                'type': 'label',
                'name': 'continue_btn',
                'content': 'Continue',
                'action': self._continue_session
            },
            {
                'type': 'label',
                'name': 'restart_btn',
                'content': 'Restart',
                'linked_to': 'continue_btn',
                'y_offset': 1,
                'action': self._restart_session
            },
            {
                'type': 'label',
                'name': 'quit_btn',
                'content': 'Quit to Main Menu',
                'linked_to': 'restart_btn',
                'y_offset': 1,
                'action': self.game.quit_session
            },
        )

        self._add_elements_from_dicts(element_dicts)
        self._expand_height()
    
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
        # update the bottom tray just to overwrite the part of the menu
        self.game.bot_tray.update()
        self.game.music_player.unpause()
    
    def _restart_session(self):
        """Close the menu and restart the session."""

        self.game.quit_session()
        self.game.start_session()
        self.close()

__all__ = [
    "MainMenu", "UpgradeMenu", "AchievementsMenu", "SettingsMenu",
    "RemapKeyMenu", "InfoMenu", "PauseMenu"
]