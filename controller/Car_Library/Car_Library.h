#ifndef Car_Lib_h
#define Car_Lib_h

float ultrasonic_distance(int trigPin, int echoPin);
int potentiometer_Read(int pin);

void motor_forward(int IN1, int IN2, int speed);
void motor_backward(int IN1, int IN2, int speed);
void motor_hold(int IN1, int IN2);


#endif