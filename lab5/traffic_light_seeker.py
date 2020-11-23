import cv2

traffic_light_cascade = cv2.CascadeClassifier('traffic_light.xml')


cap = cv2.VideoCapture(0)

numLights = 0

while True:
    ret, frame = cap.read()

    numActualLights = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray, gray)
    traffic_light_seeker = traffic_light_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(15, 15), flags=cv2.CASCADE_SCALE_IMAGE )

    for (x, y, w, h) in traffic_light_seeker:
        numActualLights += 1
        numLights += 1
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)


    cv2.putText(frame, "Lights: {}".format(numLights), (10, 15), cv2.FONT_ITALIC, 0.7, (0, 0, 0))

    cv2.putText(frame, "ActualLights: {}".format(numActualLights), (10, 50), cv2.FONT_ITALIC, 0.7, (0, 0, 0))

    cv2.imshow("LightsSeeker", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
