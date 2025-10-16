"""A module containing the classes for the top and bottom tray."""

import pygame
from .base import UIElement, Tray

class TopTray(Tray):
    """A class representing the top tray."""

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the top tray."""

        super().__init__(game, name, width, height, background)
    
    def _populate_values(self):
        """Populate the tray with UI Elements."""

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
            self.game, el_name, self.surface, self._get_session_duration(),
            False, position=(self.rect.centerx, 1), anchor="midtop",
            action=self.game.menus['pause'].open
        )

        el_name = "credits_earned"
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface,
            self.game.state.credits_earned,
            position=(self.rect.centerx, 12), anchor="midtop"
        )

        el_name = 'fps'
        self.elements[el_name] = UIElement(
            self.game, el_name, self.surface, self._get_fps(), False,
            position=(self.rect.width - 1, 12), anchor="topright"
        )
    
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

    def __init__(self, game, name, width=None, height=None, background=None):
        """Initialize the bottom tray."""

        super().__init__(game, name, width, height, background)
        self.rect.y = self.game.screen.height - self.rect.height
    
    def _populate_values(self):
        """Populate the tray with UI Elements"""

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
