# this is just an example for how to use an IP camera

import cv2
import time
import numpy as np

capture = cv2.VideoCapture('http://192.168.68.118:4747/video')

while(True):
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(5)

capture.release()
cv2.destroyAllWindows()