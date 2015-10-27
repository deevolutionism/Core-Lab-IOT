/*
This sketch demonstrates how to coordinate data
between 3 devices in a Gazell network.

The host collects RSSI samples from the Devices,
and determines which device has the strongest
average RSSI (ie: the Device that is closest
to the Host).  The Green led is set on the
closest Device.

Since the Device must initiate communication, the
device "polls" the Host evey 200ms.
*/

#include <RFduinoGZLL.h>


device_t role = DEVICE2;
int potPin = 2;

int potValue = 0;
char potData[4];



void setup()
{
  Serial.begin(9600);
  
  RFduinoGZLL.txPowerLevel = 0;

  // start the GZLL stack
  RFduinoGZLL.begin(role);
  Serial.println("broadcasting signal");
}

void loop()
{
 
 potPin = analogRead(potPin); 
 potValue = map(potPin,0,1023,0,255);
  Serial.println(potValue);
 String potStr = String(potValue);
 potStr.toCharArray(potData, 4);

 //(value to send, number of characters sending + nill character)
 RFduinoGZLL.sendToHost(potStr);
    delay(250);
}

//void RFduinoGZLL_onReceive(device_t device, int rssi, char *data, int len)
//{
//  // ignore acknowledgement without payload
//  if (len > 0)
//  {
//    // set the Green led if this device is the closest device
//    device_t closest_device = (device_t)data[0];
//    //digitalWrite(green_led, (role == closest_device));
//  }
//}
