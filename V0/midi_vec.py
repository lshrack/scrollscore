from mido import MidiFile
from mido.messages.messages import Message
import music21
from webm_to_wav import save_as_wav
from audio_to_midi import audio_to_midi
import json

output_folder = 'intermediate_results/'

def set_mxls(mxls):
    with open("intermediate_results/mxls.json", "w") as f:
        json.dump(mxls, f)

def get_mxls():
    with open("intermediate_results/mxls.json") as f:
        return json.load(f)

def set_curr_pos(curr_pos):
    with open('intermediate_results/curr_pos.txt', 'w') as f:
        f.write(str(curr_pos))

def get_curr_pos():
    with open('intermediate_results/curr_pos.txt') as f:
        return int(f.readline())
    

def mxl_to_vec(filepath):
    start_indices = [0]

    stream = music21.converter.parse(filepath)

    parts = stream.elements

    staffs = [part for part in parts
              if type(part) == music21.stream.PartStaff
              or type(part) == music21.stream.Part]

    assert len(staffs) == 2, "expected two staffs (a grand staff)!"

    treble_measures = [el for el in staffs[0].elements if type(el) == music21.stream.Measure]
    bass_measures = [el for el in staffs[1].elements if type(el) == music21.stream.Measure]

    note_stream = []
    for treble, bass in zip(treble_measures, bass_measures):
        voices = [el for el in treble.elements if type(el) == music21.stream.Voice]
        voices += [el for el in bass.elements if type(el) == music21.stream.Voice]

        if type(treble.elements[0]) == music21.layout.SystemLayout:
            start_indices.append(len(note_stream))

        measure_notes = []
        curr_time = 0
        
        for note in treble.notes:
            if type(note) == music21.note.Note:
                measure_notes.append({"notes": [note.pitch.midi],
                                    "start": curr_time,
                                    "end": curr_time + note.duration.quarterLength
                                    })

            elif type(note) == music21.chord.Chord:
                measure_notes.append({"notes": [note.pitch.midi
                                              for note in note.notes],
                                    "start": curr_time,
                                    "end": curr_time + note.duration.quarterLength
                                    })

            curr_time += note.duration.quarterLength

        curr_time = 0

        # remaining_notes = list(bass.notes)
        # for voice in voices:
        #     remaining_notes += list(voice.notes)

        for voice in [bass] + voices:
            curr_time = 0
            for note in voice.notes:
                if type(note) == music21.note.Note or type(note) == music21.chord.Chord:
                    correct_chord = None
                    for notes in measure_notes:
                        if notes['start'] <= curr_time and notes['end'] > curr_time:
                            correct_chord = notes

                    if correct_chord == None :
                        correct_chord = {"notes": [],
                                        "start": curr_time,
                                        "end": curr_time + note.duration.quarterLength
                                        }
                        measure_notes.append(correct_chord)

                    if type(note) == music21.note.Note:
                        correct_chord["notes"].append(note.pitch.midi)
                    else:
                        correct_chord["notes"] += ([note.pitch.midi for note in note.notes])

                curr_time += note.duration.quarterLength


        measure_notes = sorted(measure_notes, key=lambda x: x['start'])
        measure_notes = [notes["notes"] for notes in measure_notes]

        note_stream += measure_notes

    return note_stream, start_indices

def midi_to_vec(filepath, filter_range = None):

    def in_filter_range(note):
        return (filter_range == None
                or msg.note >= filter_range[0]
                and msg.note <= filter_range[1])
    
    mid = MidiFile(filepath)

    time_tracker = 0
    end = 0
    notes = []
    started_notes = {}

    max_len = len(mid.tracks[0])
    chosen_track = mid.tracks[0]

    for track in mid.tracks:
        if len(track) > max_len:
            max_len = len(track)
            chosen_track = track

    for msg in chosen_track:
        if type(msg) == Message:
            time_tracker += msg.time
            if msg.type == 'note_on' and msg.velocity > 0 and in_filter_range(msg.note):
                started_notes[msg.note] = time_tracker

            if msg.type == 'note_off' or msg.type == 'note_on' and msg.velocity == 0 \
                and in_filter_range(msg.note):
                start = started_notes[msg.note]
                del started_notes[msg.note]
                end = time_tracker

                if(len(notes)>0 and start < notes[-1]['end'] - 40):
                    notes[-1]['notes'].append(msg.note)
                    notes[-1]['end'] = end
                
                else:
                    notes.append({
                        'start': start,
                        'end': end,
                        'notes': [msg.note]
                    })

    return [chord['notes'] for chord in notes]

