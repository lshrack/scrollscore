import music21
from mido import MidiFile
from mido.messages.messages import Message


def file_to_note_streams(filepath, info = 'pitch'):
    stream = music21.converter.parse(filepath)

    #stream = music21.midi.translate.midiFileToStream(music21.converter.parse(filepath))
    parts = stream.elements

    staffs = [part for part in parts
              if type(part) == music21.stream.PartStaff
              or type(part) == music21.stream.Part]

    note_streams = []

    for staff in staffs:
        print("staff elements", len(staff.elements))
        measures = [el for el in staff.elements if type(el) == music21.stream.Measure]
        #print("measure elements", measures[0].elements)
        note_stream = []

        for i, measure in enumerate(measures):
            #print(type(measure.elements[0]) == music21.layout.SystemLayout, i)
            for note in measure.notes:
                if type(note) == music21.note.Note:
                    if(info == 'pitch'):
                        note_stream.append(note.pitch.nameWithOctave)
                    elif(info == 'length'):
                        note_stream.append(note.quarterLength)
                else:
                    if(info == 'pitch'):
                        note_stream.append([note.pitch.nameWithOctave for note in note.notes])
                    elif(info == 'length'):
                        note_stream.append([note.quarterLength for note in note.notes])

        note_streams.append(note_stream)

    return note_streams

#pred = file_to_note_streams('intermediate_results/Happy_Birthday_To_You_Piano_1.musicxml')
#gt = file_to_note_streams('intermediate_results/Happy_Birthday_To_You_Piano_1.musicxml', 'length')

#print(gt[0][0:3])

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
    curr_notes = []
    notes = []
    note_times = []
    notes_on = 0
    started_notes = {}
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
            
            #notes_on = 0

            if msg.type == 'note_on' and msg.velocity > 0:
                started_notes[msg.note] = time_tracker

                # if(filter_range == None or
                #    msg.note >= filter_range[0] and msg.note <= filter_range[1]):
                #     curr_notes.append(msg.note)

                #     #notes.append(msg.note)
                #     #note_times.append(time_tracker)

                #     notes_on += 1

            if msg.type == 'note_off' or msg.type == 'note_on' and msg.velocity == 0:
                start = started_notes[msg.note]
                del started_notes[msg.note]
                end = time_tracker
                
                if(len(notes)>0 and start < notes[-1]['end']):
                    notes[-1]['notes'].append(msg.note)
                    notes[-1]['end'] = end
                
                else:
                    notes.append({
                        'start': start,
                        'end': end,
                        'notes': [msg.note]
                    })
                # notes_on = max(notes_on - 1, 0)
                # if notes_on == 0 and len(curr_notes) > 0:
                #     notes.append(curr_notes)
                #     curr_notes = []

                # end = time_tracker

    if include_end:
        assert end >= note_times[-1], "MIDI should have an note_off message after the last note_on message"
        return notes, note_times, end

    return [chord['notes'] for chord in notes]


notes = midi_to_graph('intermediate_results/concatenated_002_basic_pitch.mid')

print(notes[:10])
#print(notes, note_times)

mid = MidiFile('intermediate_results/concatenated_002_basic_pitch.mid')

for message in mid.tracks[1][170:200]:
    print(message)
    #if message.type != 'pitchwheel': print(message)

#print(notes[0:10])
#print(note_times[0:10])
# for i in range(10):
#     print(note_times[i+1] - note_times[i])


#pitches = file_to_note_streams('intermediate_results/concatenated_002_basic_pitch.mid',
#                                'pitch')
# #lengths = file_to_note_streams('intermediate_results/concatenated_002_basic_pitch.mid',
#                                'length')
# #print(pitches[0][:20])
#print(lengths[0][:20])


