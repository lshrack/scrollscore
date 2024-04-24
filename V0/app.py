from flask import Flask, render_template_string, request, render_template
from flask_socketio import SocketIO, send
import json
import os
import time
from main import webm_to_y

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

        #return str(file_num * 200)
        return webm_to_y(filepath, 11)

        #return render_template_string(template, pageNum = 1, request = "POST", yVal = 2000)

    else:
        return render_template_string(template, pageNum = 1, yVal = 0)

# Endpoint to trigger scrolling
@app.route('/scroll')
def scroll_to_page():
    y_val = int(request.args.get('yVal'))
    # Send a message to the client to scroll to the specified page
    #message = {'action': 'scrollToPage', 'pageNum': page_num}
    #return json.dumps(message)
    with open('static/index.html', 'r') as file:
        template = file.read()
    return render_template_string(template, section = 'holder', yVal=y_val)

if __name__ == '__main__':
    app.run(debug=True)