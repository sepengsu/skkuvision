# from ArduinoController import ArduinoController
from detector.LineDetector import LineDetector

import cv2

PORT = "COM14"
BR = 115200
CAMINDEX = 1

def main():
    # controller = ArduinoController(PORT, BR)

    detector = LineDetector(CAMINDEX)
    
    detector()

    
if __name__ == "__main__":
    main()