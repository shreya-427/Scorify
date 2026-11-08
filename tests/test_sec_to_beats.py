from timing import seconds_to_beats
from models import NoteEvent

note = [NoteEvent(pitch=60, start_sec=2.4, end_sec=3.0)]
print(seconds_to_beats(note, bpm=100, lead_in_s=2.4))