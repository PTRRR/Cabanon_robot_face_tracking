from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils
import threading

# Keep track of time
currentTime = time.time()
lastTime = currentTime

# How much time we wait until we can take a new image
deltaTime = 5 #sec
nextTime =  currentTime + deltaTime

# Get pathes
basePath = "/home/pi/Desktop/FaceTracking/FaceTracking_test_1/"
cascadeFilesPaths = ["HS.xml", "haarcascade_frontalface_default.xml", "haarcascade_profileface.xml", "haarcascade_eye.xml", "Mouth.xml"]

# Create multiple the haar cascade to detect a maximum of facial features
# We want to bo sure that the script detects a person if there is one
cascades = [None] * len(cascadeFilesPaths)

fileIndex = 0;
for file in cascadeFilesPaths:
    cascades[fileIndex] = cv2.CascadeClassifier(basePath + file)
    fileIndex += 1
    
# Create an external thread

featuresList = [[None]] * 20
currentThread = None;

class faceThread (threading.Thread):
    def __init__(self, cascades, gray, featuresList):
        threading.Thread.__init__(self)
        self.cascades = cascades
        self.gray = gray
        self.featuresList = featuresList
    def run(self):
        check_faces(self.cascades, self.gray, self.featuresList)
    
# Create a function that will be executed in an external thred.

def check_faces(cascades, gray, featuresList):
    
    cascadeIndex = 0;
    
    for cascade in cascades:
        
        features = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
        )
    
        if len(features) > 0:
        
            print " Found {0} features!".format(len(features))
            
            # Draw a rectangle around the faces
            for feature in featuresList:
                feature = [None]
                
            featuresIndex = 0;
            for (x, y, w, h) in features:
                if featuresIndex < len(featuresList):
                    featuresList[featuresIndex] = [x, y, w, h]
                    featuresIndex += 1;
            
            break
        
        if cascadeIndex == len(cascades) - 1 and len(features) == 0:
            
            print "Noting found"
        
        cascadeIndex += 1

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
    
    if currentThread == None:
        currentThread = faceThread(cascades, gray, featuresList)
        currentThread.start()
        
    else:
        if currentThread.isAlive() is not True:
            currentThread = None
    
    # Check for facial features in the list passed to the facial_thread
    print featuresList
    for feature in featuresList:
        if len(feature) == 4:
            x = feature[0]
            y = feature[1]
            w = feature[2]
            h = feature[3]
            cv2.circle(image, (x+w/2, y+h/2), int((w+h)/3), (255, 255, 255), 1)
            
    currentTime = time.time()
    
    if currentTime > nextTime:
        
        nextTime = currentTime + deltaTime
        print "haha"
    
    lastTime = currentTime
    
    # show the frame
    cv2.imshow("Frame", image)
        
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
        
  
        

