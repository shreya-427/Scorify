import sys
from basic_pitch.inference import predict
from models import NoteEvent
from dataclasses import replace

MIN_DURATION_SEC = 0.08   # shorter than this counts as "short"
MIN_AMPLITUDE = 0.30      # weaker than this counts as "weak"
MERGE_GAP_SEC = 0.05    # same-pitch notes closer than this become one note
SAME_ONSET_SEC = 0.05   # overlapping notes starting this close are rival detections

#join notes that basic pitch might've separated (looks for same pitch with a tiny gap in between)
def merge_split_notes(notes: list[NoteEvent]) -> list[NoteEvent]:
    """Join consecutive same-pitch notes separated by a tiny gap (or an overlap)."""
    merged = []
    for note in notes:
        if merged:
            prev = merged[-1]
            gap = note.start_sec - prev.end_sec
            #if prev note has the same pitch and the gap between 2 notes is small
            if note.pitch == prev.pitch and gap < MERGE_GAP_SEC:
                merged[-1] = replace(
                    prev,
                    end_sec=max(prev.end_sec, note.end_sec),
                    amplitude=max(prev.amplitude, note.amplitude),
                )
                continue
        merged.append(note)
    return merged

#enforces that only one note can be playing at a time (for melody only)
#if 2 notes runtime overlaps, figures out if its 2 different notes --> if it is it trims the timing so they don't overlap
#
def resolve_overlaps(notes: list[NoteEvent]) -> list[NoteEvent]:
    """Make a monophonic line: no note may start before the previous one ends."""
    result = []
    for note in notes:
        if result and note.start_sec < result[-1].end_sec:
            prev = result[-1]
            if note.start_sec - prev.start_sec < SAME_ONSET_SEC:
                # Two detections of the same onset (e.g. an octave error): keep the stronger.
                #if notes overlap, and start times dif is small, keep the note w/ strong amp
                if note.amplitude > prev.amplitude:
                    result[-1] = note
                continue
            # Genuine next note: cut the earlier note short where the new one begins.
            result[-1] = replace(prev, end_sec=note.start_sec)
        result.append(note)
    return result


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
    notes = remove_ghost_notes(notes) #removes ghost notes
    notes = merge_split_notes(notes)  #
    notes = resolve_overlaps(notes)   #
    return notes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python src/transcribe.py <audio_file>")
        sys.exit(1)

    for note in transcribe(sys.argv[1]):
        print(note)