#include <Arduino.h>
#define buttonPin 2
#define potPin 0

// mode of robot control
volatile boolean changeMode = false;
volatile int mode = 0;

// check interrupt time to eliminate hardware bouncing
volatile long oldTime = 0;
long btnBounceThresh = 250;

// angle of robot joint
//int maxAngle = 90; // uncomment for J0
//int minAngle = -90;  // uncomment for J0
//int maxAngle = 110;  // uncomment for J1
//int minAngle = 0; // uncomment for J1
int maxAngle = 90; // uncomment for J2
int minAngle = -110;  // uncomment for J2
int deltaAngle = maxAngle - minAngle;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin,INPUT);
  pinMode(potPin,INPUT);
  attachInterrupt(digitalPinToInterrupt(buttonPin), handleButtonInterrupt, RISING);
}

void loop() {
  if (Serial.available() > 0) {
    String tmp = Serial.readStringUntil("\n");
    Serial.println(tmp.toInt());
    mode = tmp.toInt();
    changeMode = false;
  }
  if (changeMode) {
    Serial.print("m ");
    Serial.println(mode);
    changeMode = false;
  } else {
    int angle = deltaAngle*(analogRead(potPin)/1024.0)+minAngle;
    Serial.print("j ");
    Serial.println(angle);
  }
  delay(50);
}

void handleButtonInterrupt() {
  long delta = millis() - oldTime;
  if (delta > btnBounceThresh) {
    changeMode = true;
    mode = mode%3 + 1;
    oldTime = millis();
  }
}
