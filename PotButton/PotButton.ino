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
int maxAngle = 270;
int minAngle = 30;
int deltaAngle = maxAngle - minAngle;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin,INPUT);
  pinMode(potPin,INPUT);
  attachInterrupt(digitalPinToInterrupt(buttonPin), handleButtonInterrupt, RISING);
}

void loop() {
  if (changeMode) {
    changeMode = !changeMode;
    Serial.print("m ");
    Serial.println(mode);
  } else {
    int angle = deltaAngle*(analogRead(potPin)/1025.0)+minAngle;
    Serial.print("j ");
    Serial.println(angle);
  }
  delay(20);
}

void handleButtonInterrupt() {
  int delta = millis() - oldTime;
  if (delta > btnBounceThresh) {
    changeMode = true;
    mode = mode%3 +1;
    oldTime = millis();
  }
}
