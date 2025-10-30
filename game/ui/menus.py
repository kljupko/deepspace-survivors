"""A module containing all the menus in the game."""

import pygame

from .base import Menu, TextBox
from ..utils import config
from .menu_setups import *

class Main(Menu):
    """A class which represents the game's main menu."""

    name = "Main Menu"

    def __init__(self, game):
        """Initialize the main menu."""

        name = Main.name
        super().__init__(game, name)
    
    def _load_elements(self):
        """Populate menu with UI Elements."""

        self._add_elements_from_dicts(build_main_menu_elements(self))
        self._expand_height()

class Upgrade(Menu):
    """A class representing the upgrade menu."""

    name = "Upgrade Menu"

    def __init__(self, game):
        """Initialize the upgrade menu."""

        name = Upgrade.name
        super().__init__(game, name)
    
    def _load_elements(self):
        """Populate the menu with upgrades."""

        self._add_elements_from_dicts(build_upgrade_menu_elements(self))
        self._expand_height()
    
    def _buy_upgrade(self, upgrade_name):
        """Attempts to buy the upgrade with the given name."""

        for upgrade in self.game.upgrades.values():
            if upgrade.name != upgrade_name:
                continue
            upgrade.do_upgrade()
            self.update()
            return True
        return False

class Rewards(Menu):
    """A class representing the rewards menu."""

    name = "Rewards Menu"

    def __init__(self, game):
        """Initialize the rewards menu."""

        name = Rewards.name
        super().__init__(game, name)
    
    def _load_elements(self):
        """Populate the menu with rewards."""

        self._add_elements_from_dicts(build_rewards_menu_elements(self))
        self._expand_height()
    
    def _claim_reward(self, reward_name):
        """Claim the reward with the given name."""

        self.game.rewards[reward_name].claim()
        self.update()
    
    def _toggle_reward(self, reward_name):
        """Toggle the reward with the given name."""

        self.game.rewards[reward_name].toggle()
        self.update()

class Settings(Menu):
    """A class representing the game's settings menu."""

    name = "Settings Menu"

    def __init__(self, game):
        """Initialize the settings menu."""

        name = Settings.name
        super().__init__(game, name)
    
    def _load_elements(self):
        """Populate the menu with the values from the settings."""

        data = self.game.settings.data
        self._add_elements_from_dicts(build_settings_menu_elements(self, data))
        self._add_element_unions_from_dicts(build_settings_menu_unions(self))
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

class RemapKey(Menu):
    """A class representing the key remapping prompt."""

    name = "Remap Key Menu"

    def __init__(self, game):
        """Initialize the key remapping menu."""

        name = RemapKey.name
        self.control = None
        self.keybind = None
        self.key_name = None
        super().__init__(game, name)

    
    def open(self, control, keybind):
        """Show the menu with the correct prompt."""

        self.control = control
        self.keybind = keybind
        self.key_name = pygame.key.name(self.game.settings.data[self.keybind])
        
        return super().open()
    
    def _load_elements(self):
        """Load the remap prompt."""

        self.elements = {}

        text = f"Press a key to remap {self.control}"
        text += f"\nCurrent keybinding: {self.key_name}"

        TextBox(self, 'prompt', text, position=self.rect.center, anchor='center')
    
    def listen_for_key(self, key):
        """Listen for a keypress and remap the key."""

        if not self.is_visible:
            return False
        
        self.game.settings.data[self.keybind] = key
        self.game.menus[Settings.name].update()
        self.game.settings.save_data()
        self.close(next_menu=Settings.name)

class Info(Menu):
    """A class representing the info page/ menu."""

    name = "Info Menu"

    def __init__(self, game):
        """Initialize the info menu."""

        name = Upgrade.name
        super().__init__(game, name)
    
    def _load_elements(self):
        """Populate the menu with information."""

        self._add_elements_from_dicts(build_info_menu_elements(self))
        self._expand_height()

class Pause(Menu):
    """A class representing the game's pause menu."""

    name = "Pause Menu"

    def __init__(self, game):
        """Initialize the pause menu."""

        name = Pause.name
        super().__init__(game, name)
    
    def _load_elements(self):

        self._add_elements_from_dicts(build_pause_menu_elements(self))
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
    "Main", "Upgrade", "Rewards", "Settings",
    "RemapKey", "Info", "Pause"
]