"""
A module containing collections of dictionaries
filled with key-value pairs
specifying the names, types, positions, and actions
of their respective UI Elements.
"""
import pygame
from ..utils import config

def build_main_menu_elements(menu):
    """Return the collection of dicts for the main menu UI Elements."""

    elements = (
            {
                'type': 'label',
                'name': 'play_btn',
                'content': 'Play',
                'action': menu.game.start_session
            }, {
                'type': 'label',
                'name': 'upgrade_btn',
                'content': 'Upgrade',
                'linked_to' : 'play_btn',
                'y_offset': 1,
                'action': lambda: menu.game.menus['upgrade'].open()
            }, {
                'type': 'label',
                'name': 'achievements_btn',
                'content': 'Achievements',
                'linked_to' : 'upgrade_btn',
                'y_offset': 1,
                'action': lambda: menu.game.menus['achievements'].open()
            }, {
                'type': 'label',
                'name': 'settings_btn',
                'content': 'Settings',
                'linked_to' : 'achievements_btn',
                'y_offset': 1,
                'action': lambda: menu.game.menus['settings'].open()
            }, {
                'type': 'label',
                'name': 'info_btn',
                'content': 'Info',
                'linked_to' : 'settings_btn',
                'y_offset': 1,
                'action': lambda: menu.game.menus['info'].open()
            }, {
                'type': 'label',
                'name': 'quit_btn',
                'content': 'Quit',
                'linked_to' : 'info_btn',
                'y_offset': 1,
                'action': menu.game.quit
            },
        )
    
    return elements

def build_upgrade_menu_elements(menu):
    """
    Return the collection of dicts for the upgrade menu UI Elements.
    """

    elements = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: menu.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Upgrades',
                'font': config.font_large,
                'x_offset' : menu.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            },
        )

    return elements

def build_achievements_menu_elements(menu):
    """
    Return the collection of dicts for the achievements menu UI Elements.
    """

    elements = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: menu.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Achievements',
                'font': config.font_large,
                'x_offset' : menu.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            },
        )

    return elements

def build_settings_menu_elements(menu, settings_data):
    """
    Return the collection of dicts for the settings menu UI Elements.
    """

    elements = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: menu.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Settings',
                'font': config.font_large,
                'x_offset' : menu.rect.width // 2,
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
                'content': settings_data['fps'],
                'linked_to': 'fps_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': settings_data['show_fps'],
                'linked_to': 'show_fps_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'keybinds_header',
                'content': 'Keybinds',
                'linked_to': 'show_fps_label',
                'ignore_linked_x': True,
                'x_offset' : menu.rect.width // 2,
                'y_offset': 7,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'key_confirm_label',
                'content': 'Confirm',
                'linked_to': 'keybinds_header',
                'x_offset': -menu.rect.width,
                'y_offset': 3
            }, {
                'type': 'label',
                'name': 'key_confirm_value',
                'content': pygame.key.name(settings_data['key_confirm']),
                'linked_to': 'key_confirm_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_cancel']),
                'linked_to': 'key_cancel_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_move_left']),
                'linked_to': 'key_move_left_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_move_right']),
                'linked_to': 'key_move_right_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_fire']),
                'linked_to': 'key_fire_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_active_1']),
                'linked_to': 'key_active_1_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_active_2']),
                'linked_to': 'key_active_2_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_active_3']),
                'linked_to': 'key_active_3_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_passive_1']),
                'linked_to': 'key_passive_1_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_passive_2']),
                'linked_to': 'key_passive_2_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_passive_3']),
                'linked_to': 'key_passive_3_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
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
                'content': pygame.key.name(settings_data['key_passive_4']),
                'linked_to': 'key_passive_4_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'audio_header',
                'content': 'Audio',
                'linked_to': 'key_passive_4_label',
                'ignore_linked_x': True,
                'x_offset' : menu.rect.width // 2,
                'y_offset': 7,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'music_vol_label',
                'content': 'Music Volume',
                'linked_to': 'audio_header',
                'x_offset': -menu.rect.width,
                'y_offset': 3
            }, {
                'type': 'label',
                'name': 'music_vol_value',
                'content': settings_data['music_volume'],
                'linked_to': 'music_vol_label',
                'linked_anchor': 'topright',
                'x_offset': menu.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'other_header',
                'content': 'Other',
                'linked_to': 'music_vol_label',
                'ignore_linked_x': True,
                'x_offset' : menu.rect.width // 2,
                'y_offset': 7,
                'anchor': 'midtop'
            }, {
                'type': 'label',
                'name': 'restore_defaults_btn',
                'content': 'Restore Defaults',
                'linked_to': 'other_header',
                'ignore_linked_x': True,
                'y_offset': 3,
                'action': menu._trigger_restore_defaults
            },
        )

    return elements

