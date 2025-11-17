"""
A module containing the MusicPlayer class
for playing music from sequences of Sounds.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game

from pathlib import Path
import json

import pygame
from pygame.mixer import Channel, Sound

from ..utils import config, events

class MusicPlayer():
    """A class which handles playing music from a sequence of sounds."""

    def __init__(self, game: Game) -> None:
        """Initialize the music player."""

        self.game: Game = game

        pygame.mixer.set_reserved(4)

        self.drum_ch = Channel(0)
        self.bass_ch = Channel(1)
        self.chrd_ch = Channel(2)
        self.mldy_ch = Channel(3)

        self.set_volume()

        self.current_step: int = 0

        self.drum_snd: Sound | None = None
        self.bass_snd: Sound | None = None
        self.chrd_snd: Sound | None = None
        self.mldy_snd: Sound | None = None

        self.sequence_sounds: list[str] = []
        self.sequence: list[list[int]] = []
    
    def load_sequence(self,
                      file_name: str,
                      loop_sequence: bool = False,
                      autoplay: bool = True
                      ) -> None:
        """Load a sequence of sounds."""

        path = Path(config.sequences_path, file_name)
        if not path.exists():
            print(f"No sequence at: {path}")
            return
        
        contents = None
        try:
            contents = json.loads(path.read_text())
        except Exception as e:
            print(f"Encountered an error while parsing sequence contents:\n{e}")
            return
        
        if contents is None:
            print("Contents of sequence is 'None'.")
            return
        
        self.sequence_sounds = contents['sounds']
        self.sequence = contents['sequence']

        self.max_step = len(self.sequence) - 1
        self.loop_sequence = loop_sequence

        self.reset_sequence()

        if autoplay:
            self.update()
    
    def _load_step(self, step: int | None = None) -> None:
        """Load the sounds for the given step."""

        if step is None:
            step = self.current_step + 1
        
        if step > self.max_step:
            return

        dir = config.sounds_path
        drum = self.sequence_sounds[self.sequence[step][0]]
        bass = self.sequence_sounds[self.sequence[step][1]]
        chrd = self.sequence_sounds[self.sequence[step][2]]
        mldy = self.sequence_sounds[self.sequence[step][3]]
        self.drum_snd = None if not drum else Sound(Path(dir, drum))
        self.bass_snd = None if not bass else Sound(Path(dir, bass))
        self.chrd_snd = None if not chrd else Sound(Path(dir, chrd))
        self.mldy_snd = None if not mldy else Sound(Path(dir, mldy))

        self._insert_silence()
    
    def _insert_silence(self) -> None:
        """
        Insert silence if no sounds are loaded,
        to prevent skipping to the next part before it's time.
        """

        if self.drum_snd is None:
            dir = config.sounds_path
            self.drum_snd = Sound(Path(dir, "silence.wav"))

    def _play(self) -> None:
        """Play the loaded sounds."""

        if self.current_step > self.max_step:
            return
        
        if self.drum_snd:
            self.drum_ch.play(self.drum_snd)
            self.drum_ch.set_endevent(events.MUSIC_STEP_FINISHED)
        if self.bass_snd:
            self.bass_ch.play(self.bass_snd)
        if self.chrd_snd:
            self.chrd_ch.play(self.chrd_snd)
        if self.mldy_snd:
            self.mldy_ch.play(self.mldy_snd)
    
    def reset_sequence(self) -> None:
        """Set the sequence to step 0."""
        self.stop()
        self.current_step = 0
        self._load_step(0)
    
    def pause(self) -> None:
        """Pauses playback on all channels."""

        self.drum_ch.pause()
        self.bass_ch.pause()
        self.chrd_ch.pause()
        self.mldy_ch.pause()
    
    def unpause(self) -> None:
        """Resumes playback on all channels."""

        self.drum_ch.unpause()
        self.bass_ch.unpause()
        self.chrd_ch.unpause()
        self.mldy_ch.unpause()
    
    def stop(self) -> None:
        """Stop playback on all channels."""

        self.drum_ch.set_endevent()
        self.drum_ch.stop()
        self.bass_ch.stop()
        self.chrd_ch.stop()
        self.mldy_ch.stop()
    
    def set_volume(self, volume: int | None = None) -> None:
        """Sets the volume for all channels."""

        if volume is None:
            volume = self.game.settings.data['music_volume']
        
        if volume < 0:
            volume = 0
        elif volume > 10:
            volume = 10
        
        self.drum_ch.set_volume(volume * 0.1)
        self.bass_ch.set_volume(volume * 0.1)
        self.chrd_ch.set_volume(volume * 0.1)
        self.mldy_ch.set_volume(volume * 0.1)
    
    def update(self) -> None:
        """
        Update the music player. Play step, load next, increment step.
        """

        if self.loop_sequence and self.current_step > self.max_step:
            self.reset_sequence()
        
        if self.current_step > self.max_step:
            return

        self._play()
        self._load_step()
        self.current_step += 1

__all__ = ["MusicPlayer"]
