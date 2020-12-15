#include <ax12.h>

String jointValue;
#define numJoints 3
int jointValues[numJoints];
const float posPerDegree = 1024/300.0; // 1023 max position of dynamixel ax12 at max angle of 300 degree
const int motorSpeed = 75; // max speed is 1023 which corresponds to  113.664 RPM

void setup() {
  dxlInit(1000000); // initiate dynamixel communication 1mbps

  for (int i=1; i<=numJoints; i++) { // make sure each servo is in joint mode
    dxlSetGoalSpeed(i, motorSpeed);
    if(dxlGetMode(i) != JOINT_MODE) { // preserve EEPROM
      axSetJointMode(i);
    }
  }
  Serial.begin(9600);
}
void loop() {
  bool shouldMove = false;
  if (Serial.available() > 0) {
    String val = Serial.readStringUntil('\n');
    int jointAngleStart = 0; // joint angle 0 starts at 0th character
    int jointAngleEnd; // joint angle 0 ends at first instance of " "
    // assuming properly formed input (j0 j1 j2 ... jn)
    for (int index = 0; index < numJoints; index++) {
      val = val.substring(jointAngleStart);
      jointAngleEnd = val.indexOf(" "); // get substring from starting point to end, then find index of next " "
      if (jointAngleEnd != -1) { // if space is found then get value
        jointValues[index] = val.substring(0,jointAngleEnd).toInt(); // get value of joint angle
      } else {
        jointValues[index] = val.toInt();
      }
      jointAngleStart = jointAngleEnd+1;

      //if not assuming properly formed then need following will handle input that has too many values
      //  but need to take into account if the input doesn't have enough values
      //if (index == (numJoints - 1)) {
      //  val = val.substring(jointAngleEnd);
      //  if (val.equals(" ") || val.length() == 0) {
      //    shouldMove = true;
      //  }
      //}
    }

    //if (shouldMove) {
      Serial.println("should move");
      moveJoints(jointValues);
    //}
  }
}

void moveJoints(int *jointAngles){
  float pos;
  for (int index =0; index < numJoints; index++) {
    printJointValue(index, jointAngles[index]);
    pos = angle2MotorPos(index, jointAngles[index]);
    printJointValue(index, pos);
    dxlSetGoalPosition(index+1, pos);
  }
}

void printJointValue(int jointIndex, float value) {
  Serial.print("j");
  Serial.print(jointIndex);
  Serial.print(" ");
  Serial.print(value);
  Serial.println(" ");
}

int angle2MotorPos(int joint, int angle) {
  int motorPos;
  if (joint == 0) {
    motorPos = (150 + angle) * posPerDegree; // 150 degree on dynamixel is the center for joint 0 frame 
  } else if (joint == 1) { //joint == 1
    motorPos = (240 - angle) * posPerDegree; // 240 degree on dynamixel is the center for joint 1 frame
  } else {
    motorPos = (150 - angle) * posPerDegree; // 150 degree on dynamixel is the center for joint 0 frame 
  }
  Serial.println(motorPos);
  return motorPos;
}
