from models import QuantizedNote

#rounds a beat to the nearest grid size (default is 0.25 for sixteenth notes, which is the smallest note value we can notate now)
def snap_to_grid(beat, grid_size=0.25):
    return round(beat/grid_size)*grid_size

def quantize_note(note, grid_size=0.25):
    q_note = QuantizedNote(note.pitch, snap_to_grid(note.start_beat, grid_size), snap_to_grid(note.end_beat, grid_size))

    if q_note.start_beat >= q_note.end_beat:
        q_note.end_beat = q_note.start_beat + grid_size

    return q_note

def quantize_notes(notes, grid_size=0.25):
    quantized_notes = []
    for note in notes:
        quantized_notes.append(quantize_note(note, grid_size))

    #sorts notes by the start_beat
    quantized_notes = sorted(
        quantized_notes,
        key=lambda note: note.start_beat
    )

    for i in range(len(quantized_notes) - 2, -1, -1):
        if quantized_notes[i].end_beat > quantized_notes[i+1].start_beat:
            quantized_notes[i].end_beat = quantized_notes[i+1].start_beat
            if quantized_notes[i].end_beat == quantized_notes[i].start_beat:
                quantized_notes.pop(i)

    return quantized_notes


if __name__ == "__main__":
    test_notes = [
    QuantizedNote(60, 0.0, 1.0),
    QuantizedNote(62, 1.0, 2.0),
    QuantizedNote(64, 1.0, 2.5),
    QuantizedNote(65, 1.0, 3.0),
    QuantizedNote(67, 3.0, 4.0)
    ]

    result = quantize_notes(test_notes)

    for note in result:
        print(note)