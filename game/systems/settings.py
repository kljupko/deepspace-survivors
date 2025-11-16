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

    confirm: Keybind
    cancel: Keybind

    move_left: Keybind
    move_right: Keybind
    fire: Keybind

    active_1: Keybind
    active_2: Keybind
    active_3: Keybind
    passive_1: Keybind
    passive_2: Keybind
    passive_3: Keybind
    passive_4: Keybind

class Keybind():
    """A class representing a keybind."""

    def __init__(self, control: str, keycode: int) -> None:
        """Initialize the keybind."""

        self.control = control
        self.keycode = keycode
    
    def get_key_name(self):
        """Return the name of the key set to this keybind."""

        return pygame.key.name(self.keycode)

    def set_keybind_to(self, keycode: int):
        """Sets the keybind to the given keycode."""

        self.keycode = keycode
    
    def serialize(self):
        """Return a dictionary containing the control and keycode."""

        keybind: SerializedKeybind = {
            'control': self.control,
            'keycode': self.keycode
        }
        return keybind

class SerializedSettingsDict(TypedDict):
    """A class representing a serialized version of a SettingsDict."""

    fps: int
    show_fps: bool
    keybinds: SerializedKeybindsDict
    music_volume: int

class SerializedKeybindsDict(TypedDict):
    """A class representing a serialized version of a KeybindsDict."""

    confirm: SerializedKeybind
    cancel: SerializedKeybind

    move_left: SerializedKeybind
    move_right: SerializedKeybind
    fire: SerializedKeybind

    active_1: SerializedKeybind
    active_2: SerializedKeybind
    active_3: SerializedKeybind
    passive_1: SerializedKeybind
    passive_2: SerializedKeybind
    passive_3: SerializedKeybind
    passive_4: SerializedKeybind

class SerializedKeybind(TypedDict):
    """A class representing a serialized version of a Keybind."""

    control: str
    keycode: int

