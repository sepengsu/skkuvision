from .LineDetector import LineDetector
import cv2
import numpy as np
import keyboard

class Centerline:
    def __init__(self, camIndex):
        self.camIndex = camIndex
        self.line_detector = LineDetector(camIndex)
        self.line = self.line_detector()
        self.centerline = self.getCenterline()
    
    def __call__(self):
        self.line = self.line_detector()
        self.centerline = self.getCenterline()
        return self.centerline
    
    def getCenterline(self):
        if self.line is None:
            return None
        left = []
        right = []
        for line in self.line:
            for x1, y1, x2, y2 in line[0]:
                if x1 == x2:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                if slope < 0:
                    left.append(line)
                else:
                    right.append(line)
        left = self.getAverageLine(left)
        right = self.getAverageLine(right)
        return self.getCenterlineFromLines(left, right)
    
    def getAverageLine(self, lines):
        if len(lines) == 0:
            return None
        x1 = int(np.mean([line[0][0] for line in lines]))
        y1 = int(np.mean([line[0][1] for line in lines]))
        x2 = int(np.mean([line[0][2] for line in lines]))
        y2 = int(np.mean([line[0][3] for line in lines]))
        return (x1, y1, x2, y2)
    
    def getCenterlineFromLines(self, left, right):
        if left is None or right is None:
            return None
        x1, y1, x2, y2 = left
        x3, y3, x4, y4 = right
        cx1 = (x1 + x3) // 2
        cy1 = (y1 + y3) // 2
        cx2 = (x2 + x4) // 2
        cy2 = (y2 + y4) // 2
        return (cx1, cy1, cx2, cy2)

# 사용 예시
if __name__ == "__main__":
    centerline_detector = Centerline(camIndex=0)
    while True:
        centerline = centerline_detector()
        if centerline:
            print("Centerline:", centerline)
        if keyboard.is_pressed('q'):  # 'q' 키를 누르면 루프 종료
            break
