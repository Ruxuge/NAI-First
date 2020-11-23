import cv2

frontcar_cascade = cv2.CascadeClassifier('cascade_frontcar.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    numCarFaces = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frontCarSeeker = frontcar_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in frontCarSeeker:
        numCarFaces += 1
        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        

    cv2.putText(frame, "CarFaces: {}".format(numCarFaces), (10, 15), cv2.FONT_ITALIC, 0.7, (0, 0, 0))

    cv2.imshow("CarFacesSeeker", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
