# borrowed mainly from this StackOverflow post:
# https://stackoverflow.com/questions/69800151/convert-webm-file-to-wav-file-with-python
import subprocess

def save_as_wav(webm_path):
    """
    Save a .webm audio file as a .wav file.

    webm_path: path to .webm file

    Returns: path to .wav file
    """
    opus_path = webm_path.replace('.webm', '.opus')
    wav_path = webm_path.replace('.webm', '.wav')

    command1 = ['ffmpeg', '-i', webm_path, '-vn', '-acodec',
               'copy', opus_path]
    command2 = ['ffmpeg', '-i', webm_path, wav_path]
    subprocess.run(command1,stdout=subprocess.DEVNULL,stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    subprocess.run(command2,stdout=subprocess.DEVNULL,stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    return wav_path
