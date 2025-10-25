"""
A module containing the MusicPlayer class
for playing music from sequences of Sounds.
"""

from pathlib import Path
import json
import pygame
from pygame.mixer import Channel, Sound

from ..systems import events

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

        self.set_volume()

        self.current_step = None

        self.drum_snd = None
        self.bass_snd = None
        self.chrd_snd = None
        self.mldy_snd = None

        self.sequence_sounds = None
        self.sequence = None
    
    def load_sequence(self, file_name, loop_sequence=False, autoplay=True):
        """Load a sequence of sounds."""

        path = Path(self.game.config.sequences_path, file_name)
        if not path.exists():
            print(f"No sequence at: {path}")
            return False
        
        contents = None
        try:
            contents = json.loads(path.read_text())
        except Exception as e:
            print(f"Encountered an error while parsing sequence contents:\n{e}")
            return False
        
        if contents is None:
            print("Contents of sequence is 'None'.")
            return False
        
        self.sequence_sounds = contents['sounds']
        self.sequence = contents['sequence']

        self.max_step = len(self.sequence) - 1
        self.loop_sequence = loop_sequence

        self.reset_sequence()

        if autoplay:
            self.update()
    
    def _load_step(self, step=None):
        """Load the sounds for the given step."""

        if step is None:
            step = self.current_step + 1
        
        if step > self.max_step:
            return False

        dir = self.game.config.sounds_path
        drum = self.sequence_sounds[self.sequence[step][0]]
        bass = self.sequence_sounds[self.sequence[step][1]]
        chrd = self.sequence_sounds[self.sequence[step][2]]
        mldy = self.sequence_sounds[self.sequence[step][3]]
        self.drum_snd = None if not drum else Sound(Path(dir, drum))
        self.bass_snd = None if not bass else Sound(Path(dir, bass))
        self.chrd_snd = None if not chrd else Sound(Path(dir, chrd))
        self.mldy_snd = None if not mldy else Sound(Path(dir, mldy))

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
            self.drum_ch.play(self.drum_snd)
            self.drum_ch.set_endevent(events.MUSIC_STEP_FINISHED)
        if self.bass_snd:
            self.bass_ch.play(self.bass_snd)
        if self.chrd_snd:
            self.chrd_ch.play(self.chrd_snd)
        if self.mldy_snd:
            self.mldy_ch.play(self.mldy_snd)
    
    def reset_sequence(self):
        """Set the sequence to step 0."""
        self.stop()
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
    
    def stop(self):
        """Stop playback on all channels."""

        self.drum_ch.set_endevent()
        self.drum_ch.stop()
        self.bass_ch.stop()
        self.chrd_ch.stop()
        self.mldy_ch.stop()
    
    def set_volume(self, volume=None):
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

__all__ = ["MusicPlayer"]