from pdf_to_pngs import pdf_to_pngs
from png_to_midis import generate_midis
from audio_to_midi import audio_to_midi
from midi_graph import midi_to_graph, midi_list_to_graph
from comparator import match


pdf_path = 'data/concatenated_002.pdf'
output_folder = 'intermediate_results/'
audio_path = 'data/scale_twinkle_twinkle.wav'

# Convert PDF to PNGS of each page
png_filepaths = pdf_to_pngs(pdf_path, output_folder)

# Get a list of dictionaries with MIDI filepaths, page numbers, and staff box numbers
midis = []
for i, filepath in enumerate(png_filepaths):
    output_folder_midis = f'{output_folder}midi_page_{i+1}_'

    midis = midis + generate_midis(filepath, output_folder_midis, i+1)

# Convert audio to MIDI using basic-pitch
audio_midi = audio_to_midi(audio_path, output_folder)

print(midis, audio_midi)

# Get piecewise graph representations of audio + sheet music, plus indices into sheet music graph
midi_filepaths = [midi['filename'] for midi in midis]

audio_notes, audio_note_times = midi_to_graph(audio_midi)
sheet_music_notes, sheet_music_note_times, midi_indices = midi_list_to_graph(midi_filepaths)


# Iterate over tempos and start positions to match audio sample into sheet music


# Return page number and position of closest match

