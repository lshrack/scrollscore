from flask import Flask, render_template_string, request, render_template
from flask_socketio import SocketIO, send
import json

app = Flask(__name__)

# Render the HTML template
@app.route('/')
def index():
    with open('static/index.html', 'r') as file:
        template = file.read()
    return render_template_string(template, pageNum = 1)

@app.route('/test')
def test():
    with open('static/test.html', 'r') as file:
        template = file.read()
    res = render_template_string(template, myVar = 100)
    return res

# Endpoint to trigger scrolling
@app.route('/scroll')
def scroll_to_page():
    page_num = int(request.args.get('page'))
    # Send a message to the client to scroll to the specified page
    #message = {'action': 'scrollToPage', 'pageNum': page_num}
    #return json.dumps(message)
    with open('static/index.html', 'r') as file:
        template = file.read()
    return render_template_string(template, pageNum = page_num)

if __name__ == '__main__':
    app.run(debug=True)