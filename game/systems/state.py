"""
A module containing the State class, which tracks the current game state.
"""

import pygame

class State():
    """Represents a class which contains the game's current state."""

    def __init__(self) -> None:
        """Initialize the game state object."""

        self.session_running: bool = False
        self.session_start: int = pygame.time.get_ticks()
        self.last_session_tick: int = pygame.time.get_ticks()
        self.session_duration: int = 0 # in miliseconds
        self.last_second_tracked: int = -1
        self.credits_earned: int = 0
        self.level: int = 1
        self.killcount: int = 0
    
    def track_duration(self) -> None:
        """Track the session duration."""

        now = pygame.time.get_ticks()
        self.session_duration += now - self.last_session_tick
        self.last_session_tick = now
        
__all__ = ["State"]
