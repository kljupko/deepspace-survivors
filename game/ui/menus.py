"""A module containing all the menus in the game."""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

import pygame

from .base import Menu, TextBox
from ..utils import config
from .menu_setups import *

class Main(Menu):
    """A class which represents the game's main menu."""

    name: str = "Main Menu"

    def __init__(self, game: Game) -> None:
        """Initialize the main menu."""

        name = Main.name
        super().__init__(game, name)
    
    def _load_elements(self) -> None:
        """Populate menu with UI Elements."""

        self._add_elements_from_dicts(build_main_menu_elements(self))
        self._expand_height()

class Upgrade(Menu):
    """A class representing the upgrade menu."""

    name: str = "Upgrade Menu"

    def __init__(self, game: Game):
        """Initialize the upgrade menu."""

        name = Upgrade.name
        super().__init__(game, name)
    
    def _load_elements(self) -> None:
        """Populate the menu with upgrades."""

        self._add_elements_from_dicts(build_upgrade_menu_elements(self))
        self._expand_height()
    
    def buy_upgrade(self, upgrade_name: str) -> None:
        """Attempts to buy the upgrade with the given name."""

        for upgrade in self.game.upgrades.values():
            if upgrade.name != upgrade_name:
                continue
            upgrade.do_upgrade()
            self.update()
            return

class Rewards(Menu):
    """A class representing the rewards menu."""

    name: str = "Rewards Menu"

    def __init__(self, game: Game) -> None:
        """Initialize the rewards menu."""

        name = Rewards.name
        super().__init__(game, name)
    
    def _load_elements(self) -> None:
        """Populate the menu with rewards."""

        self._add_elements_from_dicts(build_rewards_menu_elements(self))
        self._expand_height()
    
    def claim_reward(self, reward_name: str) -> None:
        """Claim the reward with the given name."""
        
        reward = self.game.rewards[reward_name]

        if not isinstance(reward, rewards.ClaimableReward):
            return
        
        reward.claim()
        self.update()
    
    def toggle_reward(self, reward_name: str) -> None:
        """Toggle the reward with the given name."""

        reward = self.game.rewards[reward_name]

        if not isinstance(reward, rewards.ToggleableReward):
            return
        
        reward.toggle()
        self.update()

class Settings(Menu):
    """A class representing the game's settings menu."""

    name: str = "Settings Menu"

    def __init__(self, game: Game) -> None:
        """Initialize the settings menu."""

        name = Settings.name
        super().__init__(game, name)
    
    def _load_elements(self) -> None:
        """Populate the menu with the values from the settings."""

        self._add_elements_from_dicts(build_settings_menu_elements(self))
        self._add_element_unions_from_dicts(build_settings_menu_unions(self))
        self._expand_height()
    
    def trigger_restore_defaults(self) -> None:
        """Restore default settings and rewrite the menu."""

        self.game.settings.restore_to_defaults()
        self.game.settings.save_data()
        self.update()
    
    # TODO: merge the two cycle methods into one
    def cycle_framerates(self) -> None:
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

    def cycle_music_volume(self) -> None:
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
    
    def toggle_fps_display(self) -> None:
        """Switch between showing and hiding the framerate."""

        data = self.game.settings.data

        data['show_fps'] = not data['show_fps']
        self.game.settings.save_data()
        self.update()

class Remap(Menu):
    """A class representing the key remapping prompt."""

    name: str = "Remap Key Menu"

    def __init__(self, game: Game):
        """Initialize the key remapping menu."""

        name = Remap.name
        self.keybind: settings.Keybind | None = None
        super().__init__(game, name)

    
    def remap(self, keybind: settings.Keybind) -> None:
        """Show the remap menu with the correct prompt."""

        self.keybind = keybind
        self.open()
    
    def _load_elements(self) -> None:
        """Load the remap prompt."""

        if self.keybind is None:
            return

        self.elements = {}

        text = f"Press a key to remap {self.keybind.control}"
        text += f"\nCurrent keybinding: {self.keybind.get_key_name()}"

        TextBox(self, 'prompt', text, position=self.rect.center, anchor='center')
    
    def listen_for_key(self, key: int) -> None:
        """Listen for a keypress and remap the key."""

        if not self.is_visible:
            return
        
        if self.keybind is None:
            return
        
        self.keybind.set_keybind_to(key)
        self.game.menus['settings'].update()
        self.game.settings.save_data()
        self.close(self.game.menus['settings'])

class Info(Menu):
    """A class representing the info page/ menu."""

    name: str = "Info Menu"

    def __init__(self, game: Game):
        """Initialize the info menu."""

        name = Upgrade.name
        super().__init__(game, name)
    
    def _load_elements(self) -> None:
        """Populate the menu with information."""

        self._add_elements_from_dicts(build_info_menu_elements(self))
        self._expand_height()

class Pause(Menu):
    """A class representing the game's pause menu."""

    name: str = "Pause Menu"

    def __init__(self, game: Game):
        """Initialize the pause menu."""

        name = Pause.name
        super().__init__(game, name)
    
    def _load_elements(self) -> None:

        self._add_elements_from_dicts(build_pause_menu_elements(self))
        self._expand_height()
    
    def open(self) -> None:
        """Pause the game and open the menu."""

        self.game.state.session_running = False
        self.game.music_player.pause()
        return super().open()

    def continue_session(self) -> None:
        """Close the menu and continue the session."""

        self.game.state.session_running = True
        self.game.state.last_session_tick = pygame.time.get_ticks()
        self.close()
        # update the bottom tray just to overwrite the part of the menu
        self.game.bot_tray.update()
        self.game.music_player.unpause()
    
    def restart_session(self) -> None:
        """Close the menu and restart the session."""

        self.game.quit_session()
        self.game.start_session()
        self.close()

class MenusDict(TypedDict):
    """A class representing a dictionary containing all the menus."""

    main: Main
    upgrade: Upgrade
    rewards: Rewards
    settings: Settings
    remap: Remap
    info: Info
    pause: Pause

__all__ = [
    "Main", "Upgrade", "Rewards", "Settings",
    "Remap", "Info", "Pause",
    "MenusDict"
]