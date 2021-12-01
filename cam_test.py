#cam_test.py
#Use to verify function and presence of all connected cameras
#Currently
##Camera 1 appears to be located as video00
##Camera 2 appears to be located as video04
#Unknown why video14 & video15 show as present

import cv2

def testCam(source):

    try:
        print("Creating cv2 Object")
        stream = cv2.VideoCapture(source)
    except cv2.error as e:
        print(e)
        print("Warning 1: CV2 Error for camera ", source)
    except ConnectionError:
        print("Warning 2: Connection Error for camera ", source)
    except Exception as e:
        print(e)
        print("Warning 3: Random Exception for camera ", source)

    print("Checking status of camera")
    if stream is None or not stream.isOpened():
        print("Warning 4: unable to open camera ", source)
    else:
        print("Successfully opened camera ", source)

    stream.release()

testCam(0)
testCam(1)
testCam(2)
testCam(3)
testCam(4)
testCam(5)
testCam(6)
testCam(7)
testCam(8)
testCam(9)
testCam(10)
testCam(11)
testCam(12)
testCam(13)
testCam(14)
testCam(15)
testCam(16)
testCam(17)
testCam(18)
