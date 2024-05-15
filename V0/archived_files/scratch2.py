from mido import MidiFile

mid_path = 'intermediate_results/concatenated_002_basic_pitch.mid'

mid = MidiFile(mid_path)

for note in mid.tracks[1]:
    if note.type == 'note_on': print(note)