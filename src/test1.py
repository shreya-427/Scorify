from timing import seconds_to_beats
from models import NoteEvent

note = [NoteEvent(pitch=60, start_sec=1.37, end_sec=1.81)]
print(seconds_to_beats(note, bpm=100))