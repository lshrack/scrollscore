from flask import Flask, render_template_string, request, render_template
from flask_socketio import SocketIO, send
import json

app = Flask(__name__)

# Render the HTML template
@app.route('/', methods = ['POST', 'GET'])
def index():
    with open('static/index.html', 'r') as file:
        template = file.read()

    if request.method == 'POST':
        file = request.files['audio_data']
        file.save('./audio_data/file.webm')
        return "1000"

        #return render_template_string(template, pageNum = 1, request = "POST", yVal = 2000)

    else:
        return render_template_string(template, pageNum = 1, yVal = 1000)

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