import sys
from basic_pitch.inference import predict
from models import NoteEvent

MIN_DURATION_SEC = 0.08   # shorter than this counts as "short"
MIN_AMPLITUDE = 0.30      # weaker than this counts as "weak"

#removes any noise or overtone's mistaken for a note
def remove_ghost_notes(notes: list[NoteEvent]) -> list[NoteEvent]:
    kept = []
    for note in notes:
        duration = note.end_sec - note.start_sec
        is_short = duration < MIN_DURATION_SEC
        #how strongly a note is  (0.1-0.3 is prob ghost node)
        is_weak = note.amplitude < MIN_AMPLITUDE
        if not (is_short and is_weak):
            kept.append(note)
    return kept

#turns a filepath into a clean, sorted list of NoteEvent objects
def transcribe(audio_path: str) -> list[NoteEvent]:
    _, _, note_events = predict(audio_path)

    notes = []
    for start, end, pitch, amplitude, _bends in note_events:
        notes.append(
            NoteEvent(
                pitch=int(pitch),
                start_sec=float(start),
                end_sec=float(end),
                amplitude=float(amplitude),
            )
        )

    #sorts the data by start time
    notes.sort(key=lambda n: n.start_sec)
    #removes any noise and returns clean notes
    notes = remove_ghost_notes(notes)
    # TODO: merge split notes, resolve overlaps
    return notes

    return notes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python src/transcribe.py <audio_file>")
        sys.exit(1)

    for note in transcribe(sys.argv[1]):
        print(note)