var socket = io();

var wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: 'violet',
  progressColor: 'purple'
});

const volume = 0.1 
const loop = false
const playbackRate = 0.1 

const init = function () {
  addEvents()
}

const addEvents = function () {
  socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
  });

  socket.on('detection_data', onDetectionData)

  wavesurfer.on('ready', onAudioReady);
}

const onDetectionData = function (data) {
  let {text} = data
  let wavDataURI = text2Audio(text, false, 0.1)
  wavesurfer.load(wavDataURI)
}

const onAudioReady = function () {
  wavesurfer.playbackRate = playbackRate
  wavesurfer.volume = volume
  wavesurfer.loop = loop
  wavesurfer.play();
}











