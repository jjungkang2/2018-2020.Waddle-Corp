//Auther: Auejin Ham, Yeji Han, Minseong Jang, Tae Yeong Heo, Jeong Eun Kim

#include <SPI.h>
#include <BLEPeripheral.h>
#include <LedControlMS.h>
#include <String.h>

//Braille
#include "WordToBraille.h"
#include "BrailleToWord.h"

//Display
#include "Display.h"

#define MAX_LedM 13

//custom boards may override default pin definitions with BLEPeripheral(PIN_REQ, PIN_RDY, PIN_RST)
BLEPeripheral                    blePeripheral                            = BLEPeripheral();

// create service
BLEService              Service           = BLEService("ffff");

// create switch characteristic
BLEUnsignedCharCharacteristic   Characteristic = BLEUnsignedCharCharacteristic("fff1", BLERead | BLEWrite | BLENotify);
String BLEbuf= String("");
Word w_;
Braille b_;
bool Notified=false;

// keyboard part
unsigned char c_B;
const int buttonCount = 7; //버튼의 갯수 //아래 4개의 array의 크기는 buttonCount여야 함
const int inputPins[] = {2,3,4,5,6,7,8};
const int pinInfo[] = {32, 16, 8, 4, 2, 1, 0}; // 2진수-10진수 변환출력용

bool rawData[] = {false, false, false, false, false, false, false}; // 단일 loop()때 인식한 센서값
bool pressedButtons[] = {false, false, false, false, false, false, false}; // 전부 때기 전까지 누른 버튼

int buf[300], cursor = 0, *bufp = NULL;

void setup() {
  Serial.begin(9600);
#if defined (__AVR_ATmega32U4__)
  delay(1000);  //5 seconds delay for enabling to see the start up comments on the serial board
#endif
//* DISPLAY PART * //

  for (int i=0; i<5; i++){
    lc.shutdown(i,false);
    lc.setIntensity(i,1);
    lc.clearDisplay(i);
  }
  delay(100);
  lc.clearAll();


 //* BRAILLE PART *//
  for(int i = 0; i < buttonCount; i++)
  {
    pinMode(inputPins[i], INPUT);
  }

  for(int i = 0; i < 300; i++){
    buf[i] = -1;
  }
  bufp = buf;

  Serial.println("--== arduino setup complete! ==--");
  delay(1000);



 //* NEWTWORK INITIALIZE *//

  // set advertised local name and service UUID
  blePeripheral.setLocalName("waddle");
  blePeripheral.setAdvertisedServiceUuid(Service.uuid());
  blePeripheral.setAdvertisedServiceUuid(Characteristic.uuid());

  // add service and characteristic
  blePeripheral.addAttribute(Service);
  blePeripheral.addAttribute(Characteristic);

  // assign event handlers for connected, disconnected to peripheral
  blePeripheral.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  blePeripheral.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

  // assign event handlers for characteristic
  Characteristic.setEventHandler(BLEWritten, switchCharacteristicWritten);

  // begin initialization
  blePeripheral.begin();
  Characteristic.setValue(-1);
  Serial.println(F("BLE Peripheral"));

  
  
}

