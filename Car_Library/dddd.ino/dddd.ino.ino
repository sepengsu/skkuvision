int motorA1 = 6;    // 모터 드라이버 IN1
int motorA2 = 7;    // 모터 드라이버 IN2

void setup() {
  Serial.begin(9600);       // 시리얼 통신 시작, 통신 속도 설정
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
}

void motor_forward(int IN1, int IN2, int speed) {
  analogWrite(IN1, speed);
  analogWrite(IN2, 0);
}

void motor_backward(int IN1, int IN2, int speed) {
  analogWrite(IN1, 0);
  analogWrite(IN2, speed);
}

void motor_hold(int IN1, int IN2) {
  analogWrite(IN1, 0);
  analogWrite(IN2, 0);
}

void loop() {
  // Forward
  Serial.println("Motor Forward");
  motor_forward(motorA1, motorA2, 75);
  delay(3000);

  // Backward
  Serial.println("Motor Backward");
  motor_backward(motorA1, motorA2, 150);
  delay(3000);

  // Hold
  Serial.println("Motor Hold");
  motor_hold(motorA1, motorA2);
  delay(3000);
}
