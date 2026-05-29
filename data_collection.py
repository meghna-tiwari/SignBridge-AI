import cv2
import HandTrackingModule as htm
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)

offset = 20
imgSize = 300

folder = "Data/C"
counter=0

while True :
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h= hand['bbox']

        imgWhite =np.ones((imgSize, imgSize, 3), np.uint8)*255 
        imgCrop = img[max(0,y-offset) : min(img.shape[0],y + h + offset) , max(0, x - offset) : min(img.shape[1],x + w + offset) ]
        imgCropShape = imgCrop.shape
        
        if imgCrop.size == 0:
            continue

        aspectRatio = h/w

        if aspectRatio >1:
            k = imgSize/h
            wCal = math.ceil(k*w)  
            imgResize  = cv2.resize(imgCrop, (wCal, imgSize))
            imageResizeShape = imgResize.shape
            wGap= math.ceil((300-wCal)/2)
            imgWhite[:,wGap: imageResizeShape[1]+wGap ] = imgResize

        else :
            k = imgSize/w
            hCal = math.ceil(k*h)  
            imgResize  = cv2.resize(imgCrop, (imgSize, hCal))
            imageResizeShape = imgResize.shape
            hGap= math.ceil((300-hCal)/2)
            imgWhite[hGap: hCal+hGap,: ] = imgResize



        
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)
