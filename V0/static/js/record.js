// This code is largely sourced from this Stack Overflow post:
// https://stackoverflow.com/questions/60032983/record-voice-with-recorder-js-and-upload-it-to-python-flask-server-but-wav-file


URL = window.URL;

var gumStream;
var rec;
var input;
var interval;

var AudioContext = window.AudioContext;
var audioContext;

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording(){
    console.log("Record button clicked");
    var constraints = { audio: true, video:false };

    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false;

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"
        gumStream = stream;
        //input = audioContext.createMediaStreamSource(stream);
        //rec = new MediaRecorder(input,{numChannels:1});
        rec = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
        rec.start();
        console.log("Recording started");

        interval = window.setInterval(saveFile, 10000);

        var chunks = [];
        rec.onstop = (e) => {
            console.log("data available after MediaRecorder.stop() called.");
            const blob = new Blob(chunks, { type: rec.mimeType });
            createDownloadLink(blob);
          };
          
          rec.ondataavailable = (e) => {
            console.log("got data available");
            //chunks.push(e.data);
            chunks = [e.data];
            //console.log(chunks.length)
          };

    }).catch(function(err) {
        console.log(err);
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function saveFile(){
    console.log("saving off a file");
    rec.stop();
    rec.start();
}

function pauseRecording(){
    console.log("pause button clicked, state = ", rec.state);

    if(rec.state == "recording"){
        rec.stop();
        pauseButton.innerHTML="Resume";
    }
    else{
        rec.start();
        pauseButton.innerHTML="Pause";
    };
}

function stopRecording(){
    window.clearInterval(interval);
    console.log("stopButton clicked");

    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    pauseButton.innerHTML="Pause";
    rec.stop();

    gumStream.getAudioTracks()[0].stop();
}

function createDownloadLink(blob){    
    var filename = new Date().toISOString();

    var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
        if(this.readyState === 4) {
            console.log("Server returned: ",e.target.responseText);
            $(document).ready(function() {
                $("html, body").animate({ scrollTop: e.target.responseText * document.body.scrollHeight }, 100);
            })
        }
    };

    var fd=new FormData();
    fd.append("audio_data",blob, filename);
    xhr.open("POST","/",true);
    xhr.send(fd);
}

