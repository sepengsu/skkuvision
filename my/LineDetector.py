import cv2
import numpy as np
from imageprocessor import ImageProcessor  # Ensure this file exists and is correctly imported

DEFAULT_CONF = {
    "epoch": 5000,
    "thickness": 2,
    "lineColor": (0, 255, 0),
    "angularResolution": 1,
    "resolution": 1,
    "threshold": 50,
    "minLineLength": 50,
    "maxLineGap": 20,
    "imgsize": (448, 448)
}

class LineDetector:
    def __init__(self, camIndex, config=DEFAULT_CONF):
        self.env = cv2.VideoCapture(camIndex, cv2.CAP_DSHOW)
        self.epoch = config["epoch"]
        self.thickness = config["thickness"]
        self.lineColor = config["lineColor"]
        self.angularReso = (np.pi / 180) * config["angularResolution"]
        self.reso = config["resolution"]
        self.threshold = config["threshold"]
        self.minLineLength = config["minLineLength"]
        self.maxLineGap = config["maxLineGap"]
        self.imgsize = config["imgsize"]
        self.processor = ImageProcessor(self.imgsize, 30)
        print("video connected")

    def getFrame(self):
        if not self.env.isOpened():
            raise RuntimeError("Error: Can't open camera")
        ret, frame = self.env.read()
        if not ret:
            raise RuntimeError("Error: Can't read frame")
        frame = cv2.resize(frame, self.imgsize)
        return frame

    def detect(self, img):
        return self.processor.process(img)

    def __call__(self):
        for iter in range(self.epoch):
            img = self.getFrame()
            processed_img = self.detect(img)
            cv2.imshow('processed frame', processed_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def __del__(self):
        self.env.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = LineDetector(0)
    detector()