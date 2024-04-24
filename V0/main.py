from midi_graph import midi_list_to_graph, midi_to_graph, scale_times
from webm_to_wav import save_as_wav
from audio_to_midi import audio_to_midi
import pickle
from comparator import match
import sys
import os
import time

output_folder = 'intermediate_results/'
temp_midis = []
for page, staff_box in (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,1), (2,2), (2,3), (2,4):
        temp_midis.append({'filename': f'intermediate_results/manual/concat_002_{page}_{staff_box}.mid',
                            'yPos': staff_box,
                            'pageNum': page})

def get_sheet_music_graph(pdf_path):
    # implement later, once we get CNN working
    pass

def get_sheet_music_graph_temporary():
    midi_filepaths = [midi['filename'] for midi in temp_midis]
    return midi_list_to_graph(midi_filepaths)

def get_audio_graph(webm_path):
    wav_path = save_as_wav(webm_path)
    audio_midi = audio_to_midi(wav_path, output_folder)
    return midi_to_graph(audio_midi)

def match_audio_to_music(webm_path, ):
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    start_time = time.time()

    notes, note_times, start_indices = get_sheet_music_graph_temporary()
    audio_notes, audio_note_times = get_audio_graph(webm_path)

    sys.stdout = old_stdout
    

    match_start, match_end, match_factor = match((audio_notes, audio_note_times),
            (notes, note_times),
            start_indices)
    print(match_start, match_end, match_factor)
    print("Time Taken:", time.time() - start_time)

    return match_end

def staff_index_to_y(staff_index, num_staff_bars):
     return str(max((staff_index - 1) / num_staff_bars, 0))

def webm_to_y(webm_path, num_staff_bars):
     end_staff_index = match_audio_to_music(webm_path)
     return staff_index_to_y(end_staff_index, num_staff_bars)
     
for i in range(2,11):
    for f in [f'audio_data/file{i}.wav',
              f'audio_data/file{i}.opus',
              f'intermediate_results/file{i}_basic_pitch.mid',
              f'intermediate_results/file{i}_basic_pitch.wav']:
         if(os.path.isfile(f)):
            os.remove(f)

    print(i)
    match_audio_to_music(f'audio_data/file{i}.webm')








