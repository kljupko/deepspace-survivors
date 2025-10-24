"""Module which contains the class in charge of touch/ mouse controls."""

import pygame

class Touch():
    """A class that represents the touch/ mouse controls."""

    def __init__(self):
        """Initialize the controls."""

        self.start_pos = None
        self.current_pos = None
        self.touch_start_ts = None
        self.touch_duration = None
    
    def register_mousedown_event(self, event):
        """Register that the user has touched/ clicked the screen."""

        self.start_pos = event.pos
        self.current_pos = event.pos
        self.touch_start_ts = pygame.time.get_ticks()
        self.touch_duration = 0
    
    def register_mouseup_event(self):
        """Register that the user is no longer touching the screen."""

        self.start_pos = None
        self.current_pos = None
        self.touch_start_ts = None
        self.touch_duration = None
    
    def register_mousemove_event(self, event):
        """Register that the user has moved the mouse/ finger."""

        self.current_pos = event.pos
    
    def track_touch_duration(self):
        """Track how long the user has held the mouse/ finger down."""

        if self.touch_start_ts:
            self.touch_duration = pygame.time.get_ticks() - self.touch_start_ts
    
    def __str__(self):
        """Returns a readable string containing touch info."""

        return f"""
Touch object:
    Start position:     {self.start_pos}
    Current position:   {self.current_pos}
    Touch duration:     {self.touch_duration}
"""

__all__ = ["Touch"]