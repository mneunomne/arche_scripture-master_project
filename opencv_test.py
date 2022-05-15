# importing cv2 
import cv2 
import sys

# path 
path = "test.png"
  
# Reading an image in default mode
image = cv2.imread(path)
  
# Window name in which image is displayed
window_name = 'image'

device = 0 # Front camera

try:
    device = int(sys.argv[1])  # 0 for back camera
except IndexError:
    pass

cap = cv2.VideoCapture(device)

cv2.startWindowThread()
cv2.namedWindow("preview")


while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        # Using cv2.imshow() method 
        # Displaying the image 
        cv2.imshow(window_name, frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
