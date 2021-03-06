######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 10/27/19
# Description:
# This program uses a TensorFlow Lite model to perform object detection on a live webcam
# feed. It draws boxes and scores around the objects of interest in each frame from the
# webcam. To improve FPS, the webcam object runs in a separate thread from the main program.
# This script will work with either a Picamera or regular USB webcam.
#
# This code is based off the TensorFlow Lite image classification example at:
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
#
# I added my own method of drawing boxes and labels using OpenCV.
#
# Edits Made by Sara Fagin
# Date: 12/4/21
# Notes:
# All changes made to the original code are marked by an 'Edit#' tag
# These edits were made to work with our specific implementation of
# TensorFlow Lite, where the number of objects detected was the goal of the
# detection portion of the code, along with communicating this value to
# other remote nodes and using these values to control a set of traffic lights.
#
# Additional information can be found at our github:


# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
import csv
import socket
from threading import Thread
from datetime import datetime
import importlib.util
# Needed for Traffic Control & Multiprocessing
import RPi.GPIO as GPIO
import multiprocessing
from queue import Queue

manager = multiprocessing.Manager()
#shared_queue = manager.Queue()
shared_queue1 = manager.Queue()
shared_queue2 = manager.Queue()
shared_queue3 = manager.Queue()
shared_queue4 = manager.Queue()

# GPIO Pins
## Supports up to 4 Traffic Light Sets
rLED1 = 25  # Traffic Light 1
yLED1 = 8   # Traffic Light 1
gLED1 = 7   # Traffic Light 1
rLED2 = 16  # Traffic Light 2
yLED2 = 20  # Traffic Light 2
gLED2 = 21  # Traffic Light 2
rLED3 = 2   # Traffic Light 3
yLED3 = 3   # Traffic Light 3
gLED3 = 4   # Traffic Light 3
rLED4 = 17  # Traffic Light 4
yLED4 = 27  # Traffic Light 4
gLED4 = 22  # Traffic Light 4

# Edit#: Global Variable to select Camera
index = 0

# Debug Mode, 1 = On, 0 = Off
debug = 0

# Edit#: Total Traffic Counts for Remote and Local nodes
## Used to determine which traffic transition mode should be implemented
local_traffic = 0
remote_traffic = 0

# Edit#: Traffic Modes and Mode Phases/Counts
## LED pattern and time each phase should last (sec) for Normal Mode
normal_phases1 = [rLED1, gLED1, yLED1]
normal_phases2 = [rLED2, gLED2, yLED2]
normal_phases3 = [rLED3, gLED3, yLED3]
normal_phases4 = [rLED4, gLED4, yLED4]
normal_counts = [60, 50, 10]
## LED pattern and time each phase should last (sec) for Altered Mode
altered_phases1 = [rLED1, gLED1]
altered_phases2 = [rLED2, gLED2]
altered_phases3 = [rLED3, gLED3]
altered_phases4 = [rLED4, gLED4]
altered_counts = [60, 60]

## Indicates which mode should be running
### Error Mode = 0
### Normal Mode = 1
### Altered Mode = 2
traffic_mode = 0

local_traffic_count = 0

# Edit#: Creating Socket Object for global use
s_global = socket.socket()
if debug:
    print ("Successfully Created Global Socket")

# Edit#: Function to Open a Socket Connection as the Server and
# receive/send traffic information
def socketServerStart():

    # Creating Socket Object
    #s = socket.socket()
    #print ("Socket successfully created")

    # Reserving Port
    port = 3600

    # Binding to port
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    global s_global
    s_global.bind(('', port))
    print ("Socket bound to %s" %(port))

    # put the socket into listening mode
    s_global.listen(5)
    print ("Socket is Listening")

# Edit#: Function to Open a Socket Connection as the Server and
# receive/send traffic information
def socketServerRun(detected_cnt):

    # Establish connection with client.
    c, addr = s_global.accept()
    print ('\nGot connection from', addr )

    # Test, respond to connection.
    #msg = "Objects Detected on Server Node: %d\n" % count
    msg = "%d" % count
    c.send(msg.encode())

    #Sending content of own object_detected file back
    #with open('object_detected.csv', 'rb') as f:
    #    c.sendfile(f,0)

    # Write to a file
    rcvfile = c.recv(1024)
    f = open('rcvd_file.txt','wb')
    #while rcvfile:
    if debug:
        print("Printing Entry to Console")
        #print to the console
        print(rcvfile.decode())
    global remote_traffic
    remote_traffic = int(rcvfile.decode())
    #remote_traffic = rcvfile.decode()
    if debug:
        print("Writing Entry to File\n")
    f.write(rcvfile)
        #print("Receiving Next Entry")
        #rcvfile = c.recv(1024)
        #print("Moving to Next Loop Iteration")
    f.close

    # put the socket into listening mode
    #s.listen(5)
    #print ("socket is listening")

    # Close the connection with the client
    #c.shutdown(socket.SHUT_RDWR)
    c.close()

