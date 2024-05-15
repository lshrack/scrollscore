from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


def audio_to_midi(audio_file, output_folder):
    """
    Run the basic-pitch model on an audio file.

    audio_file: path to WAV file (or other file format compatible with basic-pitch)
    output_folder: path to folder where outputs should be saved
    """
    output_path = output_folder + audio_file.split('/')[-1].split('.')[0] + '_basic_pitch.mid'
    predict_and_save([audio_file],
                    output_folder,
                    True, True, False, False, ICASSP_2022_MODEL_PATH)
    
    return output_path