def build_settings_menu_unions(menu):
    """
    Return the collection of dicts for the info menu ElemUnions.
    """

    unions = (
            {
                'name': 'cycle_fps_btn',
                'elem_names': ['fps_label', 'fps_value'],
                'action': menu._cycle_framerates
            },
            {
                'name': 'show_fps_btn',
                'elem_names': ['show_fps_label', 'show_fps_value'],
                'action': menu._toggle_fps_display
            },
            {
                'name': 'remap_confirm_btn',
                'elem_names': ['key_confirm_label', 'key_confirm_value'],
                'action': (lambda: menu.game.menus['remap'].open('Confirm', 'key_confirm'))
            },
            {
                'name': 'remap_cancel_btn',
                'elem_names': ['key_cancel_label', 'key_cancel_value'],
                'action': (lambda: menu.game.menus['remap'].open('Cancel', 'key_cancel'))
            },
            {
                'name': 'remap_move_left_btn',
                'elem_names': ['key_move_left_label', 'key_move_left_value'],
                'action': (lambda: menu.game.menus['remap'].open('Move Left', 'key_move_left'))
            },
            {
                'name': 'remap_move_right_btn',
                'elem_names': ['key_move_right_label', 'key_move_right_value'],
                'action': (lambda: menu.game.menus['remap'].open('Move Right', 'key_move_right'))
            },
            {
                'name': 'remap_fire_btn',
                'elem_names': ['key_fire_label', 'key_fire_value'],
                'action': (lambda: menu.game.menus['remap'].open('Fire', 'key_fire'))
            },
            {
                'name': 'remap_active_1_btn',
                'elem_names': ['key_active_1_label', 'key_active_1_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Active 1', 'key_active_1'))
            },
            {
                'name': 'remap_active_2_btn',
                'elem_names': ['key_active_2_label', 'key_active_2_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Active 2', 'key_active_2'))
            },
            {
                'name': 'remap_active_3_btn',
                'elem_names': ['key_active_3_label', 'key_active_3_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Active 3', 'key_active_3'))
            },
            {
                'name': 'remap_passive_1_btn',
                'elem_names': ['key_passive_1_label', 'key_passive_1_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Passive 1', 'key_passive_1'))
            },
            {
                'name': 'remap_passive_2_btn',
                'elem_names': ['key_passive_2_label', 'key_passive_2_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Passive 2', 'key_passive_2'))
            },
            {
                'name': 'remap_passive_3_btn',
                'elem_names': ['key_passive_3_label', 'key_passive_3_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Passive 3', 'key_passive_3'))
            },
            {
                'name': 'remap_passive_4_btn',
                'elem_names': ['key_passive_4_label', 'key_passive_4_value'],
                'action': (lambda: menu.game.menus['remap'].open('Toggle Passive 4', 'key_passive_4'))
            },
            {
                'name': 'cycle_music_vol_btn',
                'elem_names': ['music_vol_label', 'music_vol_value'],
                'action': menu._cycle_music_volume
            },
        )

    return unions

def build_info_menu_elements(menu):
    """
    Return the collection of dicts for the info menu UI Elements.
    """

    elements = (
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: menu.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Info',
                'font': config.font_large,
                'x_offset' : menu.rect.width // 2,
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

    return elements

def build_pause_menu_elements(menu):
    """
    Return the collection of dicts for the pause menu UI Elements.
    """

    elements = (
            {
                'type': 'label',
                'name': 'continue_btn',
                'content': 'Continue',
                'action': menu._continue_session
            },
            {
                'type': 'label',
                'name': 'restart_btn',
                'content': 'Restart',
                'linked_to': 'continue_btn',
                'y_offset': 1,
                'action': menu._restart_session
            },
            {
                'type': 'label',
                'name': 'quit_btn',
                'content': 'Quit to Main Menu',
                'linked_to': 'restart_btn',
                'y_offset': 1,
                'action': menu.game.quit_session
            },
        )

    return elements