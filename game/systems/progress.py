"""
A module containing the Progress class,
which saves, loads, and keeps track of player progress.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

from pathlib import Path
import json
from ..utils import config
from ..mechanics import rewards

class ProgressDict(TypedDict):
    """
    A class representing the dictionary containing data
    about saved game progress.
    """

    credits: int
    max_credits_owned: int
    max_credits_session: int
    credits_spent: int

    num_of_sessions: int
    longest_session: int
    total_session_duration: int

    upgrades: dict[str, UpgradesProgressDict]
    #rewards: dict[str, RewardsProgressDict]
    rewards: dict[str, list[bool]]

class UpgradesProgressDict(TypedDict):
    """
    A class representing a dictionary containing information on the
    level of an upgrade.
    """

    level: int

class RewardsProgressDict(TypedDict):
    """
    A class representing a dictionary containing information on
    rewards -- are they unlocked and claimed or toggled?
    """

    is_unlocked: bool
    is_claimed_or_toggled: bool

class Progress():
    """A class which handles saving and loading the player's progress."""

    def __init__(self, game: Game):
        """Initialize the progress handler."""

        self.game = game

        data = self._load_data(config.main_save_path)
        if data:
            # loading main file successful
            self.data = data
            self.save_data(True) # save current data as backup
            return
        
        # otherwise, try loading the backup
        print("Failed to load the main save. Loading backup...")
        data = self._load_data(config.back_save_path)
        if data:
            # at least the backup worked
            self.data = data
            return
        
        # otherwise, just use the defaults
        print("Failed to load backup save. Using defaults.")
        self.data = self._defaults()
    
    def _defaults(self) -> ProgressDict:
        """Returns default progress data (new game)."""

        data: ProgressDict = {
            'credits': 0,
            'max_credits_owned' : 0,
            'max_credits_session' : 0,
            'credits_spent' : 0,

            'num_of_sessions' : 0,
            'longest_session' : 0,
            'total_session_duration' : 0,

            'upgrades': {},
            'rewards': {}
        }

        for upgrade in self.game.upgrades.values():
            data['upgrades'][upgrade.name] = {
                'level': upgrade.level
            }
        
        for reward in self.game.rewards.values():
            is_unlocked = False
            is_claimed_or_toggled = False
            if isinstance(reward, rewards.ClaimableReward):
                is_claimed_or_toggled = reward.is_claimed
            elif isinstance(reward, rewards.ToggleableReward):
                is_claimed_or_toggled = reward.is_toggled_on
            data['rewards'][reward.name] = [is_unlocked, is_claimed_or_toggled]
        
        return data
    
    def _load_data(self, path: str) -> ProgressDict | None:
        """Load progress data from a .json file."""

        p = Path(path)
        if not p.exists():
            print(f"\tFile not found at: {p}.")
            return None
        
        data = self._defaults()
        
        try:
            loaded_data = json.loads(p.read_text())
            self._copy_ProgressDict_values(loaded_data, data)
        except Exception as e:
            print(f"\t\tEncountered an error while loading progress data: {e}.")
            return None
        
        return data

    def _copy_ProgressDict_values(self,
                     src_dict: ProgressDict,
                     dest_dict: ProgressDict
                     ) -> None:
        """
        Copies to the destination ProgressDict the values from
        the source ProgressDict, if the source contains them.
        """

        sub_dicts = ['upgrades', 'rewards']
        
        for key in dest_dict:
            if key not in sub_dicts and key in src_dict:
                dest_dict[key] = src_dict[key]

        for key in dest_dict['upgrades']:
            if key in src_dict['upgrades']:
                dest_dict['upgrades'][key] = src_dict['upgrades'][key]

        for key in dest_dict['rewards']:
            if key in src_dict['rewards']:
                dest_dict['rewards'][key] = src_dict['rewards'][key]

    def save_data(self,
                  save_as_backup: bool = False
                  ) -> None:
        """Save the current progress data to a .json file."""

        if save_as_backup:
            path = Path(config.back_save_path)
        else:
            path = Path(config.main_save_path)
        
        try:
            data = json.dumps(self.data, indent=4)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        except Exception as e:
            print(f"Encountered an error while saving progress: {e}.")
    
    def update(self) -> None:
        """Updates the progress after the session ends, and saves."""

        self.data['credits'] += self.game.state.credits_earned

        if self.data['credits'] > self.data['max_credits_owned']:
            self.data['max_credits_owned'] = self.data['credits']
        
        if self.game.state.credits_earned > self.data['max_credits_session']:
            self.data['max_credits_session'] = self.game.state.credits_earned
        
        self.data['num_of_sessions'] += 1

        if self.game.state.session_duration > self.data['longest_session']:
            self.data['longest_session'] = self.game.state.session_duration
        
        self.data['total_session_duration'] += self.game.state.session_duration

        self.save_data()

__all__ = ["Progress"]