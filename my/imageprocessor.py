import numpy as np
import cv2
from line import Line

class ImageProcessor:
    def __init__(self, frameDimensions, frameRate):
        self.frameDimensions = frameDimensions
        self.frameRate = frameRate
        self.w = self.frameDimensions[0]
        self.h = self.frameDimensions[1]

        self.roiY = (0.57, 0.71)
        self.roiX = (0.67, 0.95)

        self.left = Line(self.frameDimensions, (0, 0, 255))
        self.right = Line(self.frameDimensions, (255, 0, 0))

        self.calibrationResolution = (1280, 720)
        kx = self.w / self.calibrationResolution[0]
        ky = self.h / self.calibrationResolution[1]
        cameraMatrix = np.array([
            [1.00612323e+03, 0.00000000e+00, 6.31540281e+02],
            [0.00000000e+00, 1.00551440e+03, 3.48207362e+02],
            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
        ])
        self.cameraMatrix = np.multiply(cameraMatrix, [
            [kx, 1, kx],
            [1, ky, ky],
            [1, 1, 1]
        ])
        self.distortionCoefficients = np.array([[0.18541226, -0.32660915, 0.00088513, -0.00038131, -0.02052374]])
        self.newCameraMatrix, self.roi = cv2.getOptimalNewCameraMatrix(self.cameraMatrix, self.distortionCoefficients, self.frameDimensions, 1, self.frameDimensions)
        self.rectifyMapX, self.rectifyMapY = cv2.initUndistortRectifyMap(self.cameraMatrix, self.distortionCoefficients, None, self.newCameraMatrix, self.frameDimensions, 5)

    def doBlur(self, frame, iterations, kernelSize):
        blured = frame.copy()
        while iterations > 0:
            blured = cv2.GaussianBlur(blured, (kernelSize, kernelSize), sigmaX=0, sigmaY=0)
            iterations -= 1
        return blured

    def doRegionOfInterest(self, frame):
        y0Px = int(self.h * self.roiY[0])
        y1Px = int(self.h * self.roiY[1])
        x0Px = int((1 - self.roiX[0]) * self.w / 2)
        x1Px = int((1 - self.roiX[1]) * self.w / 2)
        vertices = np.array([[
            (x0Px, y0Px),
            (x1Px, y1Px),
            (self.w - x1Px, y1Px),
            (self.w - x0Px, y0Px)
        ]], dtype=np.int32)
        mask = np.zeros_like(frame)
        cv2.fillPoly(mask, vertices, 255)
        return cv2.bitwise_and(frame, mask)

    def findLanes(self, frame, lines, minAngle=10, drawAll=False):
        self.left.clear()
        self.right.clear()
        if isinstance(lines, np.ndarray):
            for line in lines:
                for x1, y1, x2, y2 in line:
                    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                    if np.abs(angle) > minAngle:
                        if angle > 0:
                            self.right.add(x1, y1, x2, y2)
                            if drawAll:
                                cv2.line(frame, (x1, y1), (x2, y2), self.right.color)
                        else:
                            self.left.add(x1, y1, x2, y2)
                            if drawAll:
                                cv2.line(frame, (x1, y1), (x2, y2), self.left.color)
        self.left.fit()
        self.right.fit()
        return frame
        
    def drawPoly(self, frame, poly, color, width=3):
        y0 = int(self.h * self.roiY[0])
        y1 = int(self.h * self.roiY[1])
        if poly:
            x0 = int(poly(y0))
            x1 = int(poly(y1))
            cv2.line(frame, (x0, y0), (x1, y1), color, width)
        else:
            cv2.line(frame, (0, y0), (0, y1), color, width)

    def process(self, frame):
        undistort = cv2.remap(frame, self.rectifyMapX, self.rectifyMapY, cv2.INTER_LINEAR)
        gray = cv2.cvtColor(undistort, cv2.COLOR_BGR2GRAY)
        grayColor = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        blured = self.doBlur(gray, iterations=3, kernelSize=7)
        canny = cv2.Canny(blured, threshold1=20, threshold2=40)
        roi = self.doRegionOfInterest(canny)
        houghLines = cv2.HoughLinesP(
            roi,
            rho=1, 
            theta=np.pi / 180, 
            threshold=20, 
            lines=np.array([]), 
            minLineLength=5, 
            maxLineGap=60
        )
        lanes = self.findLanes(grayColor, houghLines, minAngle=10, drawAll=True)
        # self.drawPoly(lanes, self.left.poly, self.left.color, width=3)
        # self.drawPoly(lanes, self.right.poly, self.right.color, width=3)
        return lanes
