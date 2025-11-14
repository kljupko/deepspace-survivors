"""
A module which contains the Settings class
for user-defined settings and keybindings.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

from pathlib import Path
import json

import pygame

from ..utils import config

class SettingsDict(TypedDict):
    """
    A class representing the dictionary containing user-defined settings.
    """

    fps: int
    show_fps: bool
    keybinds: KeybindsDict
    music_volume: int

class KeybindsDict(TypedDict):
    """A class representing a dictionary containing keybinds."""

    key_confirm: int
    key_cancel: int

    key_move_left: int
    key_move_right: int
    key_fire: int

    key_active_1: int
    key_active_2: int
    key_active_3: int
    key_passive_1: int
    key_passive_2: int
    key_passive_3: int
    key_passive_4: int

class Settings():
    """A class representing the user settings and controls."""

    def __init__(self, game: Game):
        """Initialize the user settings object."""

        self.game = game

        data = self._load_data(config.settings_path)

        if data:
            self.data = data
            return
        
        # otherwise, loading saved settings failed
        print("Applying default settings.")
        self.data = self._defaults()
        self.save_data()
    
    def _defaults(self) -> SettingsDict:
        """Return a dictionary containing the default settings data."""

        data: SettingsDict = {
            'fps' : 60,
            'show_fps' : False,

            'keybinds': {
                'key_confirm' : pygame.K_RETURN,
                'key_cancel' : pygame.K_ESCAPE,

                'key_move_left' : pygame.K_LEFT,
                'key_move_right' : pygame.K_RIGHT,
                'key_fire' : pygame.K_SPACE,

                'key_active_1' : pygame.K_w,
                'key_active_2' : pygame.K_e,
                'key_active_3' : pygame.K_r,
                'key_passive_1' : pygame.K_a,
                'key_passive_2' : pygame.K_s,
                'key_passive_3' : pygame.K_d,
                'key_passive_4' : pygame.K_f,
            },

            'music_volume' : 5
        }
        return data
    
    def _load_data(self, path: str) -> SettingsDict | None:
        """Load the settings and controls from a .json file."""

        p = Path(path)
        if not p.exists():
            print(f"\t\tSettings not found at: {p}.")
            return None
        
        data = self._defaults()
        try:
            loaded_data = json.loads(p.read_text())
            for key in data:
                if key in loaded_data:
                    data[key] = loaded_data[key]
        except Exception as e:
            print(f"\t\tEncountered an error while loading settings data: {e}")
            return None
        
        return data
    
    def save_data(self):
        "Save the current settings to a .json file."

        path = Path(config.settings_path)

        try:
            data = json.dumps(self.data, indent=4)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        except Exception as e:
            print(f"Encountered an error while saving settings: {e}.")
    
    def restore_to_defaults(self):
        """Restore the settings to default values."""

        self.data = self._defaults()

__all__ = ["Settings"]