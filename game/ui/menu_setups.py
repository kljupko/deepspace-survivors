"""
A module containing collections of dictionaries
filled with key-value pairs
specifying the names, types, positions, and actions
of their respective UI Elements.
"""
import pygame
from ..utils import config, helper_funcs

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
                'name': 'rewards_btn',
                'content': 'Rewards',
                'linked_to' : 'upgrade_btn',
                'y_offset': 1,
                'action': lambda: menu.game.menus['rewards'].open()
            }, {
                'type': 'label',
                'name': 'settings_btn',
                'content': 'Settings',
                'linked_to' : 'rewards_btn',
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

    elements = [
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
            }, {
                'type' : 'icon',
                'name': 'credits_icon',
                'content': helper_funcs.load_image(None, 'gold', (10, 10)),
                'linked_to': 'title',
                'ignore_linked_x': True,
                'y_offset': 3
            }, {
                'type': 'label',
                'name': 'credits_amount',
                'content': helper_funcs.shorten_number(
                    menu.game.progress.data['credits']
                    ),
                'linked_to': 'credits_icon',
                'linked_anchor': 'topright',
                'x_offset': 1
            }
    ]

    linked_to = "credits_icon"
    for upgrade in menu.game.upgrades.values():

        upgrade_dict = {}
        upgrade_dict['type'] = 'icon'
        upgrade_dict['name'] = upgrade.name.lower().replace(" ", "_") + "_icon"
        upgrade_dict['content'] = upgrade.image
        upgrade_dict['linked_to'] = linked_to
        upgrade_dict['y_offset'] = 3
        elements.append(upgrade_dict)

        linked_to = upgrade_dict['name']
        upgrade_dict = {}
        upgrade_dict['type'] = 'textbox'
        upgrade_dict['name'] = upgrade.name.lower().replace(" ", "_") + "_name"
        upgrade_dict['content'] = upgrade.name
        upgrade_dict['linked_to'] = linked_to
        upgrade_dict['linked_anchor'] = 'topright'
        elements.append(upgrade_dict)

        upgrade_dict = {}
        content = upgrade.description
        content += f"\nLevel: {upgrade.level}"
        cost = f"\nCost: {helper_funcs.shorten_number(upgrade.get_cost())}"
        if upgrade.max_level is not None:
            content += f"\nMax Level: {upgrade.max_level}"
            if upgrade.level >= upgrade.max_level:
                cost = ""
        content += cost
        upgrade_dict['type'] = 'textbox'
        upgrade_dict['name'] = upgrade.name.lower().replace(" ", "_") + "_desc"
        upgrade_dict['content'] = content
        upgrade_dict['linked_to'] = linked_to
        elements.append(upgrade_dict)

        linked_to = upgrade_dict['name']
        
        upgrade_dict = {}
        content = "Upgrade" if upgrade.is_available() else "   x   "
        if upgrade.max_level is not None and upgrade.level >= upgrade.max_level:
            content = "Maxxed out"
        upgrade_dict['type'] = 'label'
        upgrade_dict['name'] = upgrade.name.lower().replace(" ", "_") + "_btn"
        upgrade_dict['content'] = content
        upgrade_dict['linked_to'] = linked_to
        upgrade_dict['y_offset'] = 1
        upgrade_dict['action'] = lambda un=upgrade.name : menu._buy_upgrade(un)
        elements.append(upgrade_dict)

        linked_to = upgrade_dict['name']

    return elements

