from typing import Dict

from prediction.models.note_sequence import NoteSequence


class Composition:
    def __init__(self, voices: Dict[int, NoteSequence]) -> None:
        self.voices: Dict[int, NoteSequence] = voices

    @property
    def rh_voices(self) -> Dict[int, NoteSequence]:
        return {voice: seq for voice, seq in self.voices.items() if voice < 5}

    @property
    def lh_voices(self) -> Dict[int, NoteSequence]:
        return {voice: seq for voice, seq in self.voices.items() if voice >= 5}

    def flatten_voices(self) -> None:
        for seq in self.voices.values():
            seq.flatten()
