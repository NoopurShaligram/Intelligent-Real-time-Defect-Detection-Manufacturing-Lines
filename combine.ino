#include <Servo.h>

// === Servo Setup ===
Servo myServo;
const int servoPin = 9;
const int homeAngle = 90;
const int box1Angle = 30;
const int box2Angle = 60;
const int box3Angle = 90;
const int box4Angle = 120;

// === DC Motor Pins (via L298N) ===
const int IN1 = 4;
const int IN2 = 5;
const int ENA = 6; // PWM pin for speed

void setup() {
  Serial.begin(9600);

  // Servo setup
  myServo.attach(servoPin);
  myServo.write(homeAngle);
  delay(1000);
  myServo.detach(); // Detach to avoid jitter

  // DC Motor setup
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
}

void loop() {
  // Keep motor running forward
  runMotorForward(162);

  // Check for serial input
  if (Serial.available() > 0) {
    char command = Serial.read();
    while (Serial.available() > 0) Serial.read(); // Clear buffer

    int targetAngle = -1;

    switch (command) {
      case 'A':
        delay(4000);
        targetAngle = box1Angle;
        break;
      case 'B':
        delay(4000);
        targetAngle = box2Angle;
        break;
      case 'C':
        delay(4000);
        targetAngle = box3Angle;
        break;
      case 'D':
        delay(4000);
        targetAngle = box4Angle;
        break;
      default:
        return;
    }

    if (targetAngle != -1) {
      myServo.attach(servoPin);
      myServo.write(targetAngle);
      delay(1000);
      myServo.write(homeAngle);
      delay(1000);
      myServo.detach();
    }
  }
}

// === DC Motor Control Function ===
void runMotorForward(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);  // Speed: 0 - 255
}
