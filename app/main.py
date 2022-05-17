"""
An example of detecting ArUco markers with OpenCV.
"""
import argparse
import os
import cv2
from cv2 import threshold
import cv2.aruco as aruco
import numpy as np
import math
from dotenv import load_dotenv
from utils import *
import threading
from flask_server import app, sendVideoOutput, socketio
from kiosk import run_kiosk

# load .env file
load_dotenv()

# webcam device
DEVICE = int(os.environ.get("WEBCAM"))

# flask server settings
FLASK_SERVER_IP = os.environ.get("FLASK_SERVER_IP")
FLASK_SERVER_PORT = os.environ.get("FLASK_SERVER_PORT")

# full server url for connection to the socket
server_url = "http://{}:{}/".format(FLASK_SERVER_IP, FLASK_SERVER_PORT)

# default values
adaptiveThreshWinSizeMin = 3
adaptiveThreshWinSizeMax = 90
adaptiveThreshWinSizeStep = 10
adaptiveThreshConstant = 2
margin=45
bin_threshold=100
captureBits=False
default_alpha = 1  # Contrast control (1.0-3.0)
beta = 0  # Brightness control (0-100)
plate_id = None
rows=220
cols=200
width=297*5
height=420*5
video_output=None
scale=2

# Argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-k', '--kiosk', default=False, action='store_true')
parser.add_argument('-f', '--flask', default=False, action='store_true')
parser.add_argument('-d', '--debug', default=False, action='store_true')
parser.add_argument('-o', '--output', type=str, default="default")
args = parser.parse_args()
print(args)
# switches
kiosk_enabled = args.kiosk
flask_enabled = args.flask
debug = args.flask
flask_output = args.output

