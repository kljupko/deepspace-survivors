"""A module containing the classes for the top and bottom tray."""

from .base import Tray

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
                'type': 'label',
                'name': 'fire_power_value',
                'content': self.game.ship.fire_power,
                'font': None, 'wraplen': None,
                'x': 0, 'y': 0,
                'anchor': None,
                'action': None
            }, {
                'type': 'label',
                'name': 'fire_rate_value',
                'content': self.game.ship.fire_rate,
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
                'type': 'label',
                'name': 'ship_hp_value',
                'content': self.game.ship.hp,
                'font': None, 'wraplen': None,
                'x': 0, 'y': 0,
                'anchor': None,
                'action': None
            }, {
                'type': 'label',
                'name': 'ship_thrust_value',
                'content': self.game.ship.thrust,
                'font': None, 'wraplen': None,
                'x': self.rect.width, 'y': 0,
                'anchor': 'topright',
                'action': None
            }, {
                'type': 'icon',
                'name': 'active_1_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 1, 'y': 11,
                'anchor': 'midtop',
                'action': self.game.ship.active_abilities[0].toggle
            }, {
                'type': 'icon',
                'name': 'active_2_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 2, 'y': 0,
                'anchor': 'midtop',
                'action': self.game.ship.active_abilities[1].toggle
            }, {
                'type': 'icon',
                'name': 'active_3_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 4 * 3, 'y': 0,
                'anchor': 'midtop',
                'action': self.game.ship.active_abilities[2].toggle
            }, {
                'type': 'icon',
                'name': 'passive_1_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 1, 'y': 12,
                'anchor': 'midtop',
                'action': self.game.ship.passive_abilities[0].toggle
            }, {
                'type': 'icon',
                'name': 'passive_2_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 3, 'y': 0,
                'anchor': 'midtop',
                'action': self.game.ship.passive_abilities[1].toggle
            }, {
                'type': 'icon',
                'name': 'passive_3_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 5, 'y': 0,
                'anchor': 'midtop',
                'action': self.game.ship.passive_abilities[2].toggle
            }, {
                'type': 'icon',
                'name': 'passive_4_btn',
                'content': None,
                'font': None, 'wraplen': None,
                'x': self.rect.width // 8 * 7, 'y': 0,
                'anchor': 'midtop',
                'action': self.game.ship.passive_abilities[3].toggle
            },
        )

        self._add_elements_from_dicts(element_dicts)
        # no need to call self._expand_height

__all__ = ["TopTray", "BottomTray"]