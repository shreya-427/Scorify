# tests/test_timing.py
import pytest
from models import NoteEvent, QuantizedNote
from timing import seconds_to_beats


def test_basic_conversion():
    notes = [NoteEvent(pitch=60, start_sec=1.37, end_sec=1.81)]
    result = seconds_to_beats(notes, bpm=100)
    assert result[0].start_beat == pytest.approx(2.2833, abs=0.001)
    assert result[0].end_beat == pytest.approx(3.0167, abs=0.001)


def test_returns_beatnotes_and_keeps_pitch():
    notes = [NoteEvent(pitch=67, start_sec=0.0, end_sec=0.6)]
    result = seconds_to_beats(notes, bpm=100)
    assert isinstance(result[0], QuantizedNote)
    assert result[0].pitch == 67


def test_one_beat_at_known_tempo():
    # 60 BPM means 1 second = 1 beat
    notes = [NoteEvent(pitch=60, start_sec=2.0, end_sec=3.0)]
    result = seconds_to_beats(notes, bpm=60)
    assert result[0].start_beat == pytest.approx(2.0)
    assert result[0].end_beat == pytest.approx(3.0)


def test_faster_tempo_gives_more_beats():
    notes = [NoteEvent(pitch=60, start_sec=0.0, end_sec=1.0)]
    slow = seconds_to_beats(notes, bpm=60)[0].end_beat
    fast = seconds_to_beats(notes, bpm=120)[0].end_beat
    assert fast == pytest.approx(slow * 2)


def test_lead_in_shifts_start_and_end():
    notes = [NoteEvent(pitch=60, start_sec=2.4, end_sec=3.0)]
    result = seconds_to_beats(notes, bpm=100, lead_in_s=2.4)
    assert result[0].start_beat == pytest.approx(0.0)
    assert result[0].end_beat == pytest.approx(1.0)


def test_lead_in_preserves_duration():
    notes = [NoteEvent(pitch=60, start_sec=3.0, end_sec=4.2)]
    without = seconds_to_beats(notes, bpm=100)[0]
    with_lead = seconds_to_beats(notes, bpm=100, lead_in_s=2.4)[0]
    d1 = without.end_beat - without.start_beat
    d2 = with_lead.end_beat - with_lead.start_beat
    assert d1 == pytest.approx(d2)


def test_note_before_lead_in_is_dropped():
    notes = [
        NoteEvent(pitch=60, start_sec=0.5, end_sec=1.0),   # during count-in
        NoteEvent(pitch=62, start_sec=2.4, end_sec=3.0),   # first real note
    ]
    result = seconds_to_beats(notes, bpm=100, lead_in_s=2.4)
    assert len(result) == 1
    assert result[0].pitch == 62


def test_empty_list():
    assert seconds_to_beats([], bpm=100) == []


def test_order_is_preserved():
    notes = [
        NoteEvent(pitch=60, start_sec=0.0, end_sec=0.5),
        NoteEvent(pitch=62, start_sec=0.6, end_sec=1.1),
        NoteEvent(pitch=64, start_sec=1.2, end_sec=1.7),
    ]
    result = seconds_to_beats(notes, bpm=100)
    assert [n.pitch for n in result] == [60, 62, 64]