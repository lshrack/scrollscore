from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


def audio_to_midi(audio_file, output_folder):
    output_path = output_folder + audio_file.split('/')[-1].split('.')[0] + '_basic_pitch.mid'
    predict_and_save([audio_file],
                    output_folder,
                    True, True, False, False, ICASSP_2022_MODEL_PATH)
    
    return output_path