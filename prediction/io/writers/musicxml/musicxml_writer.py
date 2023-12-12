from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Dict, List

from prediction.models.note_sequence import NoteSequence


class MusicXMLWriter:
    NEW_FILE_SUFFIX = "_annotated"
    FILE_EXTENSION = ".musicxml"

    def __init__(self, file_name: str, version: str = "3.1") -> None:
        self.file_name: str = file_name
        self._version: str = version

    def _build_fingering_element(self, fingering: int) -> ET.Element:
        """
        <notations>
          <technical>
            <fingering placement="below">1</fingering>
          </technical>
        </notations>
        """
        notations_element: ET.Element = ET.Element("notations")
        technical_element: ET.Element = ET.SubElement(notations_element, "technical")
        fingering_element: ET.Element = ET.SubElement(technical_element, "fingering")
        fingering_element.text = str(fingering)
        return notations_element

    def set_predictions(self, matches: Dict[int, NoteSequence], write=True) -> str:
        xml_root: ET.Element = ET.parse(self.file_name).getroot()
        measures: List[ET.Element] = xml_root.findall("part/measure")
        native_voice_pos: Dict[int, int] = {voice: 0 for voice in matches.keys()}
        for measure_element in measures:
            for note_element in measure_element.findall("note"):
                voice_idx: int = int(note_element.find("voice").text)
                target_native_note = matches[voice_idx].notes[native_voice_pos[voice_idx]]
                if (tie_element := note_element.find("tie")) is not None and tie_element.attrib["type"] == "stop":
                    continue
                if target_native_note.is_tagged():
                    if target_native_note.fingering is not None:
                        note_element.append(self._build_fingering_element(target_native_note.fingering))
                    native_voice_pos[voice_idx] += 1

        # Duplicating XML tree
        new_xml_tree = ET.ElementTree(xml_root)
        new_file_name = self.file_name.rstrip(self.FILE_EXTENSION) + self.NEW_FILE_SUFFIX + self.FILE_EXTENSION
        if write:
            new_xml_tree.write(new_file_name)
            print("Written to:", new_file_name)
        return new_file_name
