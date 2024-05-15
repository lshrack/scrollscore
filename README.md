# ScrollScore
ScrollScore is a proof-of-concept implementation of a tool that automatically scrolls PDF sheet music based on microphone input.

## How to run ScrollScore:
1. Clone the repository to your local machine.
2. Create and activate a Python virtual environment - I used Python 3.10.7. Install requirements using pip install -r requirements.txt.
3. Install a working version of FFmpeg for your system, if you don't already have one: https://ffmpeg.org/
4. Run python app.py to launch the tool. Wait for the message that it's running. You can safely ignore warnings about TFLite and TensorFlow not being installed.
5. The tool should now be running at http://127.0.0.1:5000/upload, where you can upload a PDF for conversion. Wait for it to convert and load the PDF viewer (this will take several minutes), and then you can use the scrolling functionality.

## Table of Contents:
- archived_files: lots of old Python code - you can safely ignore this.
- oemer: Slightly modified clone of the oemer OMR model. Outside code relies on oemer/oemer/ete.py.
- static: Front end HTML, CSS, and JavaScript.
    - index.html: main HTML page with PDF viewer
    - upload.html: HTML page where PDFs can be uploaded
    - styles.css: CSS styling
    - js: folder of JavaScript files
        - pdf.js: Renders PDFs
        - record.js: Handles the front-end side of collecting and processing audio data.
- app.py: Python for main Flask application
- audio_to_midi.py: Converts an audio file to MIDI using basic-pitch.
- comparator.py: Contains all of the code used to convert MIDIs and MusicXML files into vector representations and match samples into sheet music. The highest level function takes a webm file
and returns a y position for the appropriate staff bar. All functions have docstrings.
- process_pdf.py: Converts a PDF to a list of MusicXMLs (one for each page of the PDF), and saves staffline positions.
- webm_to_wav.py: Uses FFmpeg to convert .webm audio files into .wav audio files.
