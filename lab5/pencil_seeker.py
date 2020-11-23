import cv2

pencil_cascade = cv2.CascadeClassifier('cascade_pencil.xml')


cap = cv2.VideoCapture(0)

numPencils = 0

while True:
    ret, frame = cap.read()

    numActualPencils = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray, gray)
    pencil_seeker = pencil_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(15, 15), flags=cv2.CASCADE_SCALE_IMAGE )

    for (x, y, w, h) in pencil_seeker:
        numActualPencils += 1
        numPencils += 1
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)


    cv2.putText(frame, "Pencils {}".format(numPencils), (10, 15), cv2.FONT_ITALIC, 0.7, (0, 0, 0))

    cv2.putText(frame, "ActualPencils: {}".format(numActualPencils), (10, 50), cv2.FONT_ITALIC, 0.7, (0, 0, 0))

    cv2.imshow("PencilsSeeker", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
