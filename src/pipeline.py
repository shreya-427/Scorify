import argparse

from models import QuantizedNote
from transcribe import transcribe
from timing import seconds_to_beats
from quantize import quantize_notes 
from score import create_score   

def run_pipeline( audio_path: str, bpm: float, title:str,composer:str| None = None):

    transcribed_notes = transcribe(audio_path)

    prelim_quantized_notes = seconds_to_beats(transcribed_notes, bpm)

    quantized_notes= quantize_notes(prelim_quantized_notes)

    score = create_score(quantized_notes, bpm, title,composer).write("musicxml", fp="test_score.xml")

    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path")
    parser.add_argument("--bpm", type=float, required=True)
    parser.add_argument("--lead-in", type=float, help="Override the automatic first-note start (seconds)")
    args = parser.parse_args()

    for note in run_pipeline(args.audio_path, args.bpm, args.lead_in):
        print(note)
