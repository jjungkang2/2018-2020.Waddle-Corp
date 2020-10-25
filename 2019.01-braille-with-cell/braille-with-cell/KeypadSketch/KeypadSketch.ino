/*  KeypadSketch.ino
 *	
 *	Author: Yeji Han
 *	Date:   30 January 2019
 *	
 */


#include "Keypad.h"
#include "Wire.h"

#define SLAVE 4

Keypad keypad(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
bool pressedButtons[] = { false, false, false, false, false, false, false, false, false, false, false, false };

void setup() {
  Serial.begin(9600);
    Wire.begin();
  	for(int i = 0; i < BUTTONCOUNT; i++) {
        pinMode(keypad.keyPins[i], INPUT);  
    }
}

void loop() {
  
    Key key = keypad.getKey(pressedButtons);
    
    if (key.pressNum != 0) {
        Wire.beginTransmission(SLAVE);
        Wire.write((uint8_t)(key.pressNum>>8));
        Wire.write((uint8_t)(key.pressNum& 0xff));
        Wire.write(key.oper);
        Wire.endTransmission();
    }

    delay(100);
}
