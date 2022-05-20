var socket = io();

const params = new URLSearchParams(window.location.search)

const reloaded = params.has('reloaded') || false

if (!reloaded) {
  setTimeout(() => {
    window.location.href = window.location.href + "&reloaded=true"
  }, 500)
}

const test = params.has('test') || false
const fake_audio = params.has('fake_audio') || false
const random_speed = params.has('random_speed') || false

const sample_rate = 8000

const d = new Date();

var lastTimePlayed = 0

var barEl = document.querySelector(".bar")

var fakeAudioData = null 

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

wavesurfer0.setCursorColor('transparent')
wavesurfer1.setCursorColor('transparent')

var last_wavesurfer_index = null
var cur_wavesurfer = null 

var noiseScale = null

const volume = 0.1 
const loop = true
const playbackRate = 0.1
var curPlaybackRate = playbackRate

const textEl = document.getElementById('text')

var $sample_rate = document.querySelector('#sample_rate span')
var $lastTimePlayed = document.querySelector('#lastTimePlayed span')
var $curPlaybackRate = document.querySelector('#curPlaybackRate span')
var $cur_length = document.querySelector('#cur_length span')
var $noiseScale = document.querySelector('#noiseScale span')

const el_waveform0 = document.getElementById("waveform0")
const el_waveform1 = document.getElementById("waveform1")

var cur_length = 0

const init = function () {
  addEvents()
  fetchJSONFile('745.json', function(data){
    let textData = data.positions.map(p => p.char).join('');
    fakeAudioData = text2numbers(textData)
    console.log("fakeAudioData", fakeAudioData)
    if (test) run_test()
  });
}

const addEvents = function () {
  socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log("socketio connected!")
  });

  socket.on('detection_data', onDetectionData)

  wavesurfer0.on('ready', onAudioReady);
  wavesurfer1.on('ready', onAudioReady);

  wavesurfer0.on('finish', onAudioEnd);
  wavesurfer1.on('finish', onAudioEnd);

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
  if (Date.now() - lastTimePlayed < 2000 || wavesurfer0.isPlaying() || wavesurfer1.isPlaying()) {
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
  let wavDataURI = null
  
  if (fake_audio) {
    wavDataURI= interpolateDataWithFakeAudio(text)
    cur_length = text.length
  } else {
    wavDataURI= text2Audio(text, false, 0.1)
    cur_length = text.length
  }
  
  cur_wavesurfer.load(wavDataURI)
  // textEl.innerText=text
}

// returns waveDataURI
const interpolateDataWithFakeAudio = function (text) {
  let samples = text2numbers(text)
  console.log("samples.length > fakeAudioData.length", samples.length , fakeAudioData.length, samples.length-fakeAudioData.length)
  if (samples.length > fakeAudioData.length) {
    samples.splice(fakeAudioData.length, samples.length-fakeAudioData.length);
  } else {
    samples.splice(fakeAudioData.length, fakeAudioData.length-samples.length);
  }
  
  console.log("samples.length > fakeAudioData.length", samples.length , fakeAudioData.length, samples.length-fakeAudioData.length)

  noiseScale = 0.1+Math.random()*0.9
  let nd = 1/1000
  let noiseData = text.split("").map((d, i) => {
    return Math.min((1 + noise.perlin2(parseFloat(i)*nd,Math.random()*1000+parseFloat(i)*nd)/2)*noiseScale, 1)
  })

  samples = samples.map((n, i) => {
    let noise = noiseData[i]
    let fakeAudioNumber = parseFloat(fakeAudioData[i])
    // console.log("fakeAudioNumber", fakeAudioNumber)
    let newNumber = fakeAudioNumber*noise + n*(1-noise)
    return Math.floor(newNumber)
  })

  return samples2audio(samples)
}

const onAudioReady = function () {
  console.log("onAudioReady!", cur_wavesurfer)
  if (random_speed) {
    if (fake_audio) {
      curPlaybackRate = (0.15+Math.random()*0.85)*noiseScale
    } else {
      curPlaybackRate = 0.1+Math.random()*0.8
    }
    console.log(curPlaybackRate, noiseScale)
  } else {
    curPlaybackRate = playbackRate
  }

  updateLogs()
  
  cur_wavesurfer.setPlaybackRate(curPlaybackRate)
  cur_wavesurfer.volume = volume
  cur_wavesurfer.loop = loop
  cur_wavesurfer.play();
  movePlaybackBar(cur_wavesurfer.getDuration());
  cur_wavesurfer.setCursorColor('blue')
}

const movePlaybackBar = function (duration) {
  barEl.className = "bar start"
  var seconds = duration / curPlaybackRate
  console.log("seconds", seconds)
  barEl.style.transition = `left ${seconds}s linear, opacity 0.4s`
  barEl.className = "bar play"
  setTimeout(() => {
    barEl.style.transition = `opacity 0.4s`
    barEl.className = "bar hidden"
    setTimeout(() => {
      barEl.className = "bar hidden start"
    }, 400)
  }, seconds * 1000)
}

const updateLogs = () => {
  $sample_rate.textContent = " " + sample_rate;
  $lastTimePlayed.textContent = " " + lastTimePlayed;
  $curPlaybackRate.textContent = " " + curPlaybackRate;
  $cur_length.textContent = " " + cur_length;
  $noiseScale.textContent = " " + noiseScale;
}

const onAudioEnd = function () {
  lastTimePlayed = Date.now()
  wavesurfer0.setCursorColor('transparent')
  wavesurfer1.setCursorColor('transparent')
}

const run_test = () => {
  onDetectionData({"text": test_text})
  setInterval(() => {
    onDetectionData({"text": test_text})
  }, 5000)
}

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

init()