#include <Wire.h>
#define SLAVE 4 // 슬레이브 주소

void setup() {
  Wire.begin(SLAVE); // Wire 라이브러리 초기화, 주소 지정
  Wire.onReceive(receiveEvent); //데이터 전송 시 handler
  Serial.begin(9600);           // start serial for output
}

void loop(){
  delay(100);
}

void receiveEvent(int how_many_bytes)
{
  uint8_t *ch = (uint8_t *)calloc(how_many_bytes, sizeof(uint8_t));
  for (int i = 0 ; i < how_many_bytes ; i++) {
    ch[i] = Wire.read();
  }
  
  // sum is pressed number
  // ch[3] is operator
  
  uint16_t sum = ch[0]<<8 | ch[1];
  Serial.print(sum);
  Serial.println();
  Serial.flush();
  
  free(ch);
}
