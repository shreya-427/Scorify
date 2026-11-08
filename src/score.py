from music21 import stream, note, meter, clef, tempo, metadata
from models import QuantizedNote


def create_score(quantized_notes, bpm, title="Untitled", composer=""):
    score = stream.Score()

    # Title and composer, printed at the top of the sheet music
    score.metadata = metadata.Metadata()
    score.metadata.title = title
    if composer:
        score.metadata.composer = composer

    part = stream.Part()

    part.insert(0, clef.TrebleClef())
    part.insert(0, meter.TimeSignature("4/4"))
    part.insert(0, tempo.MetronomeMark(number=bpm))

    current_beat = 0.0

    for qnote in sorted(quantized_notes, key=lambda n: n.start_beat):
        # Check for silence before this note
        if qnote.start_beat > current_beat:
            rest_duration = qnote.start_beat - current_beat

            new_rest = note.Rest()
            new_rest.quarterLength = rest_duration
            part.insert(current_beat, new_rest)

        # Create the musical note
        new_note = note.Note(qnote.pitch)
        new_note.quarterLength = qnote.end_beat - qnote.start_beat

        part.insert(qnote.start_beat, new_note)

        # Track where the note ends
        current_beat = max(current_beat, qnote.end_beat)

    score.insert(0, part)
    return score


# This test code runs when the file is executed directly, but not when another file imports it
if __name__ == "__main__":
    test_notes = [
        QuantizedNote(60, 0.0, 1.0),
        QuantizedNote(62, 2.0, 3.0),
    ]

    result = create_score(test_notes, bpm=100, title="Test Piece", composer="Test Composer")
    result.write("musicxml", fp="test_score2.xml")

    print("Score generated successfully!")


# from music21 import stream, note, meter, clef
# from models import QuantizedNote
# from music21 import metadata

# # score.metadata = metadata.Metadata()
# # score.metadata.title = title
# # score.metadata.composer = composer

# def create_score(quantized_notes):
#     score = stream.Score()
#     part = stream.Part()

#     part.insert(0, clef.TrebleClef())
#     part.insert(0, meter.TimeSignature("4/4"))

#     current_beat = 0.0

#     for qnote in sorted(
#         quantized_notes,
#         key=lambda n: n.start_beat
#     ):
#         # Check for silence before this note
#         if qnote.start_beat > current_beat:
#             rest_duration = qnote.start_beat - current_beat

#             new_rest = note.Rest()
#             new_rest.quarterLength = rest_duration
#             part.insert(current_beat, new_rest)

#         # Create the musical note
#         new_note = note.Note(qnote.pitch)
#         new_note.quarterLength = (
#             qnote.end_beat - qnote.start_beat
#         )

#         part.insert(qnote.start_beat, new_note)

#         # Track where the note ends
#         current_beat = max(current_beat, qnote.end_beat)

#     score.insert(0, part)
#     return score


# # says that this test code runs when file is exectued directly, but not when another file imports it
# if __name__ == "__main__":
#     test_notes = [
#         QuantizedNote(60, 0.0, 1.0),
#         QuantizedNote(62, 2.0, 3.0)
#     ]

#     result = create_score(test_notes)
#     result.write("musicxml", fp="test_score2.xml")

#     print("Score generated successfully!")