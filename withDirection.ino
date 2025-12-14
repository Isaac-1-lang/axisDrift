const int xPin = A0;
const int yPin = A1;
const int swPin = 2;

const int center = 512;
const int deadZone = 100;

void setup() {
  Serial.begin(9600);
  pinMode(swPin, INPUT_PULLUP);
  Serial.println("Joystick Direction Test");
}

void loop() {
  int x = analogRead(xPin);
  int y = analogRead(yPin);
  int sw = digitalRead(swPin);

  String direction = "CENTER";

  // X-axis (LEFT / RIGHT)
  if (x < center - deadZone) {
    direction = "LEFT";
  } 
  else if (x > center + deadZone) {
    direction = "RIGHT";
  }

  // Y-axis (UP / DOWN)
  if (y < center - deadZone) {
    direction = "DOWN";
  } 
  else if (y > center + deadZone) {
    direction = "UP";
  }

  // Button
  if (sw == LOW) {
    direction += " + BUTTON";
  }

  Serial.print("X=");
  Serial.print(x);
  Serial.print(" Y=");
  Serial.print(y);
  Serial.print(" -> ");
  Serial.println(direction);

  delay(200);
}
