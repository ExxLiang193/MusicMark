import argparse
import pprint
import random
import time
from decimal import FloatOperation, getcontext
from typing import List

from config import get_config
from data.generation.builders.note_sequence_permuter import NoteSequencePermuter
from data.generation.generate_data import generate_sequences
from data.generation.io.note_sequence_writer import NoteSequenceWriter
from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence
from prediction.io.readers.musicxml.musicxml_reader import MusicXMLReader
from prediction.io.writers.musicxml.musicxml_writer import MusicXMLWriter
from prediction.models.composition import Composition
from prediction.models.compressed_note_sequence import NoteSequenceCompressor
from prediction.models.note_sequence import NoteSequence
from prediction.nn.model_loader import load_model
from prediction.workers.gru_data_handler import GRUDataHandler

pp = pprint.PrettyPrinter(indent=4)


def enable_safe_float_handling() -> None:
    c = getcontext()
    c.traps[FloatOperation] = True


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--generate-data", action="store_true")
    parser.add_argument("--amount", "--amt", type=int)
    parser.add_argument("--length", "--len", type=int)
    parser.add_argument("--in-file", type=str)
    parser.add_argument("--out-file", type=str)
    parser.add_argument("--predict", action="store_true")
    parser.add_argument("--rh-model", type=str)
    parser.add_argument("--lh-model", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    enable_safe_float_handling()
    config = get_config()

    if args.generate_data:
        for is_rh, tag in ((True, "RH"), (False, "LH")):
            permuter = NoteSequencePermuter(generate_sequences(is_rh), stride=1, rh=is_rh)
            note_sequences = permuter.permute_random(int(args.length), int(args.amount) * 3)
            print("Note sequences generated:", len(note_sequences))
            sampled_data: List[AnnotatedNoteSequence] = random.sample(note_sequences, int(args.amount))
            print("Note sequences sampled:", len(sampled_data))
            out_file = f"{args.out_file.rstrip('.txt')}_{tag}.txt"
            NoteSequenceWriter(sampled_data).to_dsv(out_file)
            print("Written to:", out_file)
    elif args.predict:
        composition: Composition = MusicXMLReader(args.in_file).to_composition()
        rh_data_handler: GRUDataHandler = GRUDataHandler(load_model(args.rh_model, **config))
        lh_data_handler: GRUDataHandler = GRUDataHandler(load_model(args.lh_model, **config))

        sequence_compressor: NoteSequenceCompressor = NoteSequenceCompressor()
        rh_voices: NoteSequence = sequence_compressor.compress(composition.rh_voices)
        lh_voices: NoteSequence = sequence_compressor.compress(composition.lh_voices)

        t0 = time.time()
        rh_predicted_fingerings: List[int] = rh_data_handler.get_predictions(rh_voices)
        lh_predicted_fingerings: List[int] = lh_data_handler.get_predictions(lh_voices)

        for note, fingering in zip(reversed(rh_voices.notes), reversed(rh_predicted_fingerings)):
            if fingering is not None:
                note.fingering = fingering

        for note, fingering in zip(reversed(lh_voices.notes), reversed(lh_predicted_fingerings)):
            if fingering is not None:
                note.fingering = fingering

        print(f"Fingerings computed in: {round(time.time() - t0, 2)} sec")

        composition.flatten_voices()
        MusicXMLWriter(args.in_file).set_predictions(composition.voices)
