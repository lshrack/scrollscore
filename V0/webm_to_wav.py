# borrowed mainly from this StackOverflow post:
# https://stackoverflow.com/questions/69800151/convert-webm-file-to-wav-file-with-python
import moviepy.editor as moviepy
import subprocess

def save_as_wav(webm_path):
    #clip = moviepy.AudioFileClip(webm_path)
    #clip.audio.write_audiofile(webm_path.replace('.webm', '.wav'))
    opus_path = webm_path.replace('.webm', '.opus')
    wav_path = webm_path.replace('.webm', '.wav')

    command1 = ['ffmpeg', '-i', webm_path, '-vn', '-acodec',
               'copy', opus_path]
    command2 = ['ffmpeg', '-i', webm_path, wav_path]
    subprocess.run(command1,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    subprocess.run(command2,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
