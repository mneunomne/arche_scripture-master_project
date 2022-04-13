"""
An example of detecting ArUco markers with OpenCV.
"""

import cv2
import sys

from cv2 import threshold
import cv2.aruco as aruco
import numpy as np
from pynput import keyboard
import threading
import math
import socketio

# Socket.io client
server_path = 'http://localhost:3000' # node server location
socket_connected = False
# Connect to socket.io server
try:
    socketClient = socketio.Client()
    socketClient.connect(server_path)
except socketio.exceptions.ConnectionError as err:
    socket_connected = False
    print("Error on socket connection")
else:
    socket_connected = True

alphabet = "撒健億媒間増感察総負街時哭병体封列効你老呆安发は切짜확로감外年와모ゼДが占乜산今もれすRビコたテパアEスどバウПm가бうクん스РりwАêãХйてシжغõ小éजভकöলレ入धबलخFসeवমوযиथशkحくúoनবएদYンदnuনمッьノкتبهtт一ادіاгرزरjvةзنLxっzэTपнлçşčतلイयしяトüषখথhцहیরこñóহリअعसमペيフdォドрごыСいگдとナZকইм三ョ나gшマで시Sقに口س介Иظ뉴そキやズВ자ص兮ض코격ダるなф리Юめき宅お世吃ま来店呼설진음염론波密怪殺第断態閉粛遇罩孽關警"

adaptiveThreshWinSizeMin = 3
adaptiveThreshWinSizeMax = 90
adaptiveThreshWinSizeStep = 10
adaptiveThreshConstant = 2
margin=45
bin_threshold=100
captureBits=False

json_data=0
#with open('762.json') as json_file:
#    json_data = json.load(json_file)

rows=220 #json_data['rows']
cols=200 #json_data['cols']

width=297 #json_data['width']*4
height=420 #json_data['height']*4

def on_press(key):
    global adaptiveThreshWinSizeMin
    global adaptiveThreshWinSizeMax
    global adaptiveThreshWinSizeStep
    global adaptiveThreshConstant
    global captureBits
    global bin_threshold
    global margin
    if key == keyboard.Key.space:
        print("SPACE")
        captureBits=True
    if hasattr(key, 'char'):
        # -----------------------
        # adaptiveThreshWinSizeMin
        # -----------------------
        if key.char == 'a':
            adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin+1
            print("adaptiveThreshWinSizeMin", adaptiveThreshWinSizeMin)
        if key.char == 'A':
            if adaptiveThreshWinSizeMin > 3:
                adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin-1
                print("adaptiveThreshWinSizeMin", adaptiveThreshWinSizeMin)
        # -----------------------
        # adaptiveThreshWinSizeMin
        # -----------------------
        if key.char == 's':
            adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep+1
            print("adaptiveThreshWinSizeStep", adaptiveThreshWinSizeStep)
        if key.char == 'S':
            adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep-1
            print("adaptiveThreshWinSizeStep", adaptiveThreshWinSizeStep)
        # -----------------------
        # adaptiveThreshWinSizeStep
        # -----------------------
        if key.char == 'd':
            adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax+1
            print("adaptiveThreshWinSizeMax", adaptiveThreshWinSizeMax)
        if key.char == 'D':
            adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax-1
            print("adaptiveThreshWinSizeMax", adaptiveThreshWinSizeMax)
        # -----------------------
        # adaptiveThreshWinSizeStep
        # -----------------------
        if key.char == 'c':
            adaptiveThreshConstant = adaptiveThreshConstant+1
            print("adaptiveThreshConstant", adaptiveThreshConstant)
        if key.char == 'C':
            adaptiveThreshConstant = adaptiveThreshConstant-1
            print("adaptiveThreshConstant", adaptiveThreshConstant)
        # -----------------------
        # Margin
        # -----------------------
        if key.char == 'm':
            margin = margin+1
            print("margin", margin)
        if key.char == 'M':
            margin = margin-1
            print("margin", margin)
        # -----------------------
        # THRESHOLD
        # -----------------------
        if key.char == 't':
            bin_threshold = bin_threshold+1
            print("bin_threshold", bin_threshold)
        if key.char == 'T':
            margin = margin-1
            bin_threshold = bin_threshold-1
            print("bin_threshold", bin_threshold)


def on_release(key):
    global captureBits
    if key == keyboard.Key.space:
        captureBits=False
    return
    #print('{0} released'.format(key))
 

def keyboard_listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def run_opencv():
    global captureBits

<<<<<<< HEAD
    device = 0 # Front camera
=======
    device = 1# Front camera
