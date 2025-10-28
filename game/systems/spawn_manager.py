"""
A module which contains classes for spawning aliens randomly or in waves.
"""

from random import randint, choice

from ..entities import Alien

class SpawnManager():
    """A class which manages the spawning of aliens."""

    def __init__(self, game):
        """Initialize the spawn manager."""

        self.game = game

        self.random_spawn_delay = 2000 # ms
        self.random_spawn_cooldown = self.random_spawn_delay
        self.random_spawn_count = 1

        self.random_spawns = {
            1: (Alien,),
            # TODO: add more aliens when more alien classes are made
        }

        self.waves = {
            5: AlienWave,
            # TODO: add more waves when more alien classes are made
        }
    
    def level_up(self, level=None):
        """Reduces spawn delay and/or increases spawn count."""

        if level is None:
            level = self.game.state.level

        # TODO: refine the level up logic, just reducing delay for now
        self.random_spawn_delay *= 0.95
    
    def spawn_random(self):
        """Spawns a number of randomly chosen enemies."""

        if self.random_spawn_cooldown < self.random_spawn_delay:
            self.random_spawn_cooldown += self.game.dt * 1000
            return False

        level = self.game.state.level
        if level > max(self.random_spawns.keys()):
            level = max(self.random_spawns.keys())

        for _ in range (self.random_spawn_count):
            alien_class = choice(self.random_spawns[level])
            alien = alien_class(self.game)
            alien.x = randint(0, self.game.play_surf.width - alien.rect.width)
            self.game.aliens.add(alien)
        
        self.random_spawn_cooldown = 0
    
    def spawn_wave(self, level=None):
        """Spawns a preset wave of aliens all at once."""
        
        if level is None:
            level = self.game.state.level
        
        if level in self.waves:
            wave = self.waves[level](self.game)
            wave.deploy()

class AlienWave():
    """A class representing a preset spawn of aliens."""

    def __init__(self, game):
        """Initialize the wave."""

        self.game = game

        self.aliens = []
        # arranged in a + pattern
        self.setup_data = (
            {'class': Alien, 'x_mod': 0, 'y_mod': -2},
            {'class': Alien, 'x_mod': -1, 'y_mod': -1},
            {'class': Alien, 'x_mod': 1, 'y_mod': -1},
            {'class': Alien, 'x_mod': 0, 'y_mod': 0},
        )

        for data in self.setup_data:
            alien = data['class'](self.game)
            alien.x += alien.rect.width * data['x_mod']
            alien.bounds['top'] = alien.y + alien.rect.height * data['y_mod']
            alien.y = alien.bounds['top']
            self.aliens.append(alien)
    
    def deploy(self):
        """Spawn the wave."""

        for alien in self.aliens:
            self.game.aliens.add(alien)
        
__all__ = ["SpawnManager"]