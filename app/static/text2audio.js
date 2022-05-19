const alphabet = "撒健億媒間増感察総負街時哭병体封列効你老呆安发は切짜확로감外年와모ゼДが占乜산今もれすRビコたテパアEスどバウПm가бうクん스РりwАêãХйてシжغõ小éजভकöলレ入धबलخFসeवমوযиथशkحくúoनবएদYンदnuনمッьノкتبهtт一ادіاгرزरjvةзنLxっzэTपнлçşčतلイयしяトüषখথhцहیরこñóহリअعसमペيフdォドрごыСいگдとナZকইм三ョ나gшマで시Sقに口س介Иظ뉴そキやズВ자ص兮ض코격ダるなф리Юめき宅お世吃ま来店呼설진음염론波密怪殺第断態閉粛遇罩孽關警"

const audio = document.createElement('audio');
const source = document.createElement('source');
source.setAttribute("type", "audio/wav")
audio.append(source)

const default_sample_rate = 8000
const default_bits = "8"

const text2Audio = function (text, loop) {
  var loop = loop || false 
  if (audio.duration > 0 && !audio.paused && !loop) {
    console.log("audio", audio.duration)
    return
  }
  var samples = text.split("").map(c => alphabet.indexOf(c))
  var wav = new wavefile.WaveFile();
  // Create a WaveFile using the samples
  wav.fromScratch(1, default_sample_rate, default_bits, samples);
  let wavDataURI = wav.toDataURI();
  console.log("wavDataURI", wavDataURI)
  /*
    source.src = wavDataURI;
    audio.load();
    audio.volume = volume
    audio.loop = false;
    audio.playbackRate = 0.1
    audio.play();
  */
  return wavDataURI
}

const samples2audio = function (samples) {
  var wav = new wavefile.WaveFile();
  // Create a WaveFile using the samples
  wav.fromScratch(1, default_sample_rate, default_bits, samples);
  let wavDataURI = wav.toDataURI();
  console.log("wavDataURI fake", wavDataURI)
  return wavDataURI
}

const numbers2Text = function (numbers) {
  return numbers.map(n => alphabet[n]).join('')
}

const text2numbers = function (text) {
  return text.split("").map(c => alphabet.indexOf(c))
}