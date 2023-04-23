#INITIAL SETUP
#----------------------------------------------------------------
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import random

intro = cv.imread('imgs/0.jpg')
kill = cv.imread('imgs/1.png')
winner = cv.imread('imgs/2.png')
cam = cv.VideoCapture(1) #read the camera
cam.set(3, 1920)
cam.set(4, 1080)
#sets the minimum confidence threshold for the detection
detector = HandDetector(maxHands=1,detectionCon=0.8)

#INITIALIZING GAME COMPONENTS
#----------------------------------------------------------------
sqr = cv.imread('imgs/sqr.png')
img_canvas = np.zeros((1080,1920,3),np.uint8)

tipIds = [4,8,12,16,20]
curr_x, curr_y = 0,0
prev_x, prev_y = 0,0
x,y = [],[]
distance_drawn = 0
cut_areas = []

gameOver = False
NotWon = True
toStartGame = False
toStartTime = False

TIMER_MAX=40
TIMER=TIMER_MAX
prev=time.time()
 
#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED
cv.imshow('Squid Game',cv.resize(intro,(0,0),fx=0.69,fy=0.69))
cv.waitKey(1)
while True:
    cv.imshow('Squid Game',cv.resize(intro,(0,0),fx=0.69,fy=0.69))
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

#GAME LOGIC UPTO THE TEAMS
#-----------------------------------------------------------------------------------------

while not gameOver and TIMER>=0:
    
    ret,img = cam.read()
    img = cv.resize(img,(1920,1080))
    img = cv.flip(img, 1)
    img = cv.addWeighted(sqr,0.5,img,0.5,0)
    hands,img = detector.findHands(img)
    
    """ 
    cv.line(img, (851,426), (851,652), (26,67,102), thickness=22)
    cv.line(img, (851,426), (1077,426), (26,67,102), thickness=22)
    cv.line(img, (1077,426), (1077,652), (26,67,102), thickness=22)
    cv.line(img, (851,652), (1077,652), (26,67,102), thickness=22) 
    """
    
    #Starting point
    cv.circle(img, (851,427),13,(255,0,0),-1)
    
    if len(hands) != 0:
        fingers = []
        lmList = hands[0]['lmList']
        cursor = lmList[8] #make the index be the cursor
        curr_x, curr_y = cursor[0], cursor[1]
            
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        if fingers[1] and fingers[2] == False: #check that the ring and pinky are down
            
            starting_pt_dist = math.sqrt((curr_x - 851)**2 +  (curr_y - 426)**2)
        
            if starting_pt_dist < 5: #check we are at starting point to begin
                toStartGame = True
                toStartTime = True
            
            if toStartGame:
                x.append(curr_x)
                y.append (curr_y)
                
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = curr_x, curr_y
                
                cv.line(img,(prev_x,prev_y),(curr_x, curr_y),(255,0,0),20)
                cv.line(img_canvas,(prev_x,prev_y),(curr_x, curr_y),(255,0,0),20)
                
                prev_x,prev_y = curr_x, curr_y
            
                if len(x) > 2 and len(y) > 2:
                    distance_drawn += math.sqrt((curr_x - x[-2])**2 +  (curr_y - y[-2])**2)

                #check if the cursor lies on the lines and also adjust difficulty for game
                if (835<curr_x<885 or 1045<curr_x<1095) or (415<curr_y<465 or 615<curr_y<666):
                    pass
                else:
                    gameOver = True
               
        
            if starting_pt_dist < 5 and distance_drawn > (4*224): #check for win
                toStartGame = False
                NotWon = False
                gameOver = True
                break
        
            if toStartTime: #timer block
                cv.putText(img,str(TIMER),(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,int(255*(TIMER)/TIMER_MAX),int(255*(TIMER_MAX-TIMER)/TIMER)),4,cv.LINE_AA)
                cur=time.time()
                no=random.randint(1,5)
                if cur-prev>=no:
                    prev=cur
                    TIMER=TIMER-no
                
    img = cv.addWeighted(img,0.5,img_canvas,0.5,0)
    cv.imshow('Squid Game', cv.resize(img,(0,0),fx=0.69,fy=0.69))
    if cv.waitKey(10) & 0xFF == ord('q'):
            break
        
else:
    if NotWon:
        while True:
            #show the loss screen incase time runs out
            cv.imshow('Squid Game',cv.resize(kill,(0,0),fx=0.69,fy=0.69))
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
    
cam.release()

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
