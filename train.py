import cv2 as cv
import numpy as np
import math
cap = cv.VideoCapture('C:/Users/kaiyu/PycharmProjects/train/3686.mp4')
cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
cv.resizeWindow("Resized_Window", 1920, 540)
previous = (0,255,0)
n = 0
direction = True
#out = cv.VideoWriter('C:/Users/kaiyu/PycharmProjects/train/detected.mp4', cv.VideoWriter_fourcc('m','p','4','v'), 30, (1920, 1080))
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    length = 1
    img = frame.copy()
    image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([5, 255, 255])
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])

    lower_mask = cv.inRange(image, lower1, upper1)
    upper_mask = cv.inRange(image, lower2, upper2)
    full_mask = lower_mask + upper_mask

    #cv.circle(img, (720, 800), 20, (0, 255, 0), -1)
    #cv.line(img, (1200,0), (1200, 1079), (0,255,0), 10)
    #cv.line(img, (150, 0), (150, 1079), (0, 255, 0), 10)
    crop_img = full_mask[0:1079, 150:1200]
    line1 = cv.HoughLinesP(crop_img, 1, np.pi / 180, threshold=20, minLineLength=100, maxLineGap=50)

    if line1 is not None:
        l = line1[0][0]
        #cv.line(img, (l[0]+150, l[1]), (l[2]+150, l[3]), (0, 255, 0), 10, cv.LINE_AA)
        length = math.sqrt((l[0] - l[3])**2 + (l[1] - l[3])**2)
        if (l[0] + 150 > 720):
            direction = False
        else:
            direction = True
        if n % 4 == 0:
            if(abs(l[0] + 150 - 720) > 1920/2):
                previous = (0, 0, 255)
                cv.circle(img, (1800, 100), 50, previous, -1)
            elif direction:
                if length > 620 and length < 710:
                    previous = (0,255,0)
                    cv.circle(img, (1800, 100), 50, previous, -1)
                else:
                    previous = (0, 255, 255)
                    cv.circle(img, (1800, 100), 50, previous, -1)
            else:
                previous = (0, 255, 0)
                cv.circle(img, (1800, 100), 50, previous, -1)
        else:
            cv.circle(img, (1800, 100), 50, previous, -1)
    else:
        cv.circle(img, (1800, 100), 50, previous, -1)
    n+= 1
    cv.putText(img, "Frame:" + str(n), (100, 150), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv.LINE_AA)
    #out.write(img)
    cv.imshow("Resized_Window", np.hstack([frame, img]))
    if cv.waitKey(15) == ord(' '):
        break

cap.release()
cv.destroyAllWindows()
