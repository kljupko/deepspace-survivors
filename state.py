import pygame

class State():
    """Represents a class which contains the game's current state."""

    def __init__(self):
        """Initialize the game state object."""

        self.running = False
        self.session_duration = 0 # in miliseconds
        self.credits = 0
    
    def track_duration(self):
        """Track the session duration."""

        self.session_duration = pygame.time.get_ticks()