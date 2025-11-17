"""
A module which contains classes for spawning aliens randomly or in waves.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

from random import randint, choice

from ..entities import Alien

class SpawnManager():
    """A class which manages the spawning of aliens."""

    def __init__(self, game: Game) -> None:
        """Initialize the spawn manager."""

        self.game: Game = game

        self.random_spawn_delay: float = 2000 # ms
        self.random_spawn_cooldown: float = self.random_spawn_delay
        self.random_spawn_count: int = 1

        self.random_spawns: dict[int, tuple[type[Alien]]] = {
            1: (Alien,),
            # TODO: add more aliens when more alien classes are made
        }

        self.waves: dict[int, type[AlienWave]] = {
            5: AlienWave,
            # TODO: add more waves when more alien classes are made
        }
    
    def level_up(self, level: int | None = None) -> None:
        """Reduces spawn delay and/or increases spawn count."""

        if level is None:
            level = self.game.state.level

        # TODO: refine the level up logic, just reducing delay for now
        self.random_spawn_delay *= 0.95
    
    def spawn_random(self) -> None:
        """Spawns a number of randomly chosen enemies."""

        if self.random_spawn_cooldown < self.random_spawn_delay:
            self.random_spawn_cooldown += self.game.dt * 1000
            return

        level = self.game.state.level
        if level > max(self.random_spawns.keys()):
            level = max(self.random_spawns.keys())

        for _ in range (self.random_spawn_count):
            alien_class = choice(self.random_spawns[level])
            alien = alien_class(self.game)
            alien.x = randint(0, self.game.play_surf.width - alien.rect.width)
            self.game.aliens.add(alien)
        
        self.random_spawn_cooldown = 0
    
    def spawn_wave(self, level: int | None = None) -> None:
        """Spawns a preset wave of aliens all at once."""
        
        if level is None:
            level = self.game.state.level
        
        if level in self.waves:
            wave = self.waves[level](self.game)
            wave.deploy()

class WaveSetup(TypedDict):
    """
    A class representing a dictionary containing information on a
    single alien in a presest wave.
    """

    alien_class: type[Alien]
    x_mod: int
    y_mod: int
    
class AlienWave():
    """A class representing a preset spawn of aliens."""

    def __init__(self, game: Game) -> None:
        """Initialize the wave."""

        self.game: Game = game

        self.aliens: list[Alien] = []
        # arranged in a + pattern
        self.setup_data: tuple[WaveSetup, ...] = (
            {'alien_class': Alien, 'x_mod': 0, 'y_mod': -2},
            {'alien_class': Alien, 'x_mod': -1, 'y_mod': -1},
            {'alien_class': Alien, 'x_mod': 1, 'y_mod': -1},
            {'alien_class': Alien, 'x_mod': 0, 'y_mod': 0},
        )

        for datum in self.setup_data:
            alien = datum['alien_class'](self.game)
            alien.x += alien.rect.width * datum['x_mod']
            alien.bounds['top'] = round(alien.y + alien.rect.height * datum['y_mod'])
            alien.y = alien.bounds['top']
            self.aliens.append(alien)
    
    def deploy(self) -> None:
        """Spawn the wave."""

        for alien in self.aliens:
            self.game.aliens.add(alien)
        
__all__ = ["SpawnManager"]
