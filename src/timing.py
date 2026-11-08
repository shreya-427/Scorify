from models import NoteEvent, QuantizedNote

#converts the seconds to quater note beats, after removing count in time
def seconds_to_beats(
    notes: list[NoteEvent], bpm: float, lead_in_s: float = 0.0
) -> list[QuantizedNote]:
    result = []
    beats_per_sec = bpm/60
    for note in notes:
        #count in time subtracted from beg and end
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