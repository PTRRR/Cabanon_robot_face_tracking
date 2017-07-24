from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils

# Get user supplied values
frontalFacesCascadeFilePath = "/home/pi/Desktop/FaceTracking/FaceTracking_test_1/HS.xml"
eyeFacesCascadeFilePath = "/home/pi/Desktop/FaceTracking/FaceTracking_test_1/haarcascade_eye.xml"

# Create the haar cascade
cascades = [cv2.CascadeClassifier(frontalFacesCascadeFilePath), cv2.CascadeClassifier(eyeFacesCascadeFilePath)]
frontalFaceCascade = cv2.CascadeClassifier(frontalFacesCascadeFilePath)
profileFaceCascade = cv2.CascadeClassifier(eyeFacesCascadeFilePath)

# initialize the camera and grab a reference to the raw camera capture
defMultiplier = 2;

camera = PiCamera()
camera.resolution = (160*defMultiplier, 120*defMultiplier)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(160*defMultiplier, 120*defMultiplier))

# allow the camera to warmup
time.sleep(0.1)
lastTime = time.time()*1000.0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect frontal faces in the image
    frontalFaces = frontalFaceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
    )
    
    if len(frontalFaces) > 0:
        
        print time.time()*1000.0-lastTime," Found {0} faces!".format(len(frontalFaces))
        lastTime = time.time()*1000.0
            
    # Draw a rectangle around the faces
    for (x, y, w, h) in frontalFaces:
       cv2.circle(image, (x+w/2, y+h/2), int((w+h)/3), (255, 255, 255), 1)
       
    # show the frame
    cv2.imshow("Frame", image)
        
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
        
  
        

