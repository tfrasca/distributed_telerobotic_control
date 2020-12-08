//#include <ax12.h>

String jointValue;
#define numJoints 3
int jointValues[numJoints];
void setup() {
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
  for (int index =0; index < numJoints; index++) {
    printJointValue(index+1, jointAngles[index]);
    //dxlSetGoalPosition(index+1, jointAngles[index]);
  }
}

void printJointValue(int jointIndex, int angle) {
  Serial.print("j");
  Serial.print(jointIndex);
  Serial.print(" ");
  Serial.print(angle);
  Serial.println(" ");
}
