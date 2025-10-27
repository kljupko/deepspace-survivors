"""A module containing the classes for the top and bottom tray."""

from .base import Tray
from ..systems import helper_funcs

class TopTray(Tray):
    """A class representing the top tray."""

    def __init__(self, game, name='top_tray', background=None,
                 width=None, height=None, padding=None):
        """Initialize the top tray."""

        height = 23

        super().__init__(game, name, background, width, height, padding)
    
    def _load_elements(self):
        """Populate the tray with UI Elements."""

        element_dicts = (
            {
                'type': 'icon',
                'name': 'fire_power_icon',
                'content': self.game.ship.stats['Fire Power'].image,
                'font': None, 'wraplen': None,
                'x': 0, 'y': 0,
                'anchor': None,
                'action': None
            }, {
                'type': 'label',
                'name': 'fire_power_value',
                'content': self.game.ship.stats['Fire Power'].value,
                'font': None, 'wraplen': None,
                'x': 11, 'y': 0,
                'anchor': None,
                'action': None
            }, {
                'type': 'label',
                'name': 'fire_rate_value',
                'content': self.game.ship.stats['Fire Rate'].value,
                'font': None, 'wraplen': None,
                'x': self.rect.width - 13, 'y': 0,
                'anchor': 'topright',
                'action': None
            }, {
                'type': 'icon',
                'name': 'fire_rate_icon',
                'content': self.game.ship.stats['Fire Rate'].image,
                'font': None, 'wraplen': None,
                'x': self.rect.width, 'y': 0,
                'anchor': 'topright',
                'action': None
            }, {
                'type': 'label',
                'name': 'session_duration',
                'content': self._get_session_duration(),
                'font': None, 'wraplen': None,
                'x': self.rect.centerx, 'y': 0,
                'anchor': 'midtop',
                'action': lambda: self.game.menus['pause'].open()
            }, {
                'type': 'label',
                'name': 'credits_earned',
                'content': self.game.state.credits_earned,
                'font': None, 'wraplen': None,
                'x': self.rect.centerx, 'y': 11,
                'anchor': 'midtop',
                'action': lambda: self.game.menus['pause'].open()
            }, {
                'type': 'label',
                'name': 'fps',
                'content': self._get_fps(),
                'font': None, 'wraplen': None,
                'x': self.rect.width, 'y': 0,
                'anchor': 'topright',
                'action': None
            },
        )

        self._add_elements_from_dicts(element_dicts)
        # no need to call self._expand_height
    
    def _get_session_duration(self):
        """Return the duration of the current session."""

        duration = self.game.state.session_duration

        mins, secs = divmod(duration // 1000, 60)
        hours, mins = divmod(mins, 60)
        time = f"{mins:02d}:{secs:02d}"
        if hours > 0:
            time = f"{hours:02d}:" + time
        
        return time

    def _get_fps(self):
        """Return the fps if 'show_fps' setting is True. Else blank."""
        
        return "" if not self.game.settings.data['show_fps'] else self.game.fps

class BottomTray(Tray):
    """A class representing the bottom tray."""

    def __init__(self, game, name='bot_tray', background=None,
                 width=None, height=None, padding=None):
        """Initialize the bottom tray."""

        height = game.screen.height - game.play_surf.height + 11

        super().__init__(game, name, background, width, height, padding)
        self.rect.y = self.game.screen.height - self.rect.height
    
    def _load_elements(self):
        """Populate the tray with UI Elements"""
  
        element_dicts = (
            {
                'type': 'icon',
                'name': 'ship_hp_icon',
                'content': self.game.ship.stats['Hit Points'].image,
                'font': None, 'wraplen': None,
                'x': 0, 'y': 0,
                'anchor': None,
                'action': None
            }, {
                'type': 'label',
                'name': 'ship_hp_value',
                'content': self.game.ship.stats['Hit Points'].value,
                'font': None, 'wraplen': None,
                'x': 11, 'y': 0,
                'anchor': None,
                'action': None
            }, {
                'type': 'label',
                'name': 'ship_thrust_value',
                'content': self.game.ship.stats['Thrust'].value,
                'font': None, 'wraplen': None,
                'x': self.rect.width - 13, 'y': 0,
                'anchor': 'topright',
                'action': None
            }, {
                'type': 'icon',
                'name': 'ship_thrust_icon',
                'content': self.game.ship.stats['Thrust'].image,
                'font': None, 'wraplen': None,
                'x': self.rect.width, 'y': 0,
                'anchor': 'topright',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_1_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 1, 'y': 11,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_2_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 2, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_3_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 3, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_1_icon',
                'content': self.game.ship.active_abilities[0].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 1, 'y': 1,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_2_icon',
                'content': self.game.ship.active_abilities[1].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 2, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_3_icon',
                'content': self.game.ship.active_abilities[2].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 3, 'y': 0,
                'anchor': 'midtop',
                'action': self.game.ship.active_abilities[2].toggle
            }, {
                'type': 'icon',
                'name': 'passive_1_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 1, 'y': 13,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_2_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 3, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_3_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 5, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_4_bg',
                'content': helper_funcs.load_image(dflt_size=(12, 12)),
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 7, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_1_icon',
                'content': self.game.ship.passive_abilities[0].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 1, 'y': 1,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_2_icon',
                'content': self.game.ship.passive_abilities[1].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 3, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_3_icon',
                'content': self.game.ship.passive_abilities[2].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 5, 'y': 0,
                'anchor': 'midtop',
                'action': None
            }, {
                'type': 'icon',
                'name': 'passive_4_icon',
                'content': self.game.ship.passive_abilities[3].icon,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 7, 'y': 0,
                'anchor': 'midtop',
                'action': None
            },
        )

        self._add_elements_from_dicts(element_dicts)
        # no need to call self._expand_height

        union_dicts = (
            {
                'name': 'toggle_active_1_btn',
                'elem_names': ['active_1_bg', 'active_1_icon'],
                'action': lambda: self.game.ship.toggle_active_ability_num(1)
            },
            {
                'name': 'toggle_active_2_btn',
                'elem_names': ['active_2_bg', 'active_2_icon'],
                'action': lambda: self.game.ship.toggle_active_ability_num(2)
            },
            {
                'name': 'toggle_active_3_btn',
                'elem_names': ['active_3_bg', 'active_3_icon'],
                'action': lambda: self.game.ship.toggle_active_ability_num(3)
            },
            {
                'name': 'toggle_passive_1_btn',
                'elem_names': ['passive_1_bg', 'passive_1_icon'],
                'action': lambda: self.game.ship.toggle_passive_ability_num(1)
            },
            {
                'name': 'toggle_passive_2_btn',
                'elem_names': ['passive_2_bg', 'passive_2_icon'],
                'action': lambda: self.game.ship.toggle_passive_ability_num(2)
            },
            {
                'name': 'toggle_passive_3_btn',
                'elem_names': ['passive_3_bg', 'passive_3_icon'],
                'action': lambda: self.game.ship.toggle_passive_ability_num(3)
            },
            {
                'name': 'toggle_passive_4_btn',
                'elem_names': ['passive_4_bg', 'passive_4_icon'],
                'action': lambda: self.game.ship.toggle_passive_ability_num(4)
            },
        )

        self._add_element_unions_from_dicts(union_dicts)

__all__ = ["TopTray", "BottomTray"]