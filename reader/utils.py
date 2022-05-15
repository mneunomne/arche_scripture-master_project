alphabet = "撒健億媒間増感察総負街時哭병体封列効你老呆安发は切짜확로감外年와모ゼДが占乜산今もれすRビコたテパアEスどバウПm가бうクん스РりwАêãХйてシжغõ小éजভकöলレ入धबलخFসeवমوযиथशkحくúoनবएদYンदnuনمッьノкتبهtт一ادіاгرزरjvةзنLxっzэTपнлçşčतلイयしяトüषখথhцहیরこñóহリअعसमペيフdォドрごыСいگдとナZকইм三ョ나gшマで시Sقに口س介Иظ뉴そキやズВ자ص兮ض코격ダるなф리Юめき宅お世吃ま来店呼설진음염론波密怪殺第断態閉粛遇罩孽關警"

def bits2numbers (bin_array):
  s = "".join(bin_array)
  numbers = [s[i:i+8] for i in range(0, len(s), 8)]
  return numbers

def numbers2text (numbers):
  bits = map(lambda s: int(s, 2), numbers) 
  bits = map(lambda n: alphabet[n], bits) 
  textSound = "".join(list(bits))
  return textSound