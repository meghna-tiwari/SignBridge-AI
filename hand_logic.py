import cv2
import numpy as np
import joblib
from cvzone.HandTrackingModule import HandDetector

# ----------------------------------
# HAND DETECTOR
# ----------------------------------

detector = HandDetector(
    maxHands=2,
    detectionCon=0.3
)

# ----------------------------------
# LOAD MODEL
# ----------------------------------

model = joblib.load("sign_model.pkl")

print("\nLoaded Classes:")
print(model.classes_)
print()

# ----------------------------------
# PROCESS FRAME
# ----------------------------------

def process_frame(img):

    imgOutput = img.copy()

    detected_char = ""
    conf = 0.0

    hands, img = detector.findHands(
        img,
        draw=False
    )

    if hands:

        features = []

        # ----------------------------------
        # SAME FEATURE EXTRACTION AS TRAINING
        # ----------------------------------

        for hand in hands:

            lmList = hand["lmList"]

            wrist_x = lmList[0][0]
            wrist_y = lmList[0][1]
            wrist_z = lmList[0][2]

            for lm in lmList:

                features.extend([
                    lm[0] - wrist_x,
                    lm[1] - wrist_y,
                    lm[2] - wrist_z
                ])

        # ----------------------------------
        # PAD TO 126 FEATURES
        # ----------------------------------

        while len(features) < 126:
            features.append(0)

        # ----------------------------------
        # PREDICT
        # ----------------------------------

        probabilities = model.predict_proba([features])[0]

        index = np.argmax(probabilities)

        conf = float(probabilities[index])

        detected_char = model.classes_[index]

        print(
            "Prediction:",
            detected_char,
            "| Confidence:",
            round(conf, 3)
        )

        # ----------------------------------
        # CONFIDENCE FILTER
        # ----------------------------------

        if conf < 0.20:
            detected_char = "Nothing"

        # ----------------------------------
        # BOUNDING BOX
        # ----------------------------------

        if len(hands) == 1:

            x, y, w, h = hands[0]["bbox"]

        else:

            h1 = hands[0]["bbox"]
            h2 = hands[1]["bbox"]

            x1 = min(h1[0], h2[0])
            y1 = min(h1[1], h2[1])

            x2 = max(
                h1[0] + h1[2],
                h2[0] + h2[2]
            )

            y2 = max(
                h1[1] + h1[3],
                h2[1] + h2[3]
            )

            x = x1
            y = y1
            w = x2 - x1
            h = y2 - y1

        offset = 20

        if detected_char != "Nothing":

            cv2.rectangle(
                imgOutput,
                (x - offset, y - offset),
                (x + w + offset, y + h + offset),
                (0, 255, 204),
                2
            )

            cv2.putText(
                imgOutput,
                f"{detected_char} ({conf:.2f})",
                (x, y - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    return imgOutput, detected_char, conf