import time
import serial
from .Function_Library import libARDUINO

class ArduinoController(libARDUINO):
    def __init__(self, port, baud_rate):
        super().__init__()
        self.ser = self.init(port, baud_rate)  # 시리얼 포트 초기화

    def send_command(self, command):
        try:
            self.ser.write(command.encode())  # 명령어 전송
            time.sleep(0.1)  # 잠시 대기
            response = self.ser.readline().decode()  # 응답 읽기
            return response.strip()
        except serial.SerialException as e:
            raise RuntimeError(f"Command Failed: {e}")

    def set_motor_speed(self, motor_id, speed):
        command = f'MOTOR{motor_id} SPEED {speed}\n'  # 모터 속도 설정 명령어
        response = self.send_command(command)
        print(f'Set speed response for MOTOR{motor_id}: {response}')

    def stop_motor(self, motor_id):
        command = f'MOTOR{motor_id} STOP\n'  # 모터 정지 명령어
        response = self.send_command(command)
        print(f'Stop response for MOTOR{motor_id}: {response}')

# 예제 실행 코드
if __name__ == "__main__":
    port = 'COM3'  # 실제 포트 번호로 변경
    baud_rate = 9600  # 보드레이트 설정
    controller = ArduinoController(port, baud_rate)
    try:
        # 앞 모터 속도 설정
        controller.set_motor_speed(1, 100)
        # 뒤 왼쪽 모터 속도 설정
        controller.set_motor_speed(2, 100)
        # 뒤 오른쪽 모터 속도 설정
        controller.set_motor_speed(3, 100)
        
        time.sleep(5)  # 5초 동안 대기
        
        # 모든 모터 정지
        controller.stop_motor(1)
        controller.stop_motor(2)
        controller.stop_motor(3)
    except RuntimeError as e:
        print(f'Error: {e}')
    finally:
        del controller  # 객체 삭제 (시리얼 포트 닫기 포함)
