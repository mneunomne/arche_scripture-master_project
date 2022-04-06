"""
An example of detecting ArUco markers with OpenCV.
"""

import cv2
import sys
import cv2.aruco as aruco
import numpy as np
from pynput import keyboard
import threading

adaptiveThreshWinSizeMin = 7
adaptiveThreshWinSizeMax = 133
adaptiveThreshWinSizeStep = 10
adaptiveThreshConstant = 7

def on_press(key):
    global adaptiveThreshWinSizeMin
    global adaptiveThreshWinSizeMax
    global adaptiveThreshWinSizeStep
    global adaptiveThreshConstant
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


def on_release(key):
    return
    #print('{0} released'.format(key))
 

def keyboard_listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def run_opencv():

    device = 0 # Front camera
    try:
        device = int(sys.argv[1])  # 0 for back camera
    except IndexError:
        pass


    cap = cv2.VideoCapture(device)

    cv2.startWindowThread()
    cv2.namedWindow("preview")
    cv2.namedWindow("crop")

    while cap.isOpened():

        # Capture frame-by-frame
        ret, frame = cap.read()

        width=874
        height=1240

        cropped = np.zeros((height,width,3), np.uint8)
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
        corners, ids, _ = aruco.detectMarkers(
            frame, aruco_dict, parameters=parameters)
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        if len(corners) == 4:
            array = []
            i = 0
            for c in corners:
                i+=1
                center = np.mean(c[0], axis=0)
                print('center', i, center)
                center_coordinates = (int(center[0]), int(center[1]))
                array.append(center_coordinates)

                _rect = cv2.minAreaRect(c[0])
                _box = cv2.boxPoints(_rect)
                _box = np.int0(_box)
                cv2.drawContours(frame, [_box], 0, (0, 0, 255), 2)
                
                cv2.circle(frame, center_coordinates, 10, (255, 0, 255), 2)


            sorted(array , key=lambda k: [k[1], k[0]])

            points = [
                array[0],
                array[1],
                array[3],
                array[2]
            ]
            points = np.int0(points)


            # Define corresponding points in output image
            input_pts = np.float32(points)
            output_pts = np.float32([[0,0],[width,0],[width,height],[0,height]])

            # Get perspective transform and apply it
            M = cv2.getPerspectiveTransform(input_pts,output_pts)
            cropped = cv2.warpPerspective(frame,M,(width,height))

            cv2.polylines(frame, [points], 1, (255, 0, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('preview', frame)
        cv2.imshow('cropped', cropped)
        #cv2.imshow('mais', threshInv)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


thread = threading.Thread(target=keyboard_listen)
thread.start()
#thread.join()

run_opencv()