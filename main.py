import os
import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector

folderPath = "presentation"
width,height = 1250,500
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# Get List of presentation images
imgNumber = 0
pathImages = sorted(os.listdir(folderPath),key=len)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 20
annotations = [[]]
annotationNumber = -1
annotationStart = False
print(pathImages)

hs, ws = 120, 213

# Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=2)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    # Import Images
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    imgCurrent = cv2.resize(imgCurrent,(900,500))

    hands,img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        # annotationStart = False
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList']
        # Constrain Values for easier drawing
        xVal = int(np.interp(lmList[8][0],[width//2,width],[0,width]))
        yVal = int(np.interp(lmList[8][1],[150,height-150],[0,height]))
        indexFinger = xVal, yVal #lmList[8][0], lmList[8][1]

        if cy <= gestureThreshold:
            # Gesture 1 >> Left
            if fingers == [1,0,0,0,0]:

                print("left")

                if imgNumber >0:
                    buttonPressed = True
                    imgNumber -=1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

            # Gesture 2 >> Right
            if fingers == [0,0,0,0,1]:


                print("Right")

                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        # Gesture 3 >> Pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)


        # Gesture 4 >> Draw
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber+=1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

    #     Gesture 5 ==> Erase
        if fingers==[0,1,1,1,0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber-=1
                buttonPressed = True



    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)

        # buttonPressed = False
    # Adding Webcam image on the slide
    imgSmall = cv2.resize(img, (ws,hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall
    cv2.imshow("image",img)
    cv2.imshow("Slides", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break