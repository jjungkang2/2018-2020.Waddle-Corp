/*  Keypad.cpp
 *  
 *  Author: Yeji Han
 *  Date:   28 January 2019
 *  
 */
#include "Arduino.h"
#include "Keypad.h"

Keypad::Keypad(int p0, int p1, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9, int p10, int p11)
{
    keyPins[0] = p0;
    keyPins[1] = p1;
    keyPins[2] = p2;
    keyPins[3] = p3;
    keyPins[4] = p4;
    keyPins[5] = p5;
    keyPins[6] = p6;
    keyPins[7] = p7;
    keyPins[8] = p8;
    keyPins[9] = p9;
    keyPins[10] = p10;
    keyPins[11] = p11;
    
    pinInfo[0] = 1;
    pinInfo[1] = 2;
    pinInfo[2] = 4;
    pinInfo[3] = 8;
    pinInfo[4] = 16;
    pinInfo[5] = 32;
    pinInfo[6] = 64;
    pinInfo[7] = 128;
    pinInfo[8] = 256;
    pinInfo[9] = 512;
    pinInfo[10] = 1024;
    pinInfo[11] = 2048;
}

Key Keypad::getKey(bool pressedButtons[])
{
  Key key;
  bool singleButtonPressed = false;
    
  for (int i = 0; i < BUTTONCOUNT; i++) {
        bool currentPin = digitalRead(keyPins[i]) == HIGH;
        singleButtonPressed |= currentPin;

        if (currentPin) {
            pressedButtons[i] = true;
        }
    }

    bool anyButtonPressed = false;
    for (int j = 0; j < BUTTONCOUNT; j++)
      anyButtonPressed |= pressedButtons[j];
      
    if (!singleButtonPressed & anyButtonPressed) {
      int letterNum = 0;
      for (int k = 0; k < BUTTONCOUNT; k++) {
        if (pressedButtons[k]) {
              letterNum += pinInfo[k];
              pressedButtons[k] = false;
        }
      }
      key.pressNum = letterNum;
    }
    return key;
}
