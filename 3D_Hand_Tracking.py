import socket
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

"""
Broad-casting data > usable for everyone > unity takes data from this address 
To send data we use the UDP protocol
It doesn't need initial connection > run pycharm all the time and when
run unity project , automatically connects and get the data
DCP > SOCK_STREAM
UDP > SOCK_DGRAM
"""

# Parameters
width , height = 1280 , 720
# Read from webcam
capture = cv.VideoCapture(0)
# proId=3 is width and proId=4 is height
# default : proId=3 is 640 and proId=4 is 480
# Create wider area or region for more hand movements
capture.set(propId=3,value=width)
capture.set(propId=4,value=height)

# Hand detector
hand_detector = HandDetector(maxHands=1,detectionCon=0.8)
# Communication part
# socket.AF_INET > the family
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# give the address
# Instead of 5052 > any number > but not used before
server_address_port = ("127.0.0.1",5052)

while True :
    # Get the frame from the webcam
    ret , frame = capture.read()
    if not ret :
        break
    else :
        # Hands
        hands , frame = hand_detector.findHands(frame)
        # Create an empty data > send data at the end and each time it refreshes(each iteration ) otherwise it will keep adding to previous data(not good)
        # if you declare it outside the while loop > an empty list
        data = []
        # send landmark list(21 landmarks) > each landmark > 3 values > x,y,z
        # landmark values : (x,y,z) > * 21 > total numbers values that we have(63)
        # send all 63 values in a single list > easy to decode in unity script
        if hands :
            # Get the first hand detected
            hand = hands[0]
            # Get the landmark list
            landmark_list = hand['lmList']
            # print(landmark_list)
            for landmark in landmark_list :
                data.extend([landmark[0],height-landmark[1],landmark[2]])
            # print(data)
            # Send data and encode data before sending
            sock.sendto(str.encode(str(data)),server_address_port)
        frame = cv.resize(frame,(0,0),None,0.5,0.5)
        # cv.imshow("Title of our frame",the image we want to display)
        cv.imshow("Screen",frame)
        # cv.waitKey(ms) : delay to close
        key = cv.waitKey(5) & 0xFF
        if key == 27 :
            capture.release()
            break
