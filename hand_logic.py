import cv2
import numpy as np
import joblib
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(
    maxHands=2,
    detectionCon=0.3
)

model = joblib.load("sign_model.pkl")

print("\nLoaded Classes:")
print(model.classes_)
print()

EXPECTED_FEATURES = 126


LABEL_MAP = {
    # "ModelClass" : "Action"
    "del"         : "DEL",       #  backspace gesture
    "speak"       : "SPEAK",     #  speak sentence gesture
    "nothing"     : "Nothing",   #  no hand / unknown
    
    
}


def process_frame(img):

    imgOutput = img.copy()

    detected_char = ""
    conf = 0.0

    hands, img = detector.findHands(
        img,
        draw=False
    )

    if hands:

        hands = hands[:2]

        features = []

        for hand in hands:

            lmList = hand["lmList"]

            if len(lmList) < 21:
                continue

            wrist_x = lmList[0][0]
            wrist_y = lmList[0][1]
            wrist_z = lmList[0][2]

            for lm in lmList[:21]:

                features.extend([
                    lm[0] - wrist_x,
                    lm[1] - wrist_y,
                    lm[2] - wrist_z
                ])

        if len(features) > EXPECTED_FEATURES:
            features = features[:EXPECTED_FEATURES]

        while len(features) < EXPECTED_FEATURES:
            features.append(0)

        if len(features) != EXPECTED_FEATURES:
            return imgOutput, "", 0.0

       

        try:

            probabilities = model.predict_proba(
                [features]
            )[0]

            index = np.argmax(probabilities)

            conf = float(probabilities[index])

            raw_label = model.classes_[index]

           

            detected_char = LABEL_MAP.get(
                raw_label.lower(),  # lowercase match
                raw_label           # if not in map, use as-is
            )

            print(
                f"Raw: {raw_label} → Mapped: {detected_char} | Confidence: {conf:.3f}"
            )

        except Exception as e:

            print("Prediction Error:", e)
            return imgOutput, "", 0.0

        

        if conf < 0.20:
            detected_char = "Nothing"

        

        if len(hands) == 1:
            x, y, w, h = hands[0]["bbox"]

        else:

            h1 = hands[0]["bbox"]
            h2 = hands[1]["bbox"]

            x1 = min(h1[0], h2[0])
            y1 = min(h1[1], h2[1])
            x2 = max(h1[0] + h1[2], h2[0] + h2[2])
            y2 = max(h1[1] + h1[3], h2[1] + h2[3])

            x, y = x1, y1
            w, h = x2 - x1, y2 - y1

        offset = 20

        if detected_char not in ["Nothing", "DEL", "SPEAK"]:

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

        
        elif detected_char in ["DEL", "SPEAK"]:

            color = (0, 100, 255) if detected_char == "DEL" else (255, 200, 0)

            cv2.rectangle(
                imgOutput,
                (x - offset, y - offset),
                (x + w + offset, y + h + offset),
                color,
                2
            )

            cv2.putText(
                imgOutput,
                f"[ {detected_char} ]",
                (x, y - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                color,
                2
            )

    return imgOutput, detected_char, conf
