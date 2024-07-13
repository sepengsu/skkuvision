from detector.LineDetector import LineDetector
from CalControl.SelfDrivingCar import SelfDrivingCar
from detector.LineDetector import DEFAULT_CONF
import cv2
from controller.ArduinoController import ArduinoController
import numpy as np
import keyboard

PORT = "COM14"
BR = 115200
CAMINDEX = 1
COEF ={
    'Kp': 0.1,
    'Ki': 0.1,
    'Kd': 0.1,
    'speed': 30
}

def main():
    arduino = ArduinoController(PORT, BR)
    print("Arduino connected")
    car = SelfDrivingCar(**COEF)
    line_detector = LineDetector(CAMINDEX)
    while True:
        img, lines, centerline, mask = line_detector()
        # 마스크가 gray scale이면 BGR로 변환
        if len(mask.shape) == 2:
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # 감지된 선이 없으면 다음 프레임으로 넘어감
        if centerline is not None:
            angle, velocity = car.output(centerline, DEFAULT_CONF['imgsize'])
        # 앞 모터 속도 설 정
        angle, velocity = 0, 30#임시
        print("arz")
        arduino.set_motor_speed(1, angle)
        # 뒤 왼쪽 모터 속도 설정
        arduino.set_motor_speed(2, velocity)
        # 뒤 오른쪽 모터 속도 설정
        arduino.set_motor_speed(3, velocity)
        
        # 감지된 선과 중앙선을 이미지에 그리기
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        if centerline is not None:
            x1, y1, x2, y2 = centerline
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        combined = np.hstack((img, mask))
        cv2.imshow('processed frame', combined)
        print(f"angle: {angle}, velocity: {velocity}")
        if cv2.waitKey(1) & keyboard.is_pressed('q'):
            break

    cv2.destroyAllWindows()
    line_detector.__del__()

if __name__ == "__main__":
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
    #     cv2.destroyAllWindows()
    main()
