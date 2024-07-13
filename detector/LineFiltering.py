import numpy as np
import cv2
class Centerline:
    def __init__(self, lines: list,width):
        self.lines = lines  # 여러 선을 받아 초기화
        self.width = width
    
    def __call__(self):
        self.centerline = self.getCenterline()
        return self.centerline
    
    def getCenterline(self):
        if len(self.lines) == 0:
            return None
        left = []
        right = []
        for line in self.lines:
            x1, y1, x2, y2 = line[0]  # 각 선의 좌표를 가져옴
            mid_x = (x1 + x2) / 2  # 선의 중간 지점의 x 좌표를 계산

            if mid_x < self.width / 2:
                left.append((x1, y1, x2, y2))
            else:
                right.append((x1, y1, x2, y2))
        
        left_avg = self.getAverageLine(left)
        right_avg = self.getAverageLine(right)
        return self.getCenterlineFromLines(left_avg, right_avg)

    
    def getAverageLine(self, lines):
        if len(lines) == 0:
            return None
        x1 = int(np.mean([line[0] for line in lines]))
        y1 = int(np.mean([line[1] for line in lines]))
        x2 = int(np.mean([line[2] for line in lines]))
        y2 = int(np.mean([line[3] for line in lines]))
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
    example_lines = [
        (100, 200, 150, 250),
        (200, 300, 250, 350),
        (300, 400, 350, 450)
    ]
    
    centerline_detector = Centerline(example_lines)
    while True:
        centerline = centerline_detector()
        if centerline:
            print("Centerline:", centerline)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
            break
