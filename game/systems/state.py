"""
A module containing the State class, which tracks the current game state.
"""

import pygame

class State():
    """Represents a class which contains the game's current state."""

    def __init__(self):
        """Initialize the game state object."""

        self.session_running = False
        self.session_start = pygame.time.get_ticks()
        self.last_session_tick = pygame.time.get_ticks()
        self.session_duration = 0 # in miliseconds
        self.last_second_tracked = -1
        self.credits_earned = 0
    
    def track_duration(self):
        """Track the session duration."""

        now = pygame.time.get_ticks()
        self.session_duration += now - self.last_session_tick
        self.last_session_tick = now
        
__all__ = ["State"]