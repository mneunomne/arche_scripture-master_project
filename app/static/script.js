var socket = io();

const params = new URLSearchParams(window.location.search)

const test = params.has('test') || false
const fake_audio = params.has('fake_audio') || false
const random_speed = params.has('random_speed') || false

var wavesurfer0 = WaveSurfer.create({
  container: '#waveform0',
  waveColor: 'white',
  progressColor: 'white',
  cursorWidth: 2,
  cursorColor: 'blue',
  height: 200,
  fillParent: true
});

var wavesurfer1 = WaveSurfer.create({
  container: '#waveform1',
  waveColor: 'white',
  progressColor: 'white',
  cursorWidth: 2,
  cursorColor: 'blue',
  height: 200,
  fillParent: true
});

var last_wavesurfer_index = null
var cur_wavesurfer = null 

const volume = 0.1 
const loop = true
const playbackRate = 0.1

const textEl = document.getElementById('text')

const el_waveform0 = document.getElementById("waveform0")
const el_waveform1 = document.getElementById("waveform1")

const init = function () {
  addEvents()
  if (fake_audio) load_json()
  if (test) run_test()
}

const addEvents = function () {
  socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log("socketio connected!")
  });

  socket.on('detection_data', onDetectionData)

  wavesurfer0.on('ready', onAudioReady);
  wavesurfer1.on('ready', onAudioReady);

  /*
  on any interaction
  document.body.addEventListener('mousemove', handleInteraction);
  document.body.addEventListener('scroll', handleInteraction);
  document.body.addEventListener('keydown', handleInteraction);
  document.body.addEventListener('click', handleInteraction);
  document.body.addEventListener('touchstart', handleInteraction);
  */
}

const onDetectionData = function (data) {
  console.log("detection_data!", data)

  // if its still playing, ignore...
  if (wavesurfer0.isPlaying() || wavesurfer1.isPlaying()) {
    console.log("already playing!")
    return
  }

  if (last_wavesurfer_index == null || last_wavesurfer_index == 1) {
    // 0 will be current player
    last_wavesurfer_index=0
    el_waveform1.className = 'box hidden'
    el_waveform0.className = 'box'
    cur_wavesurfer = wavesurfer0
  } else {
    // 1
    last_wavesurfer_index=1
    el_waveform0.className = 'box hidden'
    el_waveform1.className = 'box'
    cur_wavesurfer = wavesurfer1
  }

  let {text} = data
  let wavDataURI = text2Audio(text, false, 0.1)
  cur_wavesurfer.load(wavDataURI)
  textEl.innerText=text
}

const onAudioReady = function () {
  console.log("onAudioReady!", cur_wavesurfer)
  if (random_speed) {
    cur_wavesurfer.setPlaybackRate(Math.random())
  } else {
    cur_wavesurfer.setPlaybackRate(playbackRate)
  }
  cur_wavesurfer.volume = volume
  cur_wavesurfer.loop = loop
  cur_wavesurfer.play();
}

const run_test = () => {
  onDetectionData({"text": test_text})
  setInterval(() => {
    onDetectionData({"text": test_text})
  }, 5000)
}

const load_json = function () {
  function fetchJSONFile(path, callback) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                var data = JSON.parse(httpRequest.responseText);
                if (callback) callback(data);
            }
        }
    };
    httpRequest.open('GET', path);
    httpRequest.send(); 
}

// this requests the file and executes a callback with the parsed result once
//   it is available
fetchJSONFile('745.json', function(data){
    let textData = data.positions.map(p => p.char).join('');
    onDetectionData({"text": textData})
    setInterval(() => {
      onDetectionData({"text": textData})
      wavesurfer0.setCursorColor('transparent')
      wavesurfer1.setCursorColor('transparent')
    }, 10000)
  });
}

init()