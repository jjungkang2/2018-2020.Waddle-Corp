/*
 *  Trans.h - prototypes and definitions for Transaction
 *  Author : taeyeong
 *  Modify Date: 2019.01.15
 *  Version : 1.0.0
 * */

#ifndef __TRANS_H__
#define __TRANS_H__
#include <SPI.h>
#include <BLEPeripheral.h>
using namespace std;

#define CONNECT_MNUM 5
#define BLE_ATTRIBUTE_MAX_LENGTH 20


enum DataType
{
   DataUnicode=0,
   DataOperator=1
};
 
class Trans
{

  
  BLEPeripheral                    blePeripheral= BLEPeripheral();
  BLEService                          bleService;
  BLECharacteristic*       bleCharacteristic[CONNECT_MNUM];
   struct {
    bool availiable; 
    bool ble_connected=0; // 0 is advertisement, 1 is broadcast 
    uint32_t Max_Length;
    uint8_t property;
    
     uint32_t service_uuid;
    char * characteristic_uuid;
    
   }descriptor_t[CONNECT_MNUM];
   typedef struct{
      char * buf;
   } packet[CONNECT_MNUM];

   public:
  Trans(const char * uuid);
   void Trans_const(int interval)
  {
      blePeripheral.setLocalName("waddle_EVE_1.0");
      blePeripheral.begin();
      Serial.println("BLE Peripheral Begin");
      blePeripheral.setConnectionInterval(interval,interval);
      blePeripheral.setAdvertisedServiceUuid(bleService.uuid());
      blePeripheral.addAttribute(bleService);
  }

   ~Trans();
  int make_descriptor(uint32_t length, char * characteristic_uuid);
  int set_connect(int descriptor_num);
   int write(int descriptor_num, uint8_t buf[]);
   int read();
  void poll();
  



  void Unix_error(char * msg);
   char * make_packet();
  void blePeripheralConnectHandler(BLECentral& central)
{
    Serial.print(F("Connected event, central: "));
    Serial.println(central.address());
}

void blePeripheralDisconnectHandler(BLECentral& central)
{
    Serial.print(F("Disconnected event, central: "));
    Serial.println(central.address());
}


void blePeripheralWrittenHandler(BLECentral& central,BLECharacteristic& characteristic)
{
  characteristic.value();

  // print
  // not implemented
}
  


};

#endif /* __TRANS_H__ */
/* end Trans.h */
