#include <Wire.h>
#define SLAVE 4 // 슬레이브 주소

void setup() {
  Wire.begin(); // Wire 라이브러리 초기화
}

byte x = 0;

void loop()
{
  Wire.beginTransmission(SLAVE); // 슬레이브 장치로 전송 시작
  Wire.write("x is ");        // sends five bytes
  Wire.write(x);              // sends one byte
  Wire.endTransmission();    // stop transmitting

  x++;
  delay(500);
}
