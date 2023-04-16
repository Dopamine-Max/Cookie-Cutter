#INITIAL SETUP
#----------------------------------------------------------------
import cv2 as cv
import os
from cvzone import HandTrackingModule, overlayPNG
import numpy as np
import time

intro = cv.imread('frames/0.jpg')
kill = cv.imread('frames/1.png')
winner = cv.imread('frames/2.png')
cam = cv.VideoCapture(1) #read the camera
frameHeight=cam.get(cv.CAP_PROP_FRAME_HEIGHT)
frameWidth=cam.get(cv.CAP_PROP_FRAME_WIDTH)
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)
#sets the minimum confidence threshold for the detection

#INITILIZING GAME COMPONENTS
#----------------------------------------------------------------
sqr = cv.imread('frames/sqr.png')
#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED
cv.imshow('squid game',cv.resize(intro,(0,0),fx=0.69,fy=0.69))
cv.waitKey(1)
while True:
    cv.imshow('squid game',cv.resize(intro,(0,0),fx=0.69,fy=0.69))
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

#GAME LOGIC UPTO THE TEAMS
#-----------------------------------------------------------------------------------------
gameOver = False
NotWon = True
while not gameOver:
    ret,frame=cam.read()
    target_image = overlayPNG(frame,sqr,[0,0])
    cv.imshow('target_image', target_image)
    cv.waitKey(1)

#LOSS SCREEN
if NotWon:
    while True:
        #show the loss screen from the kill image read before and end it after we press q
        cv.imshow('Squid Game',cv.resize(kill,(0,0),fx=0.69,fy=0.69))
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

else:
#WIN SCREEN
#show the win screen from the winner image read before
    cv.imshow('Squid Game', cv.resize(winner,(0,0),fx=0.69,fy=0.69))
    cv.waitKey(125)

    while True:
        #show the win screen from the winner image read before and end it after we press q
        cv.imshow('Squid Game', cv.resize(winner,(0,0),fx=0.69,fy=0.69))
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

#destroy all the windows
cv.destroyAllWindows
