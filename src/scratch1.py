from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from transcribe import transcribe

notes = transcribe("samples/melody2_mixed_rhythm_100bpm.wav")

print(len(notes))                                    # 9
print([n.pitch for n in notes])                      # [60, 62, 64, 65, 67, 65, 64, 62, 60]
print(type(notes[0].start_sec), type(notes[0].pitch))  # <class 'float'> <class 'int'>

starts = [n.start_sec for n in notes]
print(starts == sorted(starts))                      # True

