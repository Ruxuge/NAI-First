from datetime import datetime

import cv2
import numpy as np
from imutils.perspective import order_points


def transform(image, pts):

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

pink_lower = np.array([136, 90, 111], np.uint8)
pink_upper = np.array([180, 255, 255], np.uint8)

video = cv2.VideoCapture(0)

while True:

    ret, frame = video.read()

    frame = cv2.resize(frame, (680, 400))
    outline = frame

    ratio = frame.shape[0] / 500.0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    scr = None

    for c in contours:
        area = cv2.contourArea(c)

        if area > 800:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                scr = approx
                x, y, w, h = cv2.boundingRect(c)
                break
            else:
                continue

    if scr is not None:
        cv2.drawContours(outline, [scr], -1, (0, 0, 255), 5)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    pink = cv2.inRange(hsv, pink_lower, pink_upper)
    pink = cv2.erode(pink, None, iterations=2)
    pink = cv2.dilate(pink, None, iterations=2)

    contours, hierarchy = cv2.findContours(pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    a = None

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 300:
            p = cv2.arcLength(contour, True)
            a = cv2.approxPolyDP(contour, 0.02 * p, True)

    if scr is not None and a is not None:
        cv2.drawContours(outline, [a], -1, (0, 0, 255), 5)
        img_name = "scrshot_{}.png".format(datetime.today().strftime('%Y%m%d%H%M%S'))
        warped = transform(frame, scr.reshape(4, 2) * ratio)
        cv2.imwrite(img_name, warped)

    cv2.imshow("ContourSeeker", edged)
    cv2.imshow("Outline", outline)
    cv2.imshow("RealView", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()