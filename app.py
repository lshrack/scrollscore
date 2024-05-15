from flask import Flask, render_template_string, request, render_template
from flask_socketio import SocketIO, send
from distutils.log import debug 
from fileinput import filename
import os
import shutil
from process_pdf import pdf_to_mxls
import comparator


app = Flask(__name__)

# Render the HTML template
@app.route('/', methods = ['POST', 'GET'])
def index():
    with open('static/index.html', 'r') as file:
        template = file.read()

    # handle upload of audio data
    if request.method == 'POST':
        # find the next file number and save the new data there
        files = [file for file in os.listdir('./audio_data') if file[0] != '.' and '.webm' in file]
        nums = [int(file.replace('file', '').replace('.webm', '')) for file in files]
        file_num = max(nums) + 1 if len(nums) > 0 else 1
        filepath = f'./audio_data/file{file_num}.webm'

        file = request.files['audio_data']
        file.save(filepath)

        # remove old files
        for f in [f'audio_data/file{file_num}.wav',
                f'audio_data/file{file_num}.opus',
                f'intermediate_results/file{file_num}_basic_pitch.mid',
                f'intermediate_results/file{file_num}_basic_pitch.wav']:
            if(os.path.isfile(f)):
                os.remove(f)

        # convert the webm file to a scroll position
        return midi_vec.sample_to_y(filepath)

    else:
        midi_vec.set_curr_pos(0)
        return render_template_string(template, pageNum = 1, yVal = 0, pdfName = '/static/concatenated_002.pdf')

# renders page for user to upload PDF
@app.route('/upload')
def upload():
    with open('static/upload.html', 'r') as file:
        template = file.read()
    return render_template_string(template)

# handles upload of PDF
@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        filepath = f'static/user_pdfs/{f.filename}'
        if not os.path.isfile(filepath):
            f.save(filepath)
            print("Converting user PDF to MusicXML files...")
            pdf_to_mxls(filepath, 'intermediate_results/')
            
        midi_vec.set_curr_pos(0)

        with open('static/index.html', 'r') as file:
            template = file.read()

        return render_template_string(template, pdfName = filepath, yVal = 0)   


def clear_directory(dir_path):
    """
    Delete all files from directory.

    dir_path: path to directory
    """
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except:
            print('Failed to clear', dir_path, "- could not delete", file_path)

def create_directory(dir_path):
    """
    Create directory if it doesn't already exist.

    dir_path: path to directory
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

if __name__ == '__main__':
    # create directories if needed
    create_directory('intermediate_results')
    create_directory('static/user_pdfs')
    create_directory('audio_data')

    # this is useful if you don't want to accumulate files, but keeping them prevents having to
    # rerun the OMR model over and over and allows you to look at intermediate outputs for debugging
    clear_directories = False
    if clear_directories:
        clear_directory('static/user_pdfs')
        clear_directory('intermediate_results')
        clear_directory('audio_data')

    app.run(debug=True)