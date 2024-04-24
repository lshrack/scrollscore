from mido import MidiFile
from mido.messages.messages import Message

def midi_to_graph(mid_path, include_end = False, filter_range = None):
    """
    Converts a MIDI file into a graph representation.

    Args:
        mid_path: path to MIDI file
    
    Returns:
        notes: list of pitches in the given MIDI file (length N)
        note_times: list of times of notes in the given MIDI file (length N)
    """
    mid = MidiFile(mid_path)

    #assert len(mid.tracks) == 2, "expected 2 tracks (one metadata, one musical information)"

    time_tracker = 0
    end = 0
    notes = []
    note_times = []
    #print(mid.tracks[-1])
    #print(len(mid.tracks[-1]))
    #print(mid_path, [(track[0], track[-1], len(track)) for track in mid.tracks])
    max_len = len(mid.tracks[0])
    chosen_track = mid.tracks[0]

    for track in mid.tracks:
        if len(track) > max_len:
            max_len = len(track)
            chosen_track = track


    for msg in chosen_track:
        if type(msg) == Message:
            #print(msg)
            time_tracker += msg.time

            if msg.type == 'note_on':
                if(filter_range == None or
                   msg.note >= filter_range[0] and msg.note <= filter_range[1]):
                    notes.append(msg.note)
                    note_times.append(time_tracker)

            if msg.type == 'note_off' or msg.type == 'note_on' and msg.velocity == 0:
                end = time_tracker

    if include_end:
        assert end >= note_times[-1], "MIDI should have an note_off message after the last note_on message"
        return notes, note_times, end

    return notes, note_times

def midi_list_to_graph(mid_paths):
    """
    Converts a list of MIDI files into a graph representation.

    Args:
        mid_paths: list of paths to MIDI files (length M)
    
    Returns:
        notes: concatenated list of pitches in the given MIDI files (length N)
        note_times: concatenated list of times of notes in the given MIDI files (length N)
        start_indices: list of indices into the notes/note_times arrays for the start point
            of each MIDI file (length M)
    """
    start_indices = []
    notes_all = []
    note_times_all = []
    prev_end = 0
    for mid_path in mid_paths:
        start_indices.append(len(notes_all))
        notes, note_times, end = midi_to_graph(mid_path, True)
        notes_all += notes
        note_times_all += [time + prev_end for time in note_times]
        prev_end += end

    return notes_all, note_times_all, start_indices

def scale_times(times, factor):
    return [time * factor for time in times]

def get_function(notes, times):
    assert times == sorted(times), "should be in chronological order"

    def f(t):
        assert t >= times[0] and t <= times[-1], "time not in domain"

        if t in times:
            return notes[times.index(t)]
        
        for i, t_i in enumerate(times):
            if t_i > t:
                return notes[i-1]
            
    return f


def area_between(audio_notes, audio_times, sheet_notes, sheet_times, num_steps = 1000):
    #audio_times = [time - audio_times[0] for time in audio_times]
    #sheet_times = [time - sheet_times[0] for time in sheet_times]
    start_time = max(audio_times[0], sheet_times[0])
    end_time = min(audio_times[-1], sheet_times[-1])

    if end_time - start_time < 0.75 * (audio_times[-1] - audio_times[0]):
        return None
    
    f1 = get_function(audio_notes, audio_times)
    f2 = get_function(sheet_notes, sheet_times)

    step_size = (end_time - start_time) / num_steps
    sum_diffs = 0

    times = [start_time + i * step_size for i in range(num_steps)]

    for t in times:
        sum_diffs += abs(f1(t) - f2(t))


    return sum_diffs / num_steps

def area_between_fast(audio_notes, audio_times, sheet_notes, sheet_times, num_steps = 1000):
    assert (audio_times == sorted(audio_times) and
            sheet_times == sorted(sheet_times)), "times arrays should be in sorted order"
    
    start_time = max(audio_times[0], sheet_times[0])
    end_time = min(audio_times[-1], sheet_times[-1])

    if end_time - start_time < 0.75 * (audio_times[-1] - audio_times[0]):
        return None
    
    step_size = (end_time - start_time) / num_steps
    sum_diffs = 0
    a_i = 0
    s_i = 0

    times = [start_time + i * step_size for i in range(num_steps)]

    for time in times:
        while audio_times[a_i] <= time:
            a_i += 1
        while sheet_times[s_i] <= time:
            s_i += 1
        
        sum_diffs += abs(audio_notes[a_i-1] - sheet_notes[s_i-1])
    
    return sum_diffs / num_steps

def index_of_time(time, note_times):
    i = 0
    while(i < len(note_times) and note_times[i] < time):
        i += 1

    return min(i, len(note_times))
