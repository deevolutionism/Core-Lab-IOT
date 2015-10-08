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

device_t role = DEVICE0;

// pin for the Green Led
int green_led = 3;
char message;

void setup()
{
  Serial.begin(57000);
  pinMode(green_led, OUTPUT);

  //RFduinoGZLL.txPowerLevel = 0;

  // start the GZLL stack
  RFduinoGZLL.begin(role);
  
  
}

void loop()
{
  delay(200);
    //read message recieved from python
    message = Serial.read(); // store data as char
    Serial.println(message); //print char

  // request the state from the Host (send a 0 byte payload)
  RFduinoGZLL.sendToHost(message); //send the message out to the host device over bluetooth
}

void RFduinoGZLL_onReceive(device_t device, int rssi, char *data, int len) //print the recieved message to python terminal
{
  char recievedMessage = data[0]; //collect data recieved
  Serial.print(recievedMessage); //send message out to python
}