void loop() {
  // poll peripheral
  

  // put your main code here, to run repeatedly:

  bool singleButtonPressed = false; // 기본값; loop()당 1개 이상 버튼 눌렸는가
  for(int i=0; i<buttonCount; i++){
    bool currentPin = digitalRead(inputPins[i]) == HIGH;
    singleButtonPressed = singleButtonPressed | currentPin;

    if(currentPin){ // true만 누적
      pressedButtons[i] = true;
    }
  }

  bool buttonsHavePressed = false;
  // pressedButtons[0] | pressedButtons[1] | ... | pressedButtons[buttonCount];
  for(int i=0; i<buttonCount; i++){
    if(pressedButtons[i]){
      buttonsHavePressed = true;
      break;
    }
  }


  if(!singleButtonPressed & buttonsHavePressed){ //다 누른 후 손가락 땠을 때 누른 결과 출력
    
    if(Notified==true)
      {
        memset(buf,-1,300);
        bufp=buf;
        Notified=false;
      }
    
    int letterNum = 0; //1~buttonCount번핀 눌림 여부를 10진수로 저장
    bool shortcut_activated = false;
    
    for(int i=0; i<buttonCount; i++){
      if(pressedButtons[i]){
        letterNum = letterNum + pinInfo[i];
      }      
    }
    
    if(!activate_shortcut()){ 
      buf[cursor++] = letterNum;
      // c_B <- letter num

      int *np = &letterNum;
      b_.Init(np, 1);
      w_ = b_.BrailleToWord();
      c_B=w_.get(0);
      w_.FreeWord();
      
      if(cursor % MAX_LedM == 1 && cursor > MAX_LedM){
        bufp += MAX_LedM;
      }

      
    }
    //printNum();

    Display(bufp);
    Characteristic.setValue(c_B);
    Characteristic.broadcast();

    
    
    for(int i=0; i<buttonCount; i++){
      pressedButtons[i] = false;
    }
  }


  //

  
  blePeripheral.poll();
}
// pointer -> int& buf[i];


void printNum(){
  for(int i = 0; i < MAX_LedM; i++){
    if((*(bufp + i)) >= 0)
      Serial.print(*(bufp + i), BIN);
    Serial.print("^");
  }
  Serial.println();
}

bool activate_shortcut(){ //단축키 입력을 의미
  bool activated = false;
  if(pressedButtons[5] & pressedButtons[6]){
    if(cursor != 0){
      c_B = 8;
      buf[--cursor] = -1;
      if(cursor % MAX_LedM == 0 && cursor >= MAX_LedM){
        bufp -= MAX_LedM;
      }
    }
    activated = true;
  }
  
  if(pressedButtons[4] & pressedButtons[6]){
    buf[cursor++] = 0;
    c_B = 32;
    if(cursor % MAX_LedM == 1 && cursor > MAX_LedM){
      bufp += MAX_LedM;
    }
    activated = true;
  }
  
  if(pressedButtons[3] & pressedButtons[6]){
    c_B = 13;
    if(cursor % MAX_LedM == 0){
      if(cursor != 0){
        bufp += MAX_LedM;
      }
      for(int i = 0; i < MAX_LedM; i++){
        buf[cursor++] = 0;
      }
    }
    else{
      while((cursor % MAX_LedM) != 0){
        buf[cursor++] = 0;
      }
    }
    activated = true;
  }
  return activated;
}


void blePeripheralConnectHandler(BLECentral& central) {
  // central connected event handler
  Serial.print(F("Connected event, central: "));
  Serial.println(central.address());
}

void blePeripheralDisconnectHandler(BLECentral& central) {
  // central disconnected event handler
  Serial.print(F("Disconnected event, central: "));
  Serial.println(central.address());
}

void switchCharacteristicWritten(BLECentral& central, BLECharacteristic& characteristic) {
  // central wrote new value to characteristic, update LED
  char c=Characteristic.value();
  BLEbuf+=c;
  Serial.println(BLEbuf);

  if(c==0)
  {
    // BUF INITIALIZE
    char imsi[300];
    int c_imsi, * bufp_imsi, len;

    // char to braile
    Serial.println("yaho");
    

    char * cstr = (char*)malloc(sizeof(char) * 500);
    for(int i = 0; i < BLEbuf.length(); i++){
      cstr[i] = BLEbuf[i];
    }
    //len=BLEbuf.length();
    BLEbuf = String("");
    
    w_.Init(cstr);
    b_ = w_.WordToBraille();

    memcpy(imsi, buf, 300);
    bufp_imsi=bufp;
    c_imsi= cursor;
    memset(buf, -1, 300);
    cursor=0, bufp=buf; // 초기화 꼭 함수로 구현해주기
    Serial.println(b_.BrailleLen());
    for(int i=0; i <b_.BrailleLen();i++ ){
       buf[i]=b_.get(i);
       Serial.println(buf[i]);
    }
    Serial.println("haha");
    //b_.FreeBraille();
    Display(bufp);
    free(cstr);
    Notified=true;
   
    

    
    
  }
   
}
