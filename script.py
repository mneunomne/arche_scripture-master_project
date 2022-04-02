"""
An example of detecting ArUco markers with OpenCV.
"""

import cv2
import sys
import cv2.aruco as aruco
import numpy as np
from pynput import keyboard
import threading

adaptiveThreshWinSizeMin = 27
adaptiveThreshWinSizeMax = 133
adaptiveThreshWinSizeStep = 10
adaptiveThreshConstant = 7

def on_press(key):
    global adaptiveThreshWinSizeMin
    global adaptiveThreshWinSizeMax
    global adaptiveThreshWinSizeStep
    global adaptiveThreshConstant
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
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
    print('{0} released'.format(key))
 

def keyboard_listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Collect events until released



def run_opencv():

    device = 1  # Front camera
    try:
        device = int(sys.argv[1])  # 0 for back camera
    except IndexError:
        pass


    cap = cv2.VideoCapture(device)

    cv2.startWindowThread()
    cv2.namedWindow("preview")

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
        corners, ids, _ = aruco.detectMarkers(
            frame, aruco_dict, parameters=parameters)
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        """
        if len(corners) == 4:
            array = []
            i = 0
            for c in corners:
                array.append(c[0][3])
                inner_corner = c[0]
                print(inner_corner, inner_corner)

            cnt = np.array(array)

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
        """
        # Display the resulting frame
        cv2.imshow('preview', frame)
        cv2.imshow('mais', threshInv)

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