class Settings():
    """A class representing the user settings and controls."""

    def __init__(self, game: Game):
        """Initialize the user settings object."""

        self.game = game

        data = self._load_data(config.settings_path)

        if data:
            self.data = self.deserialize_settings(data)
            return
        
        # otherwise, loading saved settings failed
        print("Applying default settings.")
        self.data = self.deserialize_settings(self._defaults())
        self.save_data()
      
    def _load_data(self, path: str) -> SerializedSettingsDict | None:
        """Load the settings and controls from a .json file."""

        p = Path(path)
        if not p.exists():
            print(f"\t\tSettings not found at: {p}.")
            return None
        
        data = self._defaults()
        try:
            loaded_data: SerializedSettingsDict = json.loads(p.read_text())
            for key in data:
                if key in loaded_data:
                    data[key] = loaded_data[key]
        except Exception as e:
            print(f"\t\tEncountered an error while loading settings data: {e}")
            return None
        
        return data
      
    def _defaults(self) -> SerializedSettingsDict:
        """Return a dictionary containing the default settings data."""

        defaults: SerializedSettingsDict = {
            'fps' : 60,
            'show_fps' : False,

            'keybinds': {
                'confirm' : {
                    'control': "Confirm",
                    'keycode': pygame.K_RETURN
                    },
                'cancel' : {
                    'control': "Cancel",
                    'keycode': pygame.K_ESCAPE
                    },

                'move_left' : {
                    'control': "Move Left",
                    'keycode': pygame.K_LEFT
                    },
                'move_right' : {
                    'control': "Move Right",
                    'keycode': pygame.K_RIGHT
                    },
                'fire' : {
                    'control': "Fire",
                    'keycode': pygame.K_SPACE
                    },

                'active_1' : {
                    'control': "Toggle Active 1",
                    'keycode': pygame.K_w
                    },
                'active_2' : {
                    'control': "Toggle Active 2",
                    'keycode': pygame.K_e
                    },
                'active_3' : {
                    'control': "Toggle Active 3",
                    'keycode': pygame.K_r
                    },
                'passive_1' : {
                    'control': "Toggle Passive 1",
                    'keycode': pygame.K_a
                    },
                'passive_2' : {
                    'control': "Toggle Passive 2",
                    'keycode': pygame.K_s
                    },
                'passive_3' : {
                    'control': "Toggle Passive 3",
                    'keycode': pygame.K_d
                    },
                'passive_4' : {
                    'control': "Toggle Passive 4",
                    'keycode': pygame.K_f
                    },
            },

            'music_volume' : 5
        }
        
        return defaults
    
    def deserialize_settings(self, data: SerializedSettingsDict):
        """
        Convert the values from the settings data
        into useful Python objects, and return the data dictionary.
        """

        kb = data['keybinds']
        deserialized: SettingsDict = {
            'fps': data['fps'],
            'show_fps': data['show_fps'],

            'keybinds': {
                'confirm': Keybind(
                    kb['confirm']['control'],
                    kb['confirm']['keycode']
                    ),
                'cancel': Keybind(
                    kb['cancel']['control'],
                    kb['cancel']['keycode']
                    ),

                'move_left': Keybind(
                    kb['move_left']['control'],
                    kb['move_left']['keycode']
                    ),
                'move_right': Keybind(
                    kb['move_right']['control'],
                    kb['move_right']['keycode']
                ),
                'fire': Keybind(
                    kb['fire']['control'],
                    kb['fire']['keycode']
                ),

                'active_1': Keybind(
                    kb['active_1']['control'],
                    kb['active_1']['keycode']
                ),
                'active_2': Keybind(
                    kb['active_2']['control'],
                    kb['active_2']['keycode']
                ),
                'active_3': Keybind(
                    kb['active_3']['control'],
                    kb['active_3']['keycode']
                ),
                'passive_1': Keybind(
                    kb['passive_1']['control'],
                    kb['passive_1']['keycode']
                ),
                'passive_2': Keybind(
                    kb['passive_2']['control'],
                    kb['passive_2']['keycode']
                ),
                'passive_3': Keybind(
                    kb['passive_3']['control'],
                    kb['passive_3']['keycode']
                ),
                'passive_4': Keybind(
                    kb['passive_4']['control'],
                    kb['passive_4']['keycode']
                )
            },

            'music_volume' : data['music_volume']
        }

        return deserialized

    def serialize_settings(self):
        """Convert the Python objects from the settings into json."""

        kb = self.data['keybinds']
        serialized: SerializedSettingsDict = {
            'fps' : self.data['fps'],
            'show_fps' : self.data['show_fps'],

            'keybinds': {
                'confirm' : {
                    'control': kb['confirm'].control,
                    'keycode': kb['confirm'].keycode
                    },
                'cancel' : {
                    'control': kb['cancel'].control,
                    'keycode': kb['cancel'].keycode
                    },

                'move_left' : {
                    'control': kb['move_left'].control,
                    'keycode': kb['move_left'].keycode
                    },
                'move_right' : {
                    'control': kb['move_right'].control,
                    'keycode': kb['move_right'].keycode
                    },
                'fire' : {
                    'control': kb['fire'].control,
                    'keycode': kb['fire'].keycode
                    },

                'active_1' : {
                    'control': kb['active_1'].control,
                    'keycode': kb['active_1'].keycode
                    },
                'active_2' : {
                    'control': kb['active_2'].control,
                    'keycode': kb['active_2'].keycode
                    },
                'active_3' : {
                    'control': kb['active_3'].control,
                    'keycode': kb['active_3'].keycode
                    },
                'passive_1' : {
                    'control': kb['passive_1'].control,
                    'keycode': kb['passive_1'].keycode
                    },
                'passive_2' : {
                    'control': kb['passive_2'].control,
                    'keycode': kb['passive_2'].keycode
                    },
                'passive_3' : {
                    'control': kb['passive_3'].control,
                    'keycode': kb['passive_3'].keycode
                    },
                'passive_4' : {
                    'control': kb['passive_4'].control,
                    'keycode': kb['passive_4'].keycode
                    },
            },

            'music_volume' : self.data['music_volume']
        }

        return serialized

    def save_data(self):
        "Save the current settings to a .json file."

        path = Path(config.settings_path)

        try:
            data = json.dumps(self.serialize_settings(), indent=4)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        except Exception as e:
            print(f"Encountered an error while saving settings: {e}.")
    
    def restore_to_defaults(self):
        """Restore the settings to default values."""

        self.data = self.deserialize_settings(self._defaults())

__all__ = ["Settings"]