"""A module containing classes for playing music."""

from pathlib import Path
import pygame
from pygame.mixer import Channel, Sound

class MusicPlayer():
    """A class which handles playing music from a sequence of sounds."""

    def __init__(self, game):
        """Initialize the music player."""

        self.game = game

        pygame.mixer.set_reserved(4)

        self.drum_ch = Channel(0)
        self.bass_ch = Channel(1)
        self.chrd_ch = Channel(2)
        self.mldy_ch = Channel(3)

        self.current_step = None

        self.drum_snd = None
        self.bass_snd = None
        self.chrd_snd = None
        self.mldy_snd = None

        # TODO: load the sequence from a file
        # a tuple of tuples, each inner tuple being a step in the seq.
        # indices of inner tuple same as channels
        # just strings for testing; drums and bass
        self.sequence = (
            ("drums.wav", "", "", "mel1.wav"),
            ("drums.wav", "", "", "mel1.wav"),
            ("drums.wav", "", "", "mel2.wav"),
            ("drums.wav", "", "", "mel2.wav"),
        )
        # TODO: set loop_sequence based on load_sequence method
        self.loop_sequence = False

        self.max_step = len(self.sequence) - 1
    
    def _load_step(self, step=None):
        """Load the sounds for the given step."""

        if step is None:
            step = self.current_step + 1
        
        if step > self.max_step:
            return False

        dir = self.game.config.sounds_path
        drum = self.sequence[step][0]
        bass = self.sequence[step][1]
        chrd = self.sequence[step][2]
        mldy = self.sequence[step][3]
        self.drum_snd = None if drum == "" else Sound(Path(dir, drum))
        self.bass_snd = None if bass == "" else Sound(Path(dir, bass))
        self.chrd_snd = None if chrd == "" else Sound(Path(dir, chrd))
        self.mldy_snd = None if mldy == "" else Sound(Path(dir, mldy))

        self._insert_silence()
    
    def _insert_silence(self):
        """
        Insert silence if no sounds are loaded,
        to prevent skipping to the next part before it's time.
        """

        if self.drum_snd is None:
            dir = self.game.config.sounds_path
            self.drum_snd = Sound(Path(dir, "silence.wav"))

    def _play(self):
        """Play the loaded sounds."""

        if self.current_step > self.max_step:
            return False
        
        if self.drum_snd:
            self.drum_ch.play(self.drum_snd, fade_ms=0)
            self.drum_ch.set_endevent(self.game.CH_DONE_PLAYING)
        if self.bass_snd:
            self.bass_ch.play(self.bass_snd, fade_ms=3)
        if self.chrd_snd:
            self.chrd_ch.play(self.chrd_snd, fade_ms=3)
        if self.mldy_snd:
            self.mldy_ch.play(self.mldy_snd, fade_ms=3)
    
    def reset_sequence(self):
        """Set the sequence to step 0."""
        self.drum_ch.set_endevent()
        self.current_step = 0
        self._load_step(0)
    
    def pause(self):
        """Pauses playback on all channels."""

        self.drum_ch.pause()
        self.bass_ch.pause()
        self.chrd_ch.pause()
        self.mldy_ch.pause()
    
    def unpause(self):
        """Resumes playback on all channels."""

        self.drum_ch.unpause()
        self.bass_ch.unpause()
        self.chrd_ch.unpause()
        self.mldy_ch.unpause()
    
    def update(self):
        """
        Update the music player. Play step, load next, increment step.
        """

        if self.loop_sequence and self.current_step > self.max_step:
            self.reset_sequence()
        
        if self.current_step > self.max_step:
            return False

        self._play()
        self._load_step()
        self.current_step += 1