import cv2
import HandTrackingModule as htm
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
from speech_handler import voice 


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
classifier=Classifier("Model/Keras_model.h5","Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/C"
counter=0

labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

last_text = ""

while True :
    success, img = cap.read()
    imgOutput = img.copy()
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
            

        prediction, index =classifier.getPrediction(imgWhite, draw=False)
        current_char = labels[index]

        if current_char != last_text:
                voice.speak_now(current_char)
                last_text = current_char
        
        # cv2.rectangle(imgOutput,(x-offset+50,y-offset+50), (x+w+offset,y+h+offset), (255,0,0), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x,y-20), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 2)
        cv2.rectangle(imgOutput,(x-offset,y-offset), (x+w+offset,y+h+offset), (255,0,255), 4)
        
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)
    
