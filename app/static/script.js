var socket = io();

const test = false

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
  cur_wavesurfer.setPlaybackRate(playbackRate)
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

init()