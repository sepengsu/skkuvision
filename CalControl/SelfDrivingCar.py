from .PID import PIDController
import numpy as np

class SelfDrivingCar:
    def __init__(self, Kp, Ki, Kd, speed=30):
        self.pid_controller = PIDController(Kp, Ki, Kd)
        self.speed = speed  # 기본 속도 설정

    def compute_steering_angle(self, central_line, imgshape):
        height, widh = imgshape
        central_x1, central_y1, central_x2, central_y2 = central_line

        # 중앙선의 각도 계산
        delta_x = central_x2 - central_x1
        delta_y = central_y2 - central_y1
        angle_to_vertical = np.arctan2(delta_y, delta_x) * 180 / np.pi

        # 차량의 중심에서 중앙선의 각도 차이 계산
        steering_angle = self.pid_controller.compute(90, angle_to_vertical)
        return steering_angle

    def compute_speed(self, steering_angle):
        # 간단한 로직: 조향 각도가 클수록 속도를 줄임
        max_speed = 30
        min_speed = 10
        speed = max_speed - (abs(steering_angle) / 10)
        speed = max(min_speed, min(speed, max_speed))
        return speed
    
    def output(self, central_line, img):
        steering_angle = self.compute_steering_angle(central_line, img)
        speed = self.compute_speed(steering_angle)
        return steering_angle, speed