#include <Arduino.h>

const int CW_PIN = 5;
const int CCW_PIN = 6;
const int RIGHT_SENSOR_PIN = 11;
const int LEFT_SENSOR_PIN = 10;

const float STEP_ANGLE = 0.72;
const int SENSOR_DELAY = 1000;
const int STEP_DELAY = 10000;

bool resetting = true;
bool motorStopped = true;
bool rotatingCW = true;  // Define the rotating direction flag

void setup() {
  pinMode(CW_PIN, OUTPUT);
  pinMode(CCW_PIN, OUTPUT);
  pinMode(RIGHT_SENSOR_PIN, INPUT);
  pinMode(LEFT_SENSOR_PIN, INPUT);
  Serial.begin(115200);
}

void rotateMotor(int steps, bool clockwise) {
  int sensorPin = clockwise ? RIGHT_SENSOR_PIN : LEFT_SENSOR_PIN;
  int interruptSteps = steps;

  digitalWrite(clockwise ? CCW_PIN : CW_PIN, HIGH);

  for (int i = 0; i < steps; i++) {
    if (digitalRead(sensorPin) == LOW) {
      interruptSteps = i;
      break;
    }

    digitalWrite(clockwise ? CCW_PIN : CW_PIN, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(clockwise ? CCW_PIN : CW_PIN, LOW);
    delayMicroseconds(STEP_DELAY);
  }

  digitalWrite(CW_PIN, LOW);
  digitalWrite(CCW_PIN, LOW);

  if (interruptSteps > 0) {
    int interruptedAngle = interruptSteps * STEP_ANGLE;
    Serial.println("SENSOR: " + String(clockwise ? "CW" : "CCW") + ", " + String(interruptedAngle));
    delay(SENSOR_DELAY);
    digitalWrite(clockwise ? CW_PIN : CCW_PIN, HIGH);
    delayMicroseconds(STEP_DELAY * 8);
    digitalWrite(clockwise ? CW_PIN : CCW_PIN, LOW);
    delay(SENSOR_DELAY);
    Serial.println("Restarted: " + String(clockwise ? "CCW" : "CW") + ", 8");
  }
}

void stopMotor() {
  digitalWrite(CW_PIN, LOW);
  digitalWrite(CCW_PIN, LOW);
  motorStopped = true;
  Serial.println("Motor Stopped");
}

void powerReset() {
  resetting = true;
  while (digitalRead(RIGHT_SENSOR_PIN) == HIGH) {
    rotateMotor(1, false);
  }
  delay(1000);

  while (digitalRead(LEFT_SENSOR_PIN) == HIGH) {
    rotateMotor(1, true);
    delay(SENSOR_DELAY);
  }

  if (digitalRead(LEFT_SENSOR_PIN) == LOW) {
    stopMotor();
    delay(SENSOR_DELAY);
    rotateMotor(int(8 / STEP_ANGLE), false);
    delay(SENSOR_DELAY);
    stopMotor();
    motorStopped = true;
    Serial.println("Home Base");
  }
}

void cw90() {
  resetting = false;
  int targetSteps = int(90 / STEP_ANGLE);
  rotateMotor(targetSteps, true);
  stopMotor();
  Serial.println("CW: 90");
}

void ccw90() {
  resetting = false;
  int targetSteps = int(90 / STEP_ANGLE);
  rotateMotor(targetSteps, false);
  stopMotor();
  Serial.println("CCW: 90");
}

void angleCMD() {
  if (Serial.available()) {
    int angle = Serial.parseInt();
    bool clockwise = angle < 0;

    int steps = abs(angle) / STEP_ANGLE;
    rotateMotor(steps, clockwise);

    Serial.println(String(clockwise ? "CW" : "CCW") + ": " + String(abs(angle)));
  }
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'C':
        cw90();
        break;
      case 'D':
        ccw90();
        break;
      case 'R':
        powerReset();
        break;
      case 'S':
        stopMotor();
        break;
      case 'I':
        if (rotatingCW || !rotatingCW) {
          Serial.println("Rotating: " + String(rotatingCW ? "CW" : "CCW"));
        } else if (resetting) {
          Serial.println("Rotating to Home Base");
        } else if (motorStopped) {
          if (digitalRead(LEFT_SENSOR_PIN) == LOW) {
            Serial.println("Stopped: Home Base");
          } else {
            Serial.println("Stopped: Not Home Base");
          }
        }
        break;
      case 'V':
        //speed change
        break;
      default:
        angleCMD();
        break;
    }
  }
}