# Edit#: Function to Open a Socket Connection as the Server and
# receive/send traffic information
def socketClient(detected_cnt):
    # Creating Socket
    # AF_INET = IPv4
    # SOCK_STREAM = TCP protocol
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if debug:
            print ("\nSuccessfully Created Local Socket")
    except socket.error as err:
        print ("Socket Creation Failed with Error %s" %(err))

    # Port set for Node Communication Socket
    port = 3600

    try:
        host_ip = socket.gethostbyname('192.168.86.26')
    except socket.gaierror:

        # this means could not resolve the host
        print ("There was an error resolving the host")
        sys.exit()

    # connecting to the server
    s.connect((host_ip, port))

    if debug:
        print ("The socket has successfully connected to Server Node")

    #msg = "Objects Detected on Client Node: %d\n" % count
    msg = "%d" % count
    s.send(msg.encode())

    #Sending content of own object_detected file back
    #with open('object_detected.csv', 'rb') as f:
    #    s.sendfile(f,0)

    # Write to a file
    rcvfile = s.recv(1024)
    f = open('rcvd_file.txt','wb')
    #while rcvfile:
    if debug:
        print("Printing Entry to Console")
        #print to the console
        print(rcvfile.decode())
    global remote_traffic
    remote_traffic = int(rcvfile.decode())
    #remote_traffic = rcvfile.decode()
    if debug:
        print("Writing Entry to File\n")
    f.write(rcvfile)
        #print("Receiving Next Entry")
        #rcvfile = s.recv(1024)
        #print("Moving to Next Loop Iteration")
    f.close

# Edit#:
socketMode = input("Run this Node in (S)erver or (C)lient mode?: ")
if (socketMode == "S"):
    socketServerStart()

# Edit 04: Added Function to write label output to CSV file
def logWrite(label_out):
    dateTimeObj = datetime.now()
    timeObj = dateTimeObj.time()
    #dateObj = dateTimeObj.date()
    file = "object_detected.csv"
    headers = ['Time Stamp', 'Output']
    row_data = [timeObj.strftime("%H:%M:%S.%f"), label_out]

    # Checking if Log file exists
    if not os.path.exists(file):
        print("Creating "+file)

        # creating file and adding column headers
        with open(file, 'w') as csvfile:
            # creating the csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the column headers
            csvwriter.writerow(headers)
            # close the csv file
            csvfile.close()

    # appending new row to log file
    with open(file, 'a') as csvfile:
        # creating the csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the data row
        csvwriter.writerow(row_data)
        # close csv file
        csvfile.close()

# Edit#: Added Traffic Light Controller
def traffic_control(light_num, shared_queue):
    if light_num == 1:
        if debug:
            print("traffic process 1")
        LED1 = rLED1
        LED2 = gLED1
        LED3 = yLED1
        aLED1 = rLED1
        aLED2 = gLED1
        eLED = rLED1
    if light_num == 2:
        if debug:
            print("traffic process 2")
        LED1 = rLED2
        LED2 = gLED2
        LED3 = yLED2
        aLED1 = rLED2
        aLED2 = gLED2
        eLED = rLED2
    if light_num == 3:
        if debug:
            print("traffic process 3")
        LED1 = gLED3
        LED2 = yLED3
        LED3 = rLED3
        aLED1 = gLED3
        aLED2 = rLED3
        eLED = rLED3
    if light_num == 4:
        if debug:
            print("traffic process 4")
        LED1 = gLED4
        LED2 = yLED4
        LED3 = rLED4
        aLED1 = gLED4
        aLED2 = rLED4
        eLED = rLED4
    # Setting up Normal Traffic Phase Queue
    # Pattern: Red -> Green -> Yellow
    norm_queue = Queue()
    norm_queue.put(LED1)
    norm_queue.put(LED2)
    norm_queue.put(LED3)

    # Setting up Alternate Traffic Phase Queue
    # Pattern: Red -> Green
    alt_queue = Queue()
    alt_queue.put(aLED1)
    alt_queue.put(aLED2)

    # Setting up Error Traffic Phase Queue
    # Pattern: Red
    err_queue = Queue()
    err_queue.put(eLED)

    # Setting up GPIO for LEDs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)

    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)

    # Setting default value of mode to 0
    ## 0 = Error Phase
    ## 1 = Normal Phase
    ## 2 = Altered Phase
    mode = 0
    time.sleep(1)
    try:
        while True:
            # If A mode value has been added to the shared_queue
            ## This indicates a phase change.
            ## Otherwise continue using current value of mode
            if not shared_queue.empty():
                mode_temp = shared_queue.get()
                if not mode == mode_temp:
                    mode = mode_temp
                    #making sure norm_queue is reset when mode changes
                    temp = norm_queue.get()
                    if temp != LED1:
                        norm_queue.put(temp)
                        temp = norm_queue.get()
                        if temp != LED1:
                            norm_queue.put(temp)
                            temp = norm_queue.get()
                    norm_queue.put(temp)
                    #making sure alt_queue is reset when mode changes
                    temp = alt_queue.get()
                    if temp != LED1:
                        alt_queue.put(temp)
                        temp = alt_queue.get()
                    alt_queue.put(temp)

            if mode == 1:
                led = norm_queue.get()
                norm_queue.put(led)
            elif mode == 2:
                led = alt_queue.get()
                alt_queue.put(led)
            else:
                led = err_queue.get()
                err_queue.put(led)

            # Currently Flashes LEDs for each stage of phase
            GPIO.output(led, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led, GPIO.LOW)
            #time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        #print("\nflash_led exiting\n")
        pass

