from __future__ import annotations

import heapq as h
from collections import namedtuple
from typing import Dict, List, Set, Tuple

from prediction.models.chord import Chord
from prediction.models.note import Note
from prediction.models.note_sequence import NoteSequence

MomentInfo = namedtuple("MomentInfo", ("time", "abs_position", "data", "voice", "seq_idx"))


class NoteSequenceCompressor:
    def compress(self, voices: Dict[int, NoteSequence]) -> NoteSequence:
        # for voice in voices.values():
        #     voice.optimize()
        result: NoteSequence = NoteSequence()

        cur_moments: List[MomentInfo] = list()
        for voice, seq in voices.items():
            target: Note | Chord = seq.notes[0]
            init_notes: List[Note] = [target] if isinstance(target, Note) else target.notes
            for note in init_notes:
                h.heappush(
                    cur_moments,
                    MomentInfo(
                        time=note.duration.raw_duration,
                        abs_position=float("inf") if note.is_rest() else note.position.abs_position,
                        data=note,
                        voice=voice,
                        seq_idx=0,
                    ),
                )

        while cur_moments:
            primed_voices: Set[Tuple[int, int]] = set()
            cur_moment_info: MomentInfo = h.heappop(cur_moments)

            primed_voices.add((cur_moment_info.voice, cur_moment_info.seq_idx + 1))
            if (not cur_moment_info.data.is_rest()) or all(moment.data.is_rest() for moment in cur_moments):
                result.append_note(cur_moment_info.data)

            while cur_moments and cur_moments[0].time == cur_moment_info.time:
                next_moment_info: MomentInfo = h.heappop(cur_moments)

                primed_voices.add((next_moment_info.voice, next_moment_info.seq_idx + 1))
                if not next_moment_info.data.is_rest():
                    result.append_note(next_moment_info.data)

            for moment in cur_moments:
                if not moment.data.is_rest():
                    result.append_note(moment.data)

            for voice, seq_idx in primed_voices:
                if seq_idx >= len(voices[voice]):
                    continue
                target: Note | Chord = voices[voice].notes[seq_idx]
                next_notes: List[Note] = [target] if isinstance(target, Note) else target.notes
                for note in next_notes:
                    h.heappush(
                        cur_moments,
                        MomentInfo(
                            time=cur_moment_info.time + note.duration.raw_duration,
                            abs_position=float("inf") if note.is_rest() else note.position.abs_position,
                            data=note,
                            voice=voice,
                            seq_idx=seq_idx,
                        ),
                    )

        return result
