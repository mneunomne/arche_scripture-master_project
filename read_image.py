import cv2
import numpy as np
import math
import json
 
data=0
with open('762.json') as json_file:
  data = json.load(json_file)

interval = 17
margin=74
spacing=1

img = cv2.imread('762.png')

alphabet = "撒健億媒間増感察総負街時哭병体封列効你老呆安发は切짜확로감外年와모ゼДが占乜산今もれすRビコたテパアEスどバウПm가бうクん스РりwАêãХйてシжغõ小éजভकöলレ入धबलخFসeवমوযиथशkحくúoनবएদYンदnuনمッьノкتبهtт一ادіاгرزरjvةзنLxっzэTपнлçşčतلイयしяトüषখথhцहیরこñóহリअعसमペيフdォドрごыСいگдとナZকইм三ョ나gшマで시Sقに口س介Иظ뉴そキやズВ자ص兮ض코격ダるなф리Юめき宅お世吃ま来店呼설진음염론波密怪殺第断態閉粛遇罩孽關警"

rows=data['rows']
cols=data['cols']

height,width,_ = img.shape

_interval = (width-margin*2)/(cols)

print(_interval)

array_x = np.arange(margin+_interval/2, width-margin, _interval)
array_y = np.arange(margin+_interval/2, height-margin, _interval)

cv2.startWindowThread()
cv2.namedWindow("preview")

#data = np.zeros((height,width,3), np.uint8)

print(height,width)

bin_array = [] 
for pos_y in array_y:
  for pos_x in array_x:
    k = img[math.floor(pos_y), math.floor(pos_x)]
    cv2.circle(img, [int(pos_x), int(pos_y)], 1, (255, 0, 255), 1)
    #print(k)
    bin = '1' if k[0] < 200 else '0'
    bin_array.append(bin)

s = "".join(bin_array)

numbers = [s[i:i+8] for i in range(0, len(s), 8)]
#print(list(numbers))
bits = map(lambda s: int(s, 2), numbers) 
#print(list(bits))
bits = map(lambda n: alphabet[n], bits) 
print("".join(list(bits)))

while True:
  cv2.imshow('preview', img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break