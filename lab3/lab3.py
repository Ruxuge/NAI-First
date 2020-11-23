import numpy as np 
import cv2 

webcam = cv2.VideoCapture(0) 
  
while(1): 
      
    firstBiggest = 0
    secondBiggest = 0
    firstContour = None
    secondContour = None

    _, imageFrame = webcam.read() 

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

    kernal = np.ones((5, 5), "uint8") 

    red_mask = cv2.dilate(red_mask, kernal, iterations=2) 
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask) 
   
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 

        if area > 800:
            if area > firstBiggest:
                firstBiggest = area
                firstContour = contour

            elif firstBiggest > area > secondBiggest:
                secondBiggest = area
                secondContour = contour

    x, y, w, h = cv2.boundingRect(firstContour)
    imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (255, 0, 0), 2) 
    cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

    x1, y1, w1, h1 = cv2.boundingRect(secondContour)
    imageFrame1 = cv2.rectangle(imageFrame, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2) 
    cv2.putText(imageFrame1, "Red Colour", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

                
    cv2.line(imageFrame, (x + int(w / 2), y + int(h / 2)), (x1 + int(w1 / 2), y1 + int(h1 / 2)), (255, 255, 255), thickness=3, lineType=5)
 
    cv2.imshow("Color Detection", imageFrame) 

    if cv2.waitKey(27) & 0xFF == ord('q'): 
        cap.release()
        cv2.destroyAllWindows() 
        break
