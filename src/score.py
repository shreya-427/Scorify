from music21 import stream, note, meter, clef

# creating a new emtpy score
score = stream.Score()

# create a new part for the score
part = stream.Part()

# adding clef and time signature to part
part.append(clef.TrebleClef())
part.append(meter.TimeSignature('4/4'))

#create notes
for pitch in [60, 62, 64, 65, 67, 69, 71, 72]:  # C4, D4, E4, F4, G4, A4, B4, C5
    n = note.Note(pitch)
    n.quarterLength = 1.0  # each note is a quarter note
    part.append(n)

# add the part to the score
score.append(part)

# export as MusicXML file
score.write('musicxml', fp='test_score.xml')