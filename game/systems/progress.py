"""
A module containing the Progress class,
which saves, loads, and keeps track of player progress.
"""

from pathlib import Path
import json
from ..utils import config

class Progress():
    """A class which handles saving and loading the player's progress."""

    def __init__(self, game):
        """Initialize the progress handler."""

        self.game = game

        self.data = self._load_data(config.main_save_path)
        if self.data:
            # loading main file successful
            self.save_data(True) # save current data as backup
            return
        
        # otherwise, try loading the backup
        print("Failed to load the main save. Loading backup...")
        self.data = self._load_data(config.back_save_path)
        if self.data:
            # at least the backup worked
            return
        
        # otherwise, just use the defaults
        print("Failed to load backup save. Using defaults.")
        self.data = self._defaults()
    
    def _defaults(self):
        """Returns default progress data (new game)."""

        data = {
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
            data['upgrades'][upgrade.name] = upgrade.level
        
        for reward in self.game.rewards.values():
            is_unlocked = False
            is_claimed_or_toggled = False
            if hasattr(reward, 'is_claimed'):
                is_claimed_or_toggled = reward.is_claimed
            elif hasattr(reward, 'is_toggled_on'):
                is_claimed_or_toggled = reward.is_toggled_on
            data['rewards'][reward.name] = (is_unlocked, is_claimed_or_toggled)
        
        return data
    
    def _load_data(self, path):
        """Load progress data from a .json file."""

        path = Path(path)
        if not path.exists():
            print(f"\tFile not found at: {path}.")
            return False
        
        data = self._defaults()
        
        try:
            loaded_data = json.loads(path.read_text())
            self._copy_values(loaded_data, data, ['upgrades', 'rewards'])
            self._copy_values(loaded_data['upgrades'], data['upgrades'])
            self._copy_values(loaded_data['rewards'], data['rewards'])
        except Exception as e:
            print(f"\t\tEncountered an error while loading progress data: {e}.")
            return False
        
        return data

    def _copy_values(self, from_dict, to_dict, exclude_keys=None):
        """
        Copies to the destination dict the values from the source dict,
        if the source contains them.
        """

        if exclude_keys is None:
            exclude_keys = []
        
        for key in to_dict:
            if key not in exclude_keys and key in from_dict:
                to_dict[key] = from_dict[key]

    def save_data(self, save_as_backup=False):
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
    
    def update(self):
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