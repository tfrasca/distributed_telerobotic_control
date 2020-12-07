//#include <ax12.h>

String jointValue;
#define numJoints 3
int jointValues[numJoints];
void setup() {
  Serial.begin(9600);
}
void loop() {
  bool shouldRead = true;
  int index = 0;
  bool shouldMove = false;
  while (shouldRead) { // wait until 'end' is received 
    if (Serial.available() > 0) {
      String val = Serial.readStringUntil('\n');
      if (val.equals("end")) {
        shouldRead = false;
        shouldMove = true;
      } else {
        if (index == numJoints) { // cannot accept more than numJoints joint positions
          shouldRead = false;
          shouldMove = false;
        } else {
          jointValues[index++] = val.toInt();
        }
      }
    }
  }
  if (shouldMove) {
    moveJoints(jointValues);
  }
}

void moveJoints(int *jointValues){
  Serial.println(jointValues[0]);
  Serial.println(jointValues[1]);
  Serial.println(jointValues[2]);
  //dxlSetGoalPosition(1, jointValues[0]);
  //dxlSetGoalPosition(2, jointValues[1]);
  //dxlSetGoalPosition(3, jointValues[2]);
}
