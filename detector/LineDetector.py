import cv2
import numpy as np

DEFAULT_CONF = {
    "epoch": 5000,
    "thickness": 2,  # Increased thickness for better visibility
    "lineColor": (0, 255, 0),
    "angularResolution": 1,
    "resolution": 1,
    "threshold": 50,  # Lowered threshold for more sensitivity
    "minLineLength": 20,  # Lowered for detecting shorter lines
    "maxLineGap": 10,  # Reduced to detect more continuous lines
    "imgsize": (640, 480)  # Adjusted for typical webcam resolution
}

class LineDetector:
    def __init__(self, camIndex, config=DEFAULT_CONF):
        self.env = cv2.VideoCapture(camIndex, cv2.CAP_DSHOW)
        self.epoch = config["epoch"]
        self.thickness = config["thickness"]
        self.lineColor = config["lineColor"]
        self.angularReso = (np.pi/180)*config["angularResolution"]
        self.reso = config["resolution"]
        self.threshold = config["threshold"]
        self.minLineLength = config["minLineLength"]
        self.maxLineGap = config["maxLineGap"]
        self.imgsize = config["imgsize"]
        print("video connected")
        
    def getFrame(self):
        if not self.env.isOpened():
            raise RuntimeError("Error: Can't open camera")
           
        ret, frame = self.env.read()

        if not ret:
            raise RuntimeError("Error: Can't read frame")
        
        return frame            

    def detect_white_lanes(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Define range for white color in HSV
        lower_white = np.array([0, 0, 190], dtype=np.uint8)
        upper_white = np.array([180, 40, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        
        roi = self.region_of_interest(mask)
        
        lines = cv2.HoughLinesP(
            roi,
            self.reso,
            self.angularReso,
            self.threshold,
            minLineLength=self.minLineLength,
            maxLineGap=self.maxLineGap
        )

        return lines, mask
    
    def plot(self, img, lines):
        if lines is None:
            return img
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), self.lineColor, self.thickness)
        
        return img

    def region_of_interest(self, img):
        height, width = img.shape
        mask = np.zeros_like(img)
        # Define the region of interest based on the image provided
        polygon = np.array([[
            (0, height),
            (width, height),
            (width * 3//4, height * 2//3),
            (width // 4, height * 2//3),
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def filter_lines(self, lines, img):
        left_lines = []
        right_lines = []
        if lines is None:
            return []

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:  # Filter out vertical lines to avoid dividing by zero
                    continue
                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) < 0.5:  # Filter out near-horizontal lines
                    continue
                if slope < 0:
                    left_lines.append(line)
                else:
                    right_lines.append(line)
        return left_lines + right_lines

    def __call__(self):
        while True:
            img = self.getFrame()
            lines, mask = self.detect_white_lanes(img)
            lines = self.filter_lines(lines, img)
            img = self.plot(img, lines)
            cv2.imshow('processed frame', img)
            cv2.imshow('mask', mask)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def __del__(self):
        self.env.release()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    line_detector = LineDetector(camIndex=0)
    line_detector()
