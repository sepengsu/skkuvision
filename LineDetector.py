import cv2
import numpy as np

DEFAULT_CONF = {
    "epoch": 5000,
    "thickness": 1,
    "lineColor": (0, 255, 0),
    "angularResolution": 1,
    "resolution": 1,
    "threshold": 80,
    "maxLength": 30,
    "maxGap": 10,
    "imgsize": (448, 448)
}

class LineDetector:
    def __init__(self, camIndex, config = DEFAULT_CONF):
        self.env = cv2.VideoCapture(camIndex, cv2.CAP_DSHOW)
        self.epoch = config["epoch"]
        self.thickness = config["thickness"]
        self.lineColor = config["lineColor"]
        self.angularReso = (np.pi/180)*config["angularResolution"]
        self.reso = config["resolution"]
        self.threshold = config["threshold"]
        self.maxLength = config["maxLength"]
        self.maxGap = config["maxGap"]
        self.imgsize = config["imgsize"]
        print("video connected")
        
    def getFrame(self):
        if not self.env.isOpened():
            raise RuntimeError("Error: Can't open camera")
           
        ret, frame = self.env.read()

        if not ret:
            raise RuntimeError("Error: Can't read frame")
        
        # frame = cv2.resize(frame, self.imgsize)

        return frame            

    def _detect(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img, 100, 200)
        lines = cv2.HoughLines(edges, self.reso, self.angularReso, self.threshold)
        return lines

    def detect(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(img, 100, 200)

        lines = cv2.HoughLinesP(
            edges,
            self.reso,
            self.angularReso,
            self.threshold,
            self.maxLength,
            self.maxGap
        )

        return lines
    
    def _plot(self, img, lines):
        if lines is None:
            return img
        
        for line in lines:
            rho, deg = line[0]
            cos, sin = np.cos(deg), np.sin(deg)
            cx, cy = rho*cos, rho*sin
            x1, y1 = int(cx - 1000*sin), int(cy + 1000*cos)
            x2, y2 = int(cx + 1000*sin), int(cy - 1000*cos)
            cv2.line(img, (x1, y1), (x2, y2), self.lineColor, self.thickness)        
        return img

    def plot(self, img, lines):
        if lines is None:
            return img
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), self.lineColor, self.thickness)
        
        return img

    def __call__(self):
        for iter in range(self.epoch):
            img = self.getFrame()
            lines = self._detect(img)
            img = self._plot(img, lines)
            cv2.imshow('processed frame', img)
            cv2.waitKey(0)

    def __del__(self):
        self.env.release()
        cv2.destroyAllWindows()