# Adds a mode value to the shared_queue, prompting traffic_control to change
## phases.
def mode_set(traffic_mode):
    try:
        shared_queue1.put(traffic_mode)
        shared_queue2.put(traffic_mode)
        shared_queue3.put(traffic_mode)
        shared_queue4.put(traffic_mode)
    except KeyboardInterrupt:
        #print("ctrl_led exiting\n")
        pass

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    #Edit 08: Added index parameter to select specific camera
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        #Edit 09: Changed from 0 to index to allow multiple camera options
        global index
        self.stream = cv2.VideoCapture(index)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5) #Note: Change this value to allow more or less objects to be detected
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1280x720')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
# Edit 10: Added index values to change between cameras 1-4
index = 0
videostream01 = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)
index = 4
videostream02 = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)
index = 8
videostream03 = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)
index = 20
videostream04 = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)

# Edit 17: Holds streams to loop through cameras
streams = [videostream01, videostream02]

subproc1 = multiprocessing.Process(target=traffic_control, args=(1, shared_queue1))
subproc2 = multiprocessing.Process(target=traffic_control, args=(2, shared_queue2))
subproc3 = multiprocessing.Process(target=traffic_control, args=(3, shared_queue3))
subproc4 = multiprocessing.Process(target=traffic_control, args=(4, shared_queue4))
subproc1.start()
time.sleep(1)
subproc2.start()
time.sleep(1)
subproc3.start()
time.sleep(1)
subproc4.start()
#subproc.join()

#for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
try:

    while True:
        # Edit 05: Replaced with logWrite Function
        # Edit 01: File to hold output
        #file = open('object_detected', 'w')

        # Edit#: Add a count variable to index number of objects detected.
        ## Currently just counts all detected objects, not cars specifically
        count = 0

        # Edit 18: Beginning Loop to capture each camera's feed
        for frames in streams:
            # Start timer (for calculating frame rate)
            t1 = cv2.getTickCount()

            # Edit 16: Changed this to allow cycling betwen Cameras 1-4
            # Grab frame from video stream
            #frame1 = videostream01.read()
            frame1 = frames.read()

            # Acquire frame and resize to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'],input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
            #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)



            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))

                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

                    # Edit 06:Replaced with logWrite Function
                    # Edit 02: Begins writing object label to file
                    #file.write(label)
                    #file.write('\n')
                    logWrite(label)
                    # Edit 12: Added for troubleshooting
                    print("Detected a", label)
                    count = count + 1

        if (socketMode == "S"):
            socketServerRun(count)
        elif (socketMode == "C"):
            socketClient(count)
        else:
            print("No Socket Mode Selected")

        local_traffic = count
        print("======< Objects Detected: %d >======" % (count))
        print("Local Node Object Count: %d" % (local_traffic))
        print("Remote Node Object Count: %d" % (remote_traffic))

        if local_traffic > remote_traffic:
            mode_set(2)
            if debug:
                print("Local Traffic Greater than Remote Traffic.")
            print("Running Altered Traffic Phase\n")
        else:
            mode_set(1)
            if debug:
                print("Local Traffic Less than or Equal to Remote Traffic.")
            print("Running Normal Traffic Phase\n")

        # Draw framerate in corner of frame
        #cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        #Edit 14: Commented out because unneeded while Edit 13 is in effect
        #cv2.putText(frame,'Objects Detected: %d' % (count),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        #Edit 13: Commented out to to avoid crash
        #cv2.imshow('Object detector', frame)

        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc= 1/time1

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

        time.sleep(12)
except KeyboardInterrupt: #Edit 15: Added to allow graceful exit using Ctrl+c
    #Edit 07: No longer needed, file closed in logWrite Function
    #Edit 03: Closes the written to file
    #file.close()
    # Clean up
    cv2.destroyAllWindows()
    for frames in streams:
        frames.stop()
    #videostream.stop()
    print("\n")
    print("Exiting Program\n")
    pass
