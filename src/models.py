from dataclasses import dataclass

@dataclass
class NoteEvent:
    pitch: int
    start_sec: float
    end_sec: float

@dataclass
class QuantizedNote:
    pitch: int
    start_beat: float
    end_beat: float
