import cv2

face_cascade = cv2.CascadeClassifier('cascade_face.xml')
eye_cascade = cv2.CascadeClassifier('cascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    numFaces = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceSeeker = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faceSeeker:
        numFaces += 1
        img = cv2.circle(frame, (x + int(w / 2), y + int(h / 2)), int(w / 2), (0, 255, 255), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (x1, y1, w1, h1) in eyes:
            cv2.rectangle(roi_color, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

    cv2.putText(frame, "Faces: {}".format(numFaces), (10, 15), cv2.FONT_ITALIC, 0.7, (0, 0, 0))

    cv2.imshow("FaceSeeker", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
