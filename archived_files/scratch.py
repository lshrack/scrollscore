#from png_to_midis import generate_midis
import cv2
import matplotlib.pyplot as plt
from process_pdf import pdf_to_pngs
from midi_graph import midi_list_to_graph, midi_to_graph, scale_times
from audio_to_midi import audio_to_midi
from comparator import match


filepath1 = 'scratch/original_tt.png'
filepath2 = 'scratch/pdf_screenshot_cropped_tt.png'
output_folder_midis = 'scratch/outputs/'

midi_filepaths = []
for page, staff_box in (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,1), (2,2), (2,3), (2,4):
    midi_filepaths.append(f'intermediate_results/manual/concat_002_{page}_{staff_box}.mid')

notes, note_times, start_indices = midi_list_to_graph(midi_filepaths)

#audio_midi = audio_to_midi('data/concatenated_002.wav', 'intermediate_results/')
audio_midi = 'intermediate_results/concatenated_002_basic_pitch.mid'

filter_range = (min(notes), max(notes))

audio_notes, audio_note_times = midi_to_graph(audio_midi, filter_range=filter_range)
audio_note_times = scale_times(audio_note_times, note_times[-1]/audio_note_times[-1])
print(len(audio_notes))

for start, end in (0, 50), (50, 100), (100, 150), (150,200), (250,300), (300, len(audio_notes)):
    filtered_audio_notes = audio_notes[start:end]
    filtered_audio_note_times = audio_note_times[start:end]
    
    #plt.plot(filtered_audio_note_times, filtered_audio_notes)
    #plt.show()

    print(match((filtered_audio_notes, filtered_audio_note_times),
                (notes, note_times),
                start_indices))

