'use strict';

/* globals MediaRecorder */

let mediaRecorder;
let recordedBlobs;
let uName =
    document.getElementById("username").innerText

let ass = document.getElementById("assname").innerHTML



const errorMsgElement = document.querySelector('span#errorMsg');
// const recordedVideo = document.querySelector('video#recorded');
const recordedVideo = document.querySelector('video#gum');
const recordButton = document.querySelector('button#record');
const playButton = document.querySelector('button#play');
const uploadButton = document.querySelector('button#upload');
const startButton = document.querySelector('button#start');
const nextButton = document.querySelector('button#next');

//csrf
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//upload func
uploadButton.addEventListener('click', () => {
    document.getElementById("exit").style.visibility = "visible";
    playButton.disabled = true
    uploadButton.disabled = true    
    startButton.disabled = true   
    recordButton.disabled = true   





    const blob = new Blob(recordedBlobs, { type: 'video/mp4' });
    const videoUrl = window.URL.createObjectURL(blob);

    var fd = new FormData();
    fd.append('fileName', uName);
    //fd.append('fileName', 'test.mp4');
    fd.append('data', blob);
    fd.append('assessmentName', ass)
    fd.append('videoUrl',videoUrl)

    $.ajax({
        type: 'POST',
        url: 'fileUpload/',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        mode: "same-origin",
        data: fd,
        processData: false,
        contentType: false
    }).done(function (data) {
        alert(uName + " --> Your assessment is submited successfully! Exit The Assessment.")
        console.log(data);
    });
});

// next button

var visibleDiv = 0;
function showDiv()
{
  $(".grid").hide();
  $(".grid:eq("+ visibleDiv +")").show();
}
showDiv()

function showNext()
{
if(visibleDiv== $(".grid").length-1)
{
  visibleDiv = 0;
}
else {
  visibleDiv ++;
}
showDiv();
}


function showPrev()
{
if (visibleDiv == 0)
{
  visibleDiv= $(".grid").length-1
}
else {
  visibleDiv --;
}
showDiv();
}

//record button
recordButton.addEventListener('click', () => {
    
    if (recordButton.textContent === 'Record') {
        alert("Recording is started")
        startRecording();
    } else {
        alert("Your answer is recorded review your answer and then submit it!")
        stopRecording()
        recordButton.textContent = 'Record'
        playButton.disabled = false
        uploadButton.disabled = false
    }
});

//play button
playButton.addEventListener('click', () => {
    const superBuffer = new Blob(recordedBlobs, { type: 'video/webm' });
    recordedVideo.src = null;
    recordedVideo.srcObject = null;
    recordedVideo.src = window.URL.createObjectURL(superBuffer);
    recordedVideo.controls = true;
    recordedVideo.play();
    startButton.disabled = true   
    recordButton.disabled = true 
    gum.disabled = true
});


//handleDataAvailable
function handleDataAvailable(event) {
    console.log('handleDataAvailable', event);
    if (event.data && event.data.size > 0) {
        recordedBlobs.push(event.data);
    }
}

//startRecording
function startRecording() {
    recordedBlobs = []
    let options = {
        MimeType: 'video/webm;codecs=vp9,opus'
    }
    try {
        mediaRecorder = new MediaRecorder(window.stream, options)



    } catch (e) {
        console.error('Exception while creating MediaRecorder:', e);
        errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`
        return;
    }

    console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
    recordButton.textContent = 'Stop';
    playButton.disabled = true;
    uploadButton.disabled = true;
    mediaRecorder.onstop = (event) => {
        console.log('Recorder stopped: ', event);
        console.log('Recorded Blobs: ', recordedBlobs);
    };
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();
    console.log('MediaRecorder started', mediaRecorder);
}

//stopRecording
function stopRecording() {
    mediaRecorder.stop();
}


function handleSuccess(stream) {
    recordButton.disabled = false;
    console.log('getUserMedia() got stream:', stream);
    window.stream = stream;
  
    const gumVideo = document.querySelector('video#gum');
    gumVideo.srcObject = stream;
  }
  
  async function init(constraints) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      handleSuccess(stream);
    } catch (e) {
      console.error('navigator.getUserMedia error:', e);
      errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
  }
  
  document.querySelector('button#start').addEventListener('click', async () => {
    const hasEchoCancellation = document.querySelector('#echoCancellation').checked;
    const constraints = {
      audio: {
        echoCancellation: {exact: hasEchoCancellation}
      },
      video: {
        width: 2040, height: 1080
      }
    };
    console.log('Using media constraints:', constraints);
    await init(constraints);
  });