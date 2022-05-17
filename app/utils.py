import numpy as np

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

def findBetweenMarker (markers_pos, ids, a, b, corner_ids):
    c = np.average(np.array([a, b]), axis=0)
    idx=0
    i=0
    last_val=99999
    for marker in markers_pos:
        if ids[i] in corner_ids:
            i+=1
            continue
        m = np.mean(marker[0], axis=0)
        val = dist(m[0], m[1], c[0], c[1])
        if last_val>val:
            last_val = val
            idx=i
        i+=1
    return ids[idx]

def getCornersFromIds(corner_ids, ids, markers_pos):
    corners=[]
    for corner_id in corner_ids:
        item_index=0
        for id in ids:
            if (id == corner_id):
                break
            item_index+=1
        center = np.mean(markers_pos[item_index][0], axis=0)
        center_coordinates = (int(center[0]), int(center[1]))          
        corners.append(center_coordinates)
    return corners

def dist(x1,y1,x2,y2):
  return ((x2-x1)**2 + (y2-y1)**2)**0.5
  
def nothing(a):
    return None