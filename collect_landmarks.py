import cv2
import pandas as pd
import time
from cvzone.HandTrackingModule import HandDetector

# -----------------------------------
# CONFIG
# -----------------------------------

cap = cv2.VideoCapture(0)

detector = HandDetector(
    maxHands=2,
    detectionCon=0.5
)

label = input("Enter Label Name: ")

SAVE_INTERVAL = 0.2      # 5 samples/sec

autoMode = False
last_save = time.time()

dataset = []

print("\nControls:")
print("a -> Toggle Auto Save")
print("q -> Quit & Save Dataset\n")

# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:

    success, img = cap.read()

    if not success:
        break

    hands, img = detector.findHands(img)

    if hands:

        features = []

        for hand in hands:

            lmList = hand["lmList"]

            # Wrist landmark
            wrist_x = lmList[0][0]
            wrist_y = lmList[0][1]
            wrist_z = lmList[0][2]

            # Relative coordinates
            for lm in lmList:

                features.extend([
                    lm[0] - wrist_x,
                    lm[1] - wrist_y,
                    lm[2] - wrist_z
                ])

        # Pad if only one hand is detected
        while len(features) < 126:
            features.append(0)

        # --------------------------
        # AUTO SAVE
        # --------------------------

        if autoMode and (time.time() - last_save > SAVE_INTERVAL):

            dataset.append([label] + features)

            last_save = time.time()

            print(f"Saved: {len(dataset)}")

    # --------------------------
    # DISPLAY INFO
    # --------------------------

    cv2.putText(
        img,
        f"Label: {label}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        f"Samples: {len(dataset)}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"Auto Save: {autoMode}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.imshow("Landmark Collection", img)

    key = cv2.waitKey(1) & 0xFF

    # Toggle Auto Save
    if key == ord("a"):

        autoMode = not autoMode

        print(f"\nAuto Save = {autoMode}\n")

    # Quit
    elif key == ord("q"):
        break

# -----------------------------------
# SAVE CSV
# -----------------------------------

columns = ["label"]

for i in range(126):
    columns.append(f"f{i}")

df = pd.DataFrame(
    dataset,
    columns=columns
)

try:

    old_df = pd.read_csv(
        "hand_landmarks.csv"
    )

    df = pd.concat(
        [old_df, df],
        
        ignore_index=True
    )

except:
    pass

df.to_csv(
    "hand_landmarks.csv",
    index=False
)

print("\n--------------------------------")
print(f"Saved {len(dataset)} samples")
print("Written to hand_landmarks.csv")
print("--------------------------------")

cap.release()
cv2.destroyAllWindows()