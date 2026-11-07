from dataclasses import dataclass

@dataclass
class NoteEvent:
    pitch: int
    start_sec: float
    end_sec: float
    amplitude: float = 1.0

@dataclass
class QuantizedNote:
    pitch: int
    start_beat: float
    end_beat: float
