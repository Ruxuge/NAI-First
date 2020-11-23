import cv2
import numpy as np


def compare_images(eye1, eye2: np.ndarray, threshold=0.5) -> bool:
    eye1 = cv2.cvtColor(eye1, cv2.COLOR_BGR2GRAY)
    eye2 = cv2.cvtColor(eye2, cv2.COLOR_BGR2GRAY)

    eye1 = cv2.resize(eye1, (50, 50), cv2.INTER_CUBIC)
    eye2 = cv2.resize(eye2, (50, 50), cv2.INTER_CUBIC)

    eye1_old = cv2.calcHist([eye1], [0], None, [256], [0, 256])
    eye2_old = cv2.calcHist([eye2], [0], None, [256], [0, 256])

    similar = cv2.compareHist(eye1_old, eye2_old, cv2.CMP_EQ)
    print(similar)

    return similar > threshold


cascade_src = 'cascade_eye.xml'
eye_cascade = cv2.CascadeClassifier(cascade_src)

cap = cv2.VideoCapture(0)
eyeNum = 0

eyes: list[np.ndarray] = []

while True:
    ret, img = cap.read()

    actualEyeNum = 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(gray, 1.1, 3)

    for (x, y, w, h) in eyes:
        new_eye = img[y:y + h, x:x + w]
        similar_eyes = [i for i in eyes if compare_images(new_eye, i)]
        if not similar_eyes:
            eyes.append(new_eye)
        eyeNum += 1
        actualEyeNum += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.putText(img, "eyes: {}".format(eyeNum), (10, 50), cv2.FONT_ITALIC, 0.7, (0, 0, 0))
    cv2.putText(img, "eyes: {}".format(actualEyeNum), (10, 15), cv2.FONT_ITALIC, 0.7, (0, 0, 0))
    cv2.imshow('EyeSeeker', img)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()



