# pipeline.py
import argparse

from models import QuantizedNote
from transcribe import transcribe
from timing import seconds_to_beats

# Teammate's functions. Until quantize.py is ready, use pass-through stand-ins
# so you can run the rest of the chain.
try:
    from quantize import quantize, fix_overlaps_and_gaps
except ImportError:
    def quantize(notes):
        return notes

    def fix_overlaps_and_gaps(notes):
        return notes


def run_pipeline(
    audio_path: str, bpm: float, lead_in_s: float = 0.0
) -> list[QuantizedNote]:
    notes = transcribe(audio_path)
    ...  # TODO: seconds_to_beats -> quantize -> fix_overlaps_and_gaps
    return ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path")
    parser.add_argument("--bpm", type=float, required=True)
    parser.add_argument("--lead-in", type=float, default=0.0)
    args = parser.parse_args()

    for note in run_pipeline(args.audio_path, args.bpm, args.lead_in):
        print(note)
