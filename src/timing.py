from models import NoteEvent, QuantizedNote
#
#converts seconds to quarter note beats
def seconds_to_beats(
    notes: list[NoteEvent], bpm: float, lead_in_s: float = 0.0
) -> list[QuantizedNote]:
    result = []
    for note in notes:
        ...  # TODO: subtract lead_in_s from start and end, convert both to beats,
             # and append a BeatNote (keyword arguments)
    return result