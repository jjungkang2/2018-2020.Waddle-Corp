#include "Trans.h"



Trans::Trans(const char * uuid): bleService(uuid)
{
  
}


void Trans::Unix_error(char * msg)
{
  Serial.println(msg);
  exit(0);
  
}

void Trans::poll()
{
  blePeripheral.poll();
}


Trans::~Trans()
{
  
}

int Trans::make_descriptor(uint32_t length, char * characteristic_uuid)
{

  if(length>BLE_ATTRIBUTE_MAX_LENGTH)
    Trans::Unix_error("make_descriptor : can't not exceed length over 20byte");
  
  for(int i=0 ; i< CONNECT_MNUM; i++)
  {
    if(descriptor_t[i].availiable==0)
    {
      descriptor_t[i].availiable=0;
      descriptor_t[i].Max_Length=length;
      descriptor_t[i].characteristic_uuid=characteristic_uuid;
      bleCharacteristic[i] = new BLECharacteristic(characteristic_uuid,BLERead | BLEWriteWithoutResponse | BLENotify,length);

      return i;
    }
  }

  return -1;
}



int Trans::set_connect(int descriptor_num)
{
  blePeripheral.setAdvertisedServiceUuid(bleCharacteristic[descriptor_num]->uuid());
  blePeripheral.addAttribute(*bleCharacteristic[descriptor_num]);
  blePeripheral.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  blePeripheral.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

// needed to modify for each case property


}

int Trans::write(int descriptor_num, uint8_t buf[])
{
  
  
}