def init(): 
    # start flask thread
    if flask_enabled:
        thread_flask = threading.Thread(target=socketio.run, args=(app, FLASK_SERVER_IP, FLASK_SERVER_PORT,))
        thread_flask.start()

    # start kiosk thread 
    if kiosk_enabled:
        thread_kiosk = threading.Thread(target=run_kiosk, args=(server_url,))
        thread_kiosk.start()
    
    # start opencv
    run_opencv()

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def run_opencv():
    global captureBits
    global rows
    global cols
    global plate_id
    global adaptiveThreshWinSizeMin
    global adaptiveThreshWinSizeMax
    global adaptiveThreshWinSizeStep
    global adaptiveThreshConstant
    global margin
    global video_output

    # caputure webcam feed
    cap = cv2.VideoCapture(DEVICE)

    # create window
    cv2.startWindowThread()
    cv2.namedWindow("debug")
    cv2.namedWindow("cropped")
    cv2.namedWindow("data")

    # GUI elements of image processing
    cv2.createTrackbar('brightness','debug',0,255,nothing)
    cv2.createTrackbar('alpha','debug',default_alpha*10,100,nothing)
    cv2.createTrackbar('beta','debug',0,255,nothing)
    cv2.createTrackbar('margin','debug',margin,100,nothing)

    # GUI elements for fiducial tracking values
    cv2.createTrackbar('adaptiveThreshWinSizeMin', 'debug', adaptiveThreshWinSizeMin, 100, nothing)
    cv2.createTrackbar('adaptiveThreshWinSizeMax', 'debug', adaptiveThreshWinSizeMax, 100, nothing)
    cv2.createTrackbar('adaptiveThreshWinSizeStep', 'debug', adaptiveThreshWinSizeStep, 100, nothing)
    cv2.createTrackbar('adaptiveThreshConstant', 'debug', adaptiveThreshConstant, 100, nothing)


    cropped = np.zeros((height,width,3), np.uint8)
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Check if frame is not empty
        if not ret:
            continue
        
        brightness = cv2.getTrackbarPos('brightness', 'debug')
        alpha = cv2.getTrackbarPos('alpha', 'debug')/10
        beta = cv2.getTrackbarPos('beta', 'debug')-5
        margin = cv2.getTrackbarPos('margin', 'debug')

        adaptiveThreshWinSizeMin = cv2.getTrackbarPos('adaptiveThreshWinSizeMin', 'debug')
        adaptiveThreshWinSizeMax = cv2.getTrackbarPos('adaptiveThreshWinSizeMax', 'debug')
        adaptiveThreshWinSizeStep = cv2.getTrackbarPos('adaptiveThreshWinSizeStep', 'debug')
        adaptiveThreshConstant = cv2.getTrackbarPos('adaptiveThreshConstant', 'debug')

        # image used for interpretation
        reading_frame = frame.copy()
        output_frame = frame.copy()

        output_frame = cv2.resize(output_frame, (1920*scale, 1080*scale))

        # only use red channel
        reading_frame[:, :, 0] = np.zeros([reading_frame.shape[0], reading_frame.shape[1]])
        reading_frame[:, :, 1] = np.zeros([reading_frame.shape[0], reading_frame.shape[1]])

        reading_frame = increase_brightness(reading_frame, brightness)
        reading_frame = cv2.convertScaleAbs(reading_frame, alpha=alpha, beta=beta)
        
        # image to used on debug interface
        debug_frame = reading_frame.copy()
        
        # (some extra unused convertions)
        # Convert from BGR to RGB
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # (T, threshInv) = cv2.threshold(gray, adaptiveThreshWinSizeMax, 255, cv2.THRESH_BINARY_INV)

        # fiducial markers parameters
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin
        parameters.adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax
        parameters.adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep
        parameters.adaptiveThreshConstant = adaptiveThreshConstant

        # detect fiducials
        markers_pos, ids, _ = aruco.detectMarkers(reading_frame, aruco_dict, parameters=parameters)
        # draw detected markers on the captured image
        debug_frame = aruco.drawDetectedMarkers(debug_frame, markers_pos, ids)
        output_frame = aruco.drawDetectedMarkers(output_frame, np.array(markers_pos)*scale, ids)

        if ids is not None:
            # order of fiducial id's
            corner_ids=[[1],[2],[4],[3]]
            # check if image has all id's
            has_all = all(x in ids for x in corner_ids)
            # if it has all ids... 
            if has_all and len(ids) >= 4:
                # get corner positions from ids
                corners=getCornersFromIds(corner_ids, ids, markers_pos)
                # make point array to construct rect
                points = np.int0(corners)

                eight_points = None
                # get the rest of the markers
                if len(ids) >= 8:
                    tl = corners[0]
                    tr = corners[1]
                    bl = corners[3]
                    br = corners[2]

                    cols = findBetweenMarker(markers_pos, ids, tl, tr, corner_ids)[0]
                    rows = findBetweenMarker(markers_pos, ids, tr, br, corner_ids)[0]
                    plate_id = findBetweenMarker(markers_pos, ids, bl, br, corner_ids)[0]
                    fontSize = findBetweenMarker(markers_pos, ids, tl, bl, corner_ids)[0]

                    ## Here is to try to use the other markers to do the corner...
                    corner_ids = [[1], [cols], [2], [rows],[4], [plate_id],[3], [fontSize]]
                    corners=getCornersFromIds(corner_ids, ids, markers_pos)
                    eight_points = np.int0(corners)

                # Define corresponding points in output image
                input_pts = np.float32(points)
                output_pts = np.float32([[0,0],[width,0],[width,height],[0,height]])

                # Get perspective transform and apply it
                M = cv2.getPerspectiveTransform(input_pts,output_pts)
                cropped = cv2.warpPerspective(reading_frame,M,(width,height))

                # alpha = 1  # Contrast control (1.0-3.0)
                # beta = 0  # Brightness control (0-100)
                #cropped = cv2.convertScaleAbs(cropped, alpha=alpha, beta=beta)
                
                cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                #(T, cropped) = cv2.threshold(cropped, adaptiveThreshWinSizeMax, 255, cv2.THRESH_BINARY_INV)

                if eight_points is not None:
                    cv2.polylines(debug_frame, [eight_points], 1, (255, 0, 0), 2)
                    cv2.polylines(output_frame, [eight_points], 1, (255, 0, 0), 2)
                else:
                    cv2.polylines(debug_frame, [points], 1, (255, 0, 0), 2)
                    cv2.polylines(output_frame, [points], 1, (255, 0, 0), 2)
            
                if captureBits == True or True:

                    blur = cv2.GaussianBlur(cropped,(5,5),0)
                    ret3,cropped = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                    data_img = captureBitsFromImage(cropped, width, height, rows, cols)
                    #cv2.imshow('data', th3)
                    captureBits=False

        # why this? 
        # img_grey = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(img_grey,(5,5),0)
        # ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # th3 = cv2.threshold(img_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # debug values
        params = {
            "brightness": brightness,
            "alpha": alpha,
            "beta": beta,
            "margin": margin,
            "adaptiveThreshWinSizeMin": adaptiveThreshWinSizeMin,
            "adaptiveThreshWinSizeMax": adaptiveThreshWinSizeMax,
            "adaptiveThreshWinSizeStep": adaptiveThreshWinSizeStep,
            "adaptiveThreshConstant": adaptiveThreshConstant,
            "cols": cols,
            "rows": rows,
            "plate_id": plate_id
        }
        debugValue(params, debug_frame)
        
        # pick vidoe output based on args
        if flask_output == 'default':
            video_output = output_frame.copy()
        elif flask_output == 'debug':
            video_output = debug_frame.copy()
        elif flask_output == 'raw':
            video_output = frame.copy()
        # send video to flask
        sendVideoOutput(video_output)

        # Display the resulting frame
        cv2.imshow('debug', debug_frame)
        cv2.imshow('cropped', cropped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def debugValue(params, img):
    y=30
    for key in params:
        cv2.putText(img, str(key),[0, y], cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
        cv2.putText(img, str(params[key]),[400, y], cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
        y=y+30


def captureBitsFromImage(img, width, height, rows, cols):
    global margin
    data_image = np.zeros((rows*4,cols*4,1), np.uint8)
    interval = (width-margin*2)/(cols)
    array_x = np.arange(margin+interval/2, width-margin, interval)
    array_y = np.arange(margin+interval/2, height-margin, interval)
    # print("len", len(array_x))
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
    # print(data_y, data_x)
    numbers = bits2numbers(bin_array)
    textSound = numbers2text(numbers) 
    # print("send text data!", textSound)
    socketio.emit('detection_data', {'text': textSound})

# run!
init()