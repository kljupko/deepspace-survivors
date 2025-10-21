"""A module containing classes for playing music."""

class MusicPlayer():
    """A class which handles playing music from a sequence of sounds."""

    def __init__(self, game):
        """Initialize the music player."""

        self.game = game

        # TODO: assign channels to each track:
        #   0 = drums
        #   1 = bass
        #   2 = chord
        #   3 = melody

        self.current_step = 0

        self.drum_snd = None
        self.bass_snd = None
        self.chrd_snd = None
        self.mldy_snd = None

        # TODO: load the sequence from a file
        # a tuple of tuples, each inner tuple being a step in the seq.
        # indices of inner tuple same as channels
        # just strings for testing; drums and bass
        self.sequence = (
            ("one", "one", "", ""),
            ("two", "", "", ""),
            ("three", "", "", ""),
            ("four", "two", "", ""),
            ("five", "three", "", ""),
            ("six", "", "", ""),
            ("seven", "four", "", ""),
            ("eight", "", "", ""),
        )

        self.max_step = len(self.sequence) - 1
        self._load_step(0)
    
    def _load_step(self, step=None):
        """Load the sounds for the given step."""

        if step is None:
            step = self.current_step + 1
        
        if step > self.max_step:
            return False
        
        self.drum_snd = self.sequence[step][0]
        self.bass_snd = self.sequence[step][1]
        self.chrd_snd = self.sequence[step][2]
        self.mldy_snd = self.sequence[step][3]

        self._insert_silence()
    
    def _insert_silence(self):
        """
        Insert silence if no sounds are loaded,
        to prevent skipping to the next part before it's time.
        """

        if self.drum_snd is not None:
            return False
        if self.bass_snd is not None:
            return False
        if self.chrd_snd is not None:
            return False
        if self.mldy_snd is not None:
            return False
        
        self.drum_snd = "silence"

    def _play(self):
        """Play the loaded sounds."""

        if self.current_step > self.max_step:
            return False
        
        # TODO: replace prints with playing sounds
        if self.drum_snd:
            print(f"Drums: {self.drum_snd}")
        if self.bass_snd:
            print(f"Bass: {self.bass_snd}")
        if self.chrd_snd:
            print(f"Chord: {self.chrd_snd}")
        if self.mldy_snd:
            print(f"Melody: {self.mldy_snd}")
    
    def update(self):
        """
        Update the music player. Play step, load next, increment step.
        """

        self._play()
        self._load_step()
        self.current_step += 1