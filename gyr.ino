#include <Wire.h>

const int MPU_ADDR = 0x68;

int16_t accX, accY, accZ;
int16_t gyroX, gyroY, gyroZ;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Wake up MPU6050
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);      // Power management register
  Wire.write(0x00);      // Wake up
  Wire.endTransmission(true);

  Serial.println("MPU6050 Initialized");
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // Starting register for Accel data
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);

  accX = Wire.read() << 8 | Wire.read();
  accY = Wire.read() << 8 | Wire.read();
  accZ = Wire.read() << 8 | Wire.read();

  Wire.read(); Wire.read(); // Temperature (ignored)

  gyroX = Wire.read() << 8 | Wire.read();
  gyroY = Wire.read() << 8 | Wire.read();
  gyroZ = Wire.read() << 8 | Wire.read();

  Serial.print("ACC  X: "); Serial.print(accX);
  Serial.print(" Y: "); Serial.print(accY);
  Serial.print(" Z: "); Serial.print(accZ);

  Serial.print(" | GYRO X: "); Serial.print(gyroX);
  Serial.print(" Y: "); Serial.print(gyroY);
  Serial.print(" Z: "); Serial.println(gyroZ);

  delay(200);
}
