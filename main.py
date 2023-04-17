#INITIAL SETUP
#----------------------------------------------------------------
import cv2 as cv
import os
from cvzone.HandTrackingModule import HandDetector
from cvzone import overlayPNG
import numpy as np
import math
import time

intro = cv.imread('imgs/0.jpg')
kill = cv.imread('imgs/1.png')
winner = cv.imread('imgs/2.png')
cam = cv.VideoCapture(1) #read the camera
cam.set(3, 1920)
cam.set(4, 1080)
#sets the minimum confidence threshold for the detection
detector = HandDetector(maxHands=1,detectionCon=0.77)

#INITIALIZING GAME COMPONENTS
#----------------------------------------------------------------
sqr = cv.imread('imgs/sqr.png')
ox, oy = 375, 100
tipIds = [4,8,12,16,20]
 
#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED
cv.imshow('Squid Game',cv.resize(intro,(0,0),fx=0.69,fy=0.69))
cv.waitKey(1)
while True:
    cv.imshow('Squid Game',cv.resize(intro,(0,0),fx=0.69,fy=0.69))
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

#GAME LOGIC UPTO THE TEAMS
#-----------------------------------------------------------------------------------------
gameOver = False
NotWon = True
while not gameOver:
    ret,img = cam.read()
    img = cv.resize(img,(1920,1080))
    img = cv.flip(img, 1)
    img = cv.addWeighted(sqr,0.5,img,0.5,0)
    hands,img = detector.findHands(img)
    img_c = img.copy()
    
    cv.line(img, (851,426), (851,652), (26,67,102), thickness=22)
    cv.line(img, (851,426), (1077,426), (26,67,102), thickness=22)
    cv.line(img, (1077,426), (1077,652), (26,67,102), thickness=22)
    cv.line(img, (851,652), (1077,652), (26,67,102), thickness=22)
    
    #Starting point
    cv.circle(img, (851,426),15,(255,0,0),-1)
    
    
    if hands:
        fingers = []
        lmList = hands[0]['lmList']
        cursor = lmList[8]
            
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        if fingers[1] and fingers[2] == False:
            cv.circle(img, (cursor[0],cursor[1]),15,(255,0,255),cv.FILLED)
        
        if (851>cursor[0]>873 or 1055>cursor[0]>1077) and (426>cursor[1]>404 or 630>cursor[1]>652):
            print("Inside")
            
            
    cv.imshow('Squid Game', cv.resize(img,(0,0),fx=0.69,fy=0.69))
    if cv.waitKey(10) & 0xFF == ord('q'):
            break
    

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
