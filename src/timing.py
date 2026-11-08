from models import NoteEvent, QuantizedNote

# Convert seconds to quarter-note beats, starting at the first note by default.
def seconds_to_beats(
    notes: list[NoteEvent], bpm: float, lead_in_s: float | None = None
) -> list[QuantizedNote]:
    if not notes:
        return []

    if lead_in_s is None:
        lead_in_s = min(note.start_sec for note in notes)

    result = []
    beats_per_sec = bpm/60
    for note in notes:
        # Shift both endpoints to preserve durations and gaps between notes.
        start_s = note.start_sec - lead_in_s
        end_s = note.end_sec - lead_in_s

        if start_s < 0:
            continue  # note began during the count-in, so drop it

        result.append(
            QuantizedNote(
                pitch=note.pitch,
                start_beat=start_s * beats_per_sec,
                end_beat=end_s * beats_per_sec,
            )
        )
    return result
