import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector


width,height =1280, 720
folderpath='presentation'

cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

pathImages = sorted(os.listdir(folderpath),key=len)
print(pathImages)

#variables
imgNumber=0
hs,ws =int(120 * 1), int(213 * 1)
gestureThreshold=300
buttonpress=False
counter=0
buttonDelay=25
annotations =[[]]
annotationsnumber=-1
annotationstart =False

detector=HandDetector(detectionCon=0.7 ,maxHands=1)


while True:
     success,img =cap.read()
     img=cv2.flip(img,1)   #1 mean horizontal flip
     pathFullImage =os.path.join(folderpath,pathImages[imgNumber])
     imgCurrent =cv2.imread(pathFullImage)


     hands, img=detector.findHands(img)
     cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)   #green line

     if hands and buttonpress is False:
          hand=hands[0]
          fingers= detector.fingersUp(hand)  #checking no. of fingers are up
          cx,cy=hand['center']
          lmList =hand['lmList']       #landmark list


          xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))    #8 is index finger here
          yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
          indexFinger = xVal, yVal
          #print(fingers)



          if cy<=gestureThreshold: #if hand is at the height of the face
               if fingers ==[1,0,0,0,0]:
                    print('left')
                    if imgNumber>0:                #here error if you dont write this line because index goes out of bound
                         buttonpress = True    #keep track of button press
                         annotations = [[]]
                         annotationsnumber = -1
                         annotationstart = False
                         imgNumber-=1

               if fingers ==[0,0,0,0,1]:
                    print('Right')
                    if imgNumber<len(pathImages)-1:
                         buttonpress = True
                         annotations = [[]]
                         annotationsnumber = -1
                         annotationstart = False
                         imgNumber+=1

          #pointer    #out of the above loop because it should not limit to the green line
          if fingers==[0,1,1,0,0]:
               cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)

          #draw
          if fingers == [0, 1, 0, 0, 0]:
               if annotationstart is False:
                    annotationstart=True
                    annotationsnumber+=1
                    annotations.append([])
               cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
               annotations[annotationsnumber].append(indexFinger)
          else:
               annotationstart =False

          # erase
          if fingers == [0, 1, 1, 1, 0]:
               if annotations:
                    annotations.pop(-1)
                    annotationsnumber -= 1
                    buttonpress = True

     if buttonpress:   #button press iteration
          counter +=1
          if counter> buttonDelay:
              counter=0
              buttonpress=False



     for i in range(len(annotations)):
          for j in range(len(annotations[i])):
               if j !=0:
                    cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)


     imgSmall=cv2.resize(img,(ws,hs))
     h,w,_ =imgCurrent.shape
     imgCurrent[0:hs,w-ws:w]=imgSmall
     cv2.imshow("Image",img)
     cv2.imshow("slides",imgCurrent)
     key =cv2.waitKey(1)
     if key == ord('q'):
         break