def mxls_to_vec(filepaths):
    starts = []
    vec = []
    for i, filepath in enumerate(filepaths):
        mxl_vec, start_indices = mxl_to_vec(filepath)
        prev_len = len(vec)
        vec += mxl_vec
        for j, start in enumerate(start_indices):
            starts.append({
                "start":start + prev_len,
                "page_num": i,
                "staff_box": j
            })
    
    return vec, starts

def acc_rec(sample, sm, sample_i, sm_i, cache):
    def compute_score(sample_val, sm_val):
        return len(set(sample_val).intersection(set(sm_val)))
                
    if((sample_i, sm_i) in cache):
        return cache[(sample_i, sm_i)]

    if(sample_i == len(sample) or sm_i == len(sm)):
        cache[(sample_i, sm_i)] = (0, sm_i)

    else:
        score = compute_score(sample[sample_i], sm[sm_i])

        if(sample_i == len(sample) - 1 and sm_i == len(sm) - 1):
            cache[(sample_i, sm_i)] = (score, sm_i)
            
        else:
            match_here_score, match_here_end = acc_rec(sample, sm, sample_i + 1, sm_i + 1, cache)
            match_here_score += score

            skip_sample_score, skip_sample_end = acc_rec(sample, sm, sample_i + 1, sm_i, cache)
            skip_sample_score*=.98

            skip_sm_score, skip_sm_end = acc_rec(sample, sm, sample_i, sm_i + 1, cache)
            skip_sm_score*=.95

            if match_here_score >= skip_sample_score and match_here_score >= skip_sm_score:
                cache[(sample_i, sm_i)] = match_here_score, match_here_end
            elif skip_sample_score >= skip_sm_score:
                cache[(sample_i, sm_i)] = skip_sample_score, skip_sample_end
            else:
                cache[(sample_i, sm_i)] = skip_sm_score, skip_sm_end

    return cache[(sample_i, sm_i)]

def match(sample_midi, sm_mxls, start_index = 0):
    sm_vec, start_indices = mxls_to_vec(sm_mxls)
    filter_range = [min(min(x) for x in sm_vec), max(max(x) for x in sm_vec)]

    sample_vec = midi_to_vec(sample_midi, filter_range)

    acc, index = acc_rec(sample_vec, sm_vec, 0, start_index, {})
    set_curr_pos(index)
    print(acc, index)

    for i in range(len(start_indices)-1):
        start = start_indices[i]
        next_start = start_indices[i+1]
        if next_start['start'] > index:
            return start["page_num"], start["staff_box"]
        
    return start_indices[-1]["page_num"], start_indices[-1]["staff_box"]

def sample_to_y(sample_webm):
    mxls = get_mxls()
    curr_pos = get_curr_pos()
    assert len(mxls) > 0, "PDF wasn't loaded properly"

    wav_path = save_as_wav(sample_webm)
    sample_midi = audio_to_midi(wav_path, output_folder)

    page_num, staff_box = match(sample_midi,
                                [mxl["filepath"] for mxl in mxls],
                                curr_pos)
    
    y_pos = (mxls[page_num]['y_pos'][staff_box] + page_num) / len(mxls)
    print(y_pos)

    return str(y_pos)

# _mxls = [{"filepath": "intermediate_results/Happy_Birthday_To_You_Piano_1.musicxml",
#          "y_pos": [306, 706, 1105, 1504]}]

# print(sample_to_y("intermediate_results/Happy_Birthday_To_You_Piano_basic_pitch.mid"))
  
# print(match("intermediate_results/Happy_Birthday_To_You_Piano_basic_pitch.mid",
#             ["intermediate_results/Happy_Birthday_To_You_Piano_1.musicxml"],
#             start_index = 0))


    