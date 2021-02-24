import cv2
import numpy as np
import serial

video = cv2.VideoCapture(0)
port = serial.Serial('COM3',9600)

while True:
    (grabbed, frame) = video.read()
    if not grabbed :
        break

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)


    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)

    cv2.imshow("Live Cam", frame)
    cv2.imshow("Fire Detection", output)

    if int(no_red) > 800:
        port.write(str.encode('A'))
        print('Fire Detected')
    if int(no_red) < 800:
        print(' ')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
