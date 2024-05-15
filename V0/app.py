from flask import Flask, render_template_string, request, render_template
from flask_socketio import SocketIO, send
from distutils.log import debug 
from fileinput import filename
import json
import os
import time
import shutil
from process_pdf import pdf_to_mxls
import midi_vec


app = Flask(__name__)

# Render the HTML template
@app.route('/', methods = ['POST', 'GET'])
def index():
    with open('static/index.html', 'r') as file:
        template = file.read()

    if request.method == 'POST':
        files = [file for file in os.listdir('./audio_data') if file[0] != '.' and '.webm' in file]
        nums = [int(file.replace('file', '').replace('.webm', '')) for file in files]
        file_num = max(nums) + 1 if len(nums) > 0 else 1
        filepath = f'./audio_data/file{file_num}.webm'

        file = request.files['audio_data']
        file.save(filepath)

        for f in [f'audio_data/file{file_num}.wav',
                f'audio_data/file{file_num}.opus',
                f'intermediate_results/file{file_num}_basic_pitch.mid',
                f'intermediate_results/file{file_num}_basic_pitch.wav']:
            if(os.path.isfile(f)):
                os.remove(f)

        #return str(file_num * 200)
        return midi_vec.sample_to_y(filepath)
        #return webm_to_y(filepath, 11)

        #return render_template_string(template, pageNum = 1, request = "POST", yVal = 2000)

    else:
        midi_vec.set_curr_pos(0)
        return render_template_string(template, pageNum = 1, yVal = 0, pdfName = '/static/concatenated_002.pdf')

# Endpoint to trigger scrolling
@app.route('/scroll')
def scroll_to_page():
    y_val = int(request.args.get('yVal'))
    with open('static/index.html', 'r') as file:
        template = file.read()
    return render_template_string(template, section = 'holder', yVal=y_val)

@app.route('/upload')
def upload():
    with open('static/upload.html', 'r') as file:
        template = file.read()
    return render_template_string(template)

@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        filepath = f'static/user_pdfs/{f.filename}'
        if not os.path.isfile(filepath):
            f.save(filepath)   
            print("about to run PDF => MXLs")
            print(pdf_to_mxls(filepath, 'intermediate_results/'))
        midi_vec.set_curr_pos(0)

        # [306, 706, 1105, 1504]

        with open('static/index.html', 'r') as file:
            template = file.read()

        return render_template_string(template, pdfName = filepath, yVal = 0)   


def clear_directory(dir_path):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except:
            print('Failed to clear', dir_path, "- could not delete", file_path)

if __name__ == '__main__':
    if False:
        clear_directory('static/user_pdfs')
        clear_directory('intermediate_results')
        clear_directory('audio_data')
    app.run(debug=True)