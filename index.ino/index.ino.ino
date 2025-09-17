const int joyXpin=A1;
const int joyYpin=A0;
const int joyState=2;
void setup() {
  Serial.begin(9600);
  pinMode(joyState, INPUT_PULLUP);
  Serial.print("JOYSTICK ON SERIAL MONITOR");
  Serial.print("==========================");
}
void loop() {
  const int joyX=analogRead(joyXpin);
  const int joyY=analogRead(joyYpin);
  const int State=digitalRead(joyState);
  // put your main code here, to run repeatedly:
  Serial.print(joyX);
  Serial.print(",");
  Serial.print(joyY);
  Serial.print(",");
  Serial.print(State);
  Serial.println();
  delay(100);
}
