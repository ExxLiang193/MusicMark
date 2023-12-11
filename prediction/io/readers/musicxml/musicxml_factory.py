from __future__ import annotations

import xml.etree.ElementTree as ET
from decimal import Decimal
from typing import TYPE_CHECKING

from prediction.models.duration import Duration
from prediction.models.note import Note
from prediction.models.note_name import NoteName
from prediction.models.tagged.note import TaggedNote
from prediction.models.time_signature import TimeSignature

if TYPE_CHECKING:
    from prediction.models.position import Position


class MusicXMLFactory:
    def __init__(self, duration_scale: Decimal) -> None:
        Duration.set_scale(duration_scale)

    def build_note(self, note_element: ET.Element, note_id: int) -> Note:
        pitch_element: ET.Element = note_element.find("pitch")
        step: str = pitch_element.find("step").text
        alter: int = 0 if (alter := pitch_element.find("alter")) is None else int(alter.text)
        octave: int = int(pitch_element.find("octave").text)
        position: Position = NoteName.from_raw(step, alter).as_position(octave)
        duration: Decimal = Decimal(note_element.find("duration").text)
        tied: bool = (tie_element := note_element.find("tie")) is not None and (tie_element.attrib["type"] == "stop")
        return TaggedNote.from_raw(position.abs_position, duration, [note_id], tied)

    def build_rest(self, note_element: ET.Element, note_id: int) -> Note:
        duration: Decimal = Decimal(note_element.find("duration").text)
        return TaggedNote.from_raw(None, duration, [note_id])

    def build_default_rest(self, time_signature: TimeSignature) -> Note:
        return Note.from_raw(None, time_signature.real_measure_duration * Duration.SCALE)

    def build_time_signature(self, time_element: ET.Element) -> TimeSignature:
        beat_count: int = int(time_element.find("beats").text)
        raw_beat_duration: Decimal = Decimal(time_element.find("beat-type").text)
        return TimeSignature.from_raw(beat_count, raw_beat_duration)
