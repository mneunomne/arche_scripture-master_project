var socket = io();

var wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: 'white',
});

const volume = 0.1 
const loop = false
const playbackRate = 0.1

const textEl = document.getElementById('text')

const init = function () {
  addEvents()
}

const addEvents = function () {
  socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log("socketio connected!")
  });

  socket.on('detection_data', onDetectionData)

  wavesurfer.on('ready', onAudioReady);
}

const onDetectionData = function (data) {
  console.log("detection_data!", data)
  let {text} = data
  let wavDataURI = text2Audio(text, false, 0.1)
  wavesurfer.load(wavDataURI)
  textEl.innerText=text
}

const onAudioReady = function () {
  wavesurfer.playbackRate = playbackRate
  wavesurfer.volume = volume
  wavesurfer.loop = loop
  wavesurfer.play();
}

init()


