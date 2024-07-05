from ArduinoController import ArduinoController
from LineDetector import LineDetector

import cv2

PORT = "COM6"
BR = 115200
CAMINDEX = 0

def main():
    controller = ArduinoController(PORT, BR)

    detector = LineDetector(CAMINDEX)
    
    detector()

    # cv2.waitKey(0)
    
if __name__ == "main":
    main()