def build_rewards_menu_elements(menu):
    """
    Return the collection of dicts for the rewards menu UI Elements.
    """

    elements = [
            {
                'type': 'label',
                'name': 'back_btn',
                'content': '< BACK',
                'action': lambda: menu.close('main')
            }, {
                'type': 'label',
                'name': 'title',
                'content': 'Rewards',
                'font': config.font_large,
                'x_offset' : menu.rect.width // 2,
                'y_offset': 22,
                'anchor': 'midtop'
            },
    ]

    linked_to = 'title'
    for reward in menu.game.rewards.values():
        
        reward_dict = {}
        reward_dict['type'] = 'icon'
        reward_dict['name'] = reward.name.lower().replace(" ", "_") + "_icon"
        reward_dict['content'] = reward.image
        reward_dict['linked_to'] = linked_to
        reward_dict['ignore_linked_x'] = True
        reward_dict['y_offset'] = 3
        elements.append(reward_dict)

        linked_to = reward_dict['name']
        reward_dict = {}
        reward_dict['type'] = 'textbox'
        reward_dict['name'] = reward.name.lower().replace(" ", "_") + "_name"
        reward_dict['content'] = reward.name
        reward_dict['linked_to'] = linked_to
        reward_dict['linked_anchor'] = 'topright'
        elements.append(reward_dict)

        reward_dict = {}
        reward_dict['type'] = 'textbox'
        reward_dict['name'] = reward.name.lower().replace(" ", "_") + "_instr"
        reward_dict['content'] = reward.instructions
        reward_dict['linked_to'] = linked_to
        elements.append(reward_dict)
        
        linked_to = reward_dict['name']
        reward_dict = {}
        content = "Locked"
        action = None
        if reward.is_unlocked:
            if hasattr(reward, 'is_claimed') and not reward.is_claimed:
                content = "Claim"
                action = lambda rn=reward.name : menu._claim_reward(rn)
            elif hasattr(reward, 'is_toggled_on'):
                action = lambda rn=reward.name : menu._toggle_reward(rn)
                if reward.is_toggled_on:
                    content = "Disable"
                else:
                    content = "Enable"
        reward_dict['type'] = 'label'
        reward_dict['name'] = reward.name.lower().replace(" ", "_") + "_btn"
        reward_dict['content'] = content
        reward_dict['linked_to'] = linked_to
        reward_dict['y_offset'] = 1
        reward_dict['action'] = action
        elements.append(reward_dict)

        linked_to = reward_dict['name']

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

def build_top_tray_elements(tray):
    """
    Return the collection of dicts for the top tray's UI Elements.
    """

    elements = (
            {
                'type': 'icon',
                'name': 'fire_power_icon',
                'content': tray.game.ship.stats['Fire Power'].image,
            }, {
                'type': 'label',
                'name': 'fire_power_value',
                'content': tray.game.ship.stats['Fire Power'].value,
                'linked_to' : 'fire_power_icon',
                'linked_anchor': 'topright'
            }, {
                'type': 'icon',
                'name': 'fire_rate_icon',
                'content': tray.game.ship.stats['Fire Rate'].image,
                'x_offset': tray.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'fire_rate_value',
                'content': tray.game.ship.stats['Fire Rate'].value,
                'linked_to': 'fire_rate_icon',
                'linked_anchor': 'topleft',
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'session_duration',
                'content': tray._get_session_duration(),
                'x_offset': tray.rect.width // 2,
                'anchor': 'midtop',
                'action': lambda: tray.game.menus['pause'].open()
            }, {
                'type': 'label',
                'name': 'credits_earned',
                'content': helper_funcs.shorten_number(tray.game.state.credits_earned),
                'linked_to': 'session_duration',
                'linked_anchor': 'midbottom',
                'x_offset': 5,
                'y_offset': 1,
                'anchor': 'midtop',
                'action': lambda: tray.game.menus['pause'].open()
            }, {
                'type': 'icon',
                'name': 'credits_icon',
                'content': helper_funcs.load_image(None, 'gold', (10, 10)),
                'linked_to': 'credits_earned',
                'linked_anchor': 'topleft',
                'x_offset': -1,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'fps',
                'content': tray._get_fps(),
                'linked_to': 'credits_earned',
                'ignore_linked_x': True,
                'linked_anchor': 'topleft',
                'x_offset': tray.rect.width,
                'anchor': 'topright'
            },
        )

    return elements

def build_bot_tray_elements(tray):
    """
    Return the collection of dicts for the bottom tray's UI Elements.
    """

    elements = (
            {
                'type': 'icon',
                'name': 'ship_hp_icon',
                'content': tray.game.ship.stats['Hit Points'].image,
            }, {
                'type': 'label',
                'name': 'ship_hp_value',
                'content': tray.game.ship.stats['Hit Points'].value,
                'linked_to': 'ship_hp_icon',
                'linked_anchor': 'topright'
            }, {
                'type': 'icon',
                'name': 'ship_thrust_icon',
                'content': tray.game.ship.stats['Thrust'].image,
                'x_offset': tray.rect.width,
                'anchor': 'topright'
            }, {
                'type': 'label',
                'name': 'ship_thrust_value',
                'content': tray.game.ship.stats['Thrust'].value,
                'linked_to': 'ship_thrust_icon',
                'linked_anchor': 'topleft',
                'anchor': 'topright',
            }, {
                'type': 'icon',
                'name': 'active_1_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'ship_hp_icon',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 4 * 1,
                'anchor': 'midtop',
            }, {
                'type': 'icon',
                'name': 'active_1_icon',
                'content': tray.game.ship.active_abilities[0].icon,
                'linked_to': 'active_1_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            },  {
                'type': 'icon',
                'name': 'active_2_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'ship_hp_icon',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 4 * 2,
                'anchor': 'midtop',
            }, {
                'type': 'icon',
                'name': 'active_2_icon',
                'content': tray.game.ship.active_abilities[1].icon,
                'linked_to': 'active_2_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            }, {
                'type': 'icon',
                'name': 'active_3_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'ship_hp_icon',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 4 * 3,
                'anchor': 'midtop',
            }, {
                'type': 'icon',
                'name': 'active_3_icon',
                'content': tray.game.ship.active_abilities[2].icon,
                'linked_to': 'active_3_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            }, {
                'type': 'icon',
                'name': 'passive_1_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'active_1_bg',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 8 * 1,
                'anchor': 'midtop'
            }, {
                'type': 'icon',
                'name': 'passive_1_icon',
                'content': tray.game.ship.passive_abilities[0].icon,
                'linked_to': 'passive_1_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            }, {
                'type': 'icon',
                'name': 'passive_2_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'active_1_bg',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 8 * 3,
                'anchor': 'midtop'
            }, {
                'type': 'icon',
                'name': 'passive_2_icon',
                'content': tray.game.ship.passive_abilities[1].icon,
                'linked_to': 'passive_2_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            }, {
                'type': 'icon',
                'name': 'passive_3_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'active_1_bg',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 8 * 5,
                'anchor': 'midtop'
            }, {
                'type': 'icon',
                'name': 'passive_3_icon',
                'content': tray.game.ship.passive_abilities[2].icon,
                'linked_to': 'passive_3_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            }, {
                'type': 'icon',
                'name': 'passive_4_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'linked_to': 'active_1_bg',
                'y_offset': 1,
                'ignore_linked_x': True,
                'x_offset': tray.rect.width // 8 * 7,
                'anchor': 'midtop'
            }, {
                'type': 'icon',
                'name': 'passive_4_icon',
                'content': tray.game.ship.passive_abilities[3].icon,
                'linked_to': 'passive_4_bg',
                'linked_anchor': 'center',
                'anchor': 'center'
            }
        )

    return elements

def build_bot_tray_unions(tray):
    """
    Return the collection of dicts for the bottom tray's ElemUnions.
    """

    unions = (
            {
                'name': 'toggle_active_1_btn',
                'elem_names': ['active_1_bg', 'active_1_icon'],
                'action': lambda: tray.game.ship.toggle_active_ability_num(1)
            },
            {
                'name': 'toggle_active_2_btn',
                'elem_names': ['active_2_bg', 'active_2_icon'],
                'action': lambda: tray.game.ship.toggle_active_ability_num(2)
            },
            {
                'name': 'toggle_active_3_btn',
                'elem_names': ['active_3_bg', 'active_3_icon'],
                'action': lambda: tray.game.ship.toggle_active_ability_num(3)
            },
            {
                'name': 'toggle_passive_1_btn',
                'elem_names': ['passive_1_bg', 'passive_1_icon'],
                'action': lambda: tray.game.ship.toggle_passive_ability_num(1)
            },
            {
                'name': 'toggle_passive_2_btn',
                'elem_names': ['passive_2_bg', 'passive_2_icon'],
                'action': lambda: tray.game.ship.toggle_passive_ability_num(2)
            },
            {
                'name': 'toggle_passive_3_btn',
                'elem_names': ['passive_3_bg', 'passive_3_icon'],
                'action': lambda: tray.game.ship.toggle_passive_ability_num(3)
            },
            {
                'name': 'toggle_passive_4_btn',
                'elem_names': ['passive_4_bg', 'passive_4_icon'],
                'action': lambda: tray.game.ship.toggle_passive_ability_num(4)
            },
        )

    return unions
