/* Keypad.h
 *
 * Author: Yeji Han
 * Date:   28 January 2019
 * Library for 8-key keyapd.
 */

#ifndef KEYPAD_H
#define KEYPAD_H

const int BUTTONCOUNT = 12;

struct Key
{
  uint16_t pressNum = 0;
  uint8_t oper = 0;
};

class Keypad
{
public:
  int keyPins[BUTTONCOUNT];
  int pinInfo[BUTTONCOUNT];

  Keypad(int p0, int p1, int p2, int p3, int p4, int p5,int p6, int p7, int p8, int p9, int p10, int p11);
  Key getKey(bool pressedButtons[]);
};

#endif
