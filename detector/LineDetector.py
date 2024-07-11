import cv2
import numpy as np

# 기본 설정 값
DEFAULT_CONF = {
    "epoch": 5000,
    "thickness": 2,  # 더 잘 보이도록 선 두께 증가
    "lineColor": (0, 255, 0),
    "angularResolution": 1,
    "resolution": 1,
    "threshold": 50,  # 민감도를 높이기 위해 임계값을 낮춤
    "minLineLength": 20,  # 더 짧은 선도 감지할 수 있도록 최소 선 길이 낮춤
    "maxLineGap": 10,  # 더 연속적인 선을 감지하기 위해 최대 선 간격 줄임
    "imgsize": (640, 480)  # 일반적인 웹캠 해상도로 조정
}

class LineDetector:
    def __init__(self, camIndex, config=DEFAULT_CONF):
        # 카메라 초기화
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
        print("비디오 연결됨")

    def getFrame(self):
        # 카메라에서 프레임을 가져옴
        if not self.env.isOpened():
            raise RuntimeError("오류: 카메라를 열 수 없음")
        
        ret, frame = self.env.read()

        if not ret:
            raise RuntimeError("오류: 프레임을 읽을 수 없음")
        
        return frame

    def detect_white_lanes(self, img):
        # 이미지를 HSV 색 공간으로 변환
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 흰색 범위를 정의
        lower_white = np.array([0, 0, 190], dtype=np.uint8)
        upper_white = np.array([180, 40, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_white, upper_white)

        # 관심 영역(ROI) 설정
        roi = self.region_of_interest(mask)

        # 허프 변환을 사용하여 선 감지
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
        # 감지된 선을 이미지에 그림
        if lines is None:
            return img

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), self.lineColor, self.thickness)

        return img

    def region_of_interest(self, img):
        # 관심 영역(ROI)을 설정하여 특정 영역만 감지
        height, width = img.shape
        mask = np.zeros_like(img)
        # 다각형 영역을 정의
        polygon = np.array([[
            (0, height),
            (width, height),
            (width * 3 // 4, height * 2 // 3),
            (width // 4, height * 2 // 3),
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def filter_lines(self, lines, img):
        # 왼쪽 선과 오른쪽 선을 분리
        left_lines = []
        right_lines = []
        if lines is None:
            return []

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:  # 수직선을 필터링하여 나누기 오류를 피함
                    continue
                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) < 0.5:  # 수평에 가까운 선을 필터링
                    continue
                if slope < 0:
                    left_lines.append(line)
                else:
                    right_lines.append(line)
        return left_lines + right_lines

    def __call__(self):
        # 프레임을 처리하고 선을 감지하여 반환
        img = self.getFrame()
        lines, mask = self.detect_white_lanes(img)
        lines = self.filter_lines(lines, img)
        img = self.plot(img, lines)
        cv2.imshow('processed frame', img)
        cv2.imshow('mask', mask)
        return 

    def __del__(self):
        # 자원을 해제하고 윈도우를 닫음
        self.env.release()
        cv2.destroyAllWindows()

# 사용 예시
if __name__ == "__main__":
    line_detector = LineDetector(camIndex=0)
    line_detector()
