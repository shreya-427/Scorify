from models import NoteEvent, QuantizedNote


def seconds_to_beats(notes: list[NoteEvent], bpm: float) -> list[QuantizedNote]:
    """Convert seconds to quarter-note beats, with the first note starting at beat 0."""
    if not notes:
        return []

    beats_per_sec = bpm / 60
    origin = min(n.start_sec for n in notes)   # the zero point of the timeline

    result = []
    for note in notes:
        result.append(
            QuantizedNote(
                pitch=note.pitch,
                start_beat=(note.start_sec - origin) * beats_per_sec,
                end_beat=(note.end_sec - origin) * beats_per_sec,
            )
        )
    return result