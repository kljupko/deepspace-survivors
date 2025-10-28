"""
A module which contains the Settings class
for user-defined settings and keybindings.
"""

from pathlib import Path
import json
import pygame

from ..utils import config

class Settings():
    """A class representing the user settings and controls."""

    def __init__(self, game):
        """Initialize the user settings object."""

        self.game = game

        self.data = self._load_data(config.settings_path)

        if self.data:
            return
        
        # otherwise, loading saved settings failed
        print("Applying default settings.")
        self.data = self._defaults()
        self.save_data()
    
    def _defaults(self):
        """Return a dictionary containing the default settings data."""

        data = {
            'fps' : 60,
            'show_fps' : False,

            # keybinds
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

            'music_volume' : 5
        }
        return data
    
    def _load_data(self, path):
        """Load the settings and controls from a .json file."""

        path = Path(path)
        if not path.exists():
            print(f"\t\tSettings not found at: {path}.")
            return False
        
        data = self._defaults()
        try:
            loaded_data = json.loads(path.read_text())
            for key in data:
                if key in loaded_data:
                    data[key] = loaded_data[key]
        except Exception as e:
            print(f"\t\tEncountered an error while loading settings data: {e}")
            return False
        
        return data
    
    def save_data(self):
        "Save the current settings to a .json file."

        path = Path(config.settings_path)

        try:
            data = json.dumps(self.data)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        except Exception as e:
            print(f"Encountered an error while saving settings: {e}.")
    
    def restore_to_defaults(self):
        """Restore the settings to default values."""

        self.data = self._defaults()

__all__ = ["Settings"]