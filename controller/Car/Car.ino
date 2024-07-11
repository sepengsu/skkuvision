#include <Arduino.h>
#include "Car_Library.h"

// 핀 정의
const int leftMotorPin1 = 3; // 왼쪽 뒤바퀴 모터의 IN1 핀
const int leftMotorPin2 = 4; // 왼쪽 뒤바퀴 모터의 IN2 핀
const int rightMotorPin1 = 5; // 오른쪽 뒤바퀴 모터의 IN1 핀
const int rightMotorPin2 = 6; // 오른쪽 뒤바퀴 모터의 IN2 핀
const int handlePin1 = 7; // 핸들 모터의 IN1 핀
const int handlePin2 = 8; // 핸들 모터의 IN2 핀

void setup() {
  // 핀 모드 설정
  pinMode(leftMotorPin1, OUTPUT);
  pinMode(leftMotorPin2, OUTPUT);
  pinMode(rightMotorPin1, OUTPUT);
  pinMode(rightMotorPin2, OUTPUT);
  pinMode(handlePin1, OUTPUT);
  pinMode(handlePin2, OUTPUT);

  // 시리얼 통신 시작
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("MOTOR")) {
      int motor_id = command.substring(5, 6).toInt();
      String action = command.substring(7, 12);
      int speed = command.substring(13).toInt();

      switch (motor_id) {
        case 1: // 왼쪽 뒤바퀴 모터 제어
          if (action == "SPEED") {
            motor_forward(leftMotorPin1, leftMotorPin2, speed);
          } else if (action == "STOP") {
            motor_hold(leftMotorPin1, leftMotorPin2);
          }
          break;
        case 2: // 오른쪽 뒤바퀴 모터 제어
          if (action == "SPEED") {
            motor_forward(rightMotorPin1, rightMotorPin2, speed);
          } else if (action == "STOP") {
            motor_hold(rightMotorPin1, rightMotorPin2);
          }
          break;
        case 3: // 핸들 모터 제어
          if (action == "SPEED") {
            motor_forward(handlePin1, handlePin2, speed);
          } else if (action == "STOP") {
            motor_hold(handlePin1, handlePin2);
          }
          break;
      }
    }
  }
}
