import argparse
import random
from typing import List

from data.generation.builders.note_sequence_permuter import NoteSequencePermuter
from data.generation.generate_data import generate_sequences
from data.generation.io.note_sequence_writer import NoteSequenceWriter
from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--generate-data", action="store_true")
    parser.add_argument("--amount", "--amt", type=int)
    parser.add_argument("--out-file", type=str, default="data/note_sequences.txt")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.generate_data:
        permuter = NoteSequencePermuter(generate_sequences(), stride=1)
        note_sequences = permuter.permute_random(10, int(1e6))
        print("Note sequences generated:", len(note_sequences))
        sampled_data: List[AnnotatedNoteSequence] = random.sample(note_sequences, int(args.amount))
        print("Note sequences sampled:", len(sampled_data))
        NoteSequenceWriter(sampled_data).to_dsv(args.out_file)
        print("Written to:", args.out_file)