>>>>>>> f8ee0c2b4ec0282dc87aca2a25c001ff59be973a
    try:
        device = int(sys.argv[1])  # 0 for back camera
    except IndexError:
        pass

    cap = cv2.VideoCapture(device)

    cv2.startWindowThread()
    cv2.namedWindow("preview")
    cv2.namedWindow("crop")
    cv2.namedWindow("data")


    cropped = np.zeros((height,width,3), np.uint8)
    while cap.isOpened():


        # Capture frame-by-frame
        ret, frame = cap.read()
        
        #frame[:,:,2] = np.zeros([frame.shape[0], frame.shape[1]])

        # Check if frame is not empty
        if not ret:
            continue

        # Auto rotate camera
        # frame = cv2.autorotate(frame, device)

        # Convert from BGR to RGB
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (T, threshInv) = cv2.threshold(gray, adaptiveThreshWinSizeMax, 255, cv2.THRESH_BINARY_INV)


        alpha = 1.5  # Contrast control (1.0-3.0)
        beta = 0  # Brightness control (0-100)

        adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)
        parameters = aruco.DetectorParameters_create()

        parameters.adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin
        parameters.adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax
        parameters.adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep
        parameters.adaptiveThreshConstant = adaptiveThreshConstant
        #parameters.adaptiveThreshConstant = 10
        #parameters.minMarkerPerimeterRate = 0.001
        #parameters.maxMarkerPerimeterRate = 8
        #parameters.maxErroneousBitsInBorderRate = 0.8
        #parameters.adaptiveThreshWinSizeMax = 10
        
        markers_pos, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        frame = aruco.drawDetectedMarkers(frame, markers_pos, ids)

        if ids is not None:
            corner_ids=[[1],[2],[4],[3]]
            has_all = all(x in ids for x in corner_ids)

            if has_all:
                #print(corners)
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
                    #cv2.circle(frame, center_coordinates, 10, (255, 0, 255), 2)

                points = np.int0(corners)

                # Define corresponding points in output image
                input_pts = np.float32(points)
                output_pts = np.float32([[0,0],[width,0],[width,height],[0,height]])

                # Get perspective transform and apply it
                M = cv2.getPerspectiveTransform(input_pts,output_pts)
                cropped = cv2.warpPerspective(frame,M,(width,height))

                # alpha = 1  # Contrast control (1.0-3.0)
                # beta = 0  # Brightness control (0-100)
                # cropped = cv2.convertScaleAbs(cropped, alpha=alpha, beta=beta)
                
                #cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                #(T, cropped) = cv2.threshold(cropped, adaptiveThreshWinSizeMax, 255, cv2.THRESH_BINARY_INV)

                cv2.polylines(frame, [points], 1, (255, 0, 0), 2)
            
                if captureBits == True or True:

                    img_grey = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

                    blur = cv2.GaussianBlur(img_grey,(5,5),0)
                    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                    print(cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                    captureBitsFromImage(th3, width, height, rows, cols)
                    captureBits=False

        img_grey = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(img_grey,(5,5),0)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #th3 = cv2.threshold(img_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # Display the resulting frame
        cv2.imshow('preview', frame)
        cv2.imshow('cropped', th3)
        #cv2.imshow('mais', threshInv)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def captureBitsFromImage(img, width, height, rows, cols):
    global margin
    data_image = np.zeros((rows*4,cols*4,1), np.uint8)
    interval = (width-margin*2)/(cols)
    array_x = np.arange(margin+interval/2, width-margin, interval)
    array_y = np.arange(margin+interval/2, height-margin, interval)
    print("len", len(array_x))
    bin_array = [] 
    data_y = 0
    for pos_y in array_y:
        data_x=0
        for pos_x in array_x:
            k = img[math.floor(pos_y), math.floor(pos_x)]
            cv2.circle(img, [int(pos_x), int(pos_y)], 1, (255, 0, 255), 1)
            bin = '1' if k < bin_threshold else '0'
            bin_array.append(bin)
            #data_image[data_y, data_x]=k
            start_point=(int(data_x*4), int(data_y*4))
            end_point=(int(data_x*4+4), int(data_y*4+4))
            color = 255 if k > bin_threshold else 0
            data_image = cv2.rectangle(data_image, start_point, end_point, (color), -1)
            data_x+=1
        data_y+=1
    print(data_y, data_x)
    s = "".join(bin_array)
    numbers = [s[i:i+8] for i in range(0, len(s), 8)]
    cv2.imshow('data_image', data_image)
    bits = map(lambda s: int(s, 2), numbers) 
    bits = map(lambda n: alphabet[n], bits) 
    textSound = "".join(list(bits))
    print(textSound)
    if socket_connected:
        sendData(textSound)

def sendData (textSound):
    try:
        socketClient.emit('textSound', textSound)
    except socketio.exceptions.BadNamespaceError as err:
        print("error sending data", err)

thread = threading.Thread(target=keyboard_listen)
thread.start()
#thread.join()

run_opencv()