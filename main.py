from detector.CenterLine import Centerline
from controller import ArduinoController
from CalControl.SelfDrivingCar import SelfDrivingCar
from detector.LineDetector import DEFAULT_CONF
import cv2

# from ArduinoController import ArduinoController


PORT = "COM14"
BR = 115200
CAMINDEX = 1
COEF ={
    'kp': 0.1,
    'ki': 0.1,
    'kd': 0.1,
    'speed': 30
}

def main():
    arduino = ArduinoController(PORT, BR)
    car = SelfDrivingCar(**COEF)
    while True:
        line = Centerline(CAMINDEX)() # path를 찾아줌
        angle , velocity = car.output(line, DEFAULT_CONF['imgsize'])
        # 앞 모터 속도 설정
        arduino.set_motor_speed(1, angle)
        # 뒤 왼쪽 모터 속도 설정
        arduino.set_motor_speed(2, velocity)
        # 뒤 오른쪽 모터 속도 설정
        arduino.set_motor_speed(3, velocity)
        # Your code here
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()