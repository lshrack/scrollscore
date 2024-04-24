from midi_graph import area_between, scale_times, index_of_time, area_between_fast

def match_index(index, sheet_music_indices):
    staff_index = 0
    while(staff_index < len(sheet_music_indices)
          and sheet_music_indices[staff_index] <= index):
        staff_index += 1

    return staff_index - 1

def match(audio_graph, sheet_music_graph, sheet_music_indices):
    audio_notes, audio_times = audio_graph
    sheet_notes, sheet_times = sheet_music_graph

    audio_times = [time - audio_times[0] for time in audio_times]

    min_differences = []
    best_start, best_end = None, None
    best_factor = None
    scaling_factors = [x/20 for x in range(5, 80, 1)]
    scaled_audio_times_list = []
    for factor in scaling_factors:
        scaled_audio_times_list.append(scale_times(audio_times, factor))

    for start in range(len(sheet_notes)):
        sheet_times_shifted = [time - sheet_times[start] for time in sheet_times[start:]]

        for scaled_audio_times in scaled_audio_times_list:
            difference = area_between_fast(audio_notes, scaled_audio_times,
                                        sheet_notes[start:], sheet_times_shifted, num_steps = 1000)
            if (difference is not None and
                (min_difference is None or difference < min_difference)):
                min_difference = difference
                best_start = start
                end_time = scaled_audio_times[-1] - scaled_audio_times[0] + sheet_times[start]
                best_end = index_of_time(end_time, sheet_times)
                best_factor = factor

    
    return (match_index(best_start, sheet_music_indices),
            match_index(best_end, sheet_music_indices),
            best_factor)

    
        