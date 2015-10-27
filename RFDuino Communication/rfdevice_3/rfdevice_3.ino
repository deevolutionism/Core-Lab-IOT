/*
Read incoming python text, then
*/

#include <RFduinoGZLL.h>


device_t role = DEVICE2;

char state=0;
bool keyPassSent;
String keyPassCharacter;


void setup()
{
  Serial.begin(9600);
  
  RFduinoGZLL.txPowerLevel = 0;

  // start the GZLL stack
  RFduinoGZLL.begin(role);
  
}

void loop()
{

  while (Serial.available() > 0){
  String fromPySerial = Serial.readString();
  Serial.println(fromPySerial);

 
 RFduinoGZLL.sendToHost(fromPySerial);
  delay(250);
  }
}

void RFduinoGZLL_onReceive(device_t device, int rssi, char *data, int len)
{

  if(keyPassSent == false){
    keyPassCharacter = data; //set the keyPass 
    Serial.println("waiting for key pass");
    passKey(keyPassCharacter); 
  } else if (keyPassSent == true){
    Serial.println("looking for message");
    String incomingData = data;
    char keyCharacter = incomingData.charAt(1);
    if (String(keyCharacter) == keyPassCharacter){
        Serial.println(data);
        Serial.write(data);
    }
    
  }


 
}

void passKey(String keyPass){
  keyPassSent = true;
  Serial.println("The KeyPassCharacter is: " + keyPassCharacter);
}

