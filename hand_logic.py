import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

detector = HandDetector(maxHands=1)
classifier = Classifier("Model/Keras_model.h5", "Model/labels.txt")
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "Okay"]

def process_frame(img):
    imgOutput = img.copy()
    hands, img = detector.findHands(img, draw=False) 
    
    offset = 40 
    imgSize = 300
    detected_char = ""

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        
        try:
           
            y1, y2 = max(0, y - offset), min(img.shape[0], y + h + offset)
            x1, x2 = max(0, x - offset), min(img.shape[1], x + w + offset)
            imgCrop = img[y1:y2, x1:x2]

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            detected_char = labels[index]

            
            color = (0, 255, 204) # Neon Cyan
            cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), color, 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset - 45), (x + 50, y - offset), color, cv2.FILLED)
            cv2.putText(imgOutput, detected_char, (x - offset + 10, y - offset - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            
        except Exception:
            pass
            
    return imgOutput, detected_char