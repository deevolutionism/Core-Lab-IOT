/*
recieve message sent by python over rfduino
send messages sent by python over rfduino
*/

#include <RFduinoGZLL.h>

device_t role = HOST;

// the last known state from DEVICE0 (default to off)
char state = 0;
bool keyPassSent;
String keyPassCharacter;
void setup()
{
  Serial.begin(9600);
  // start the GZLL stack  
  RFduinoGZLL.begin(role);
  Serial.println("beginning Host");
}

void loop()
{
//  String webpage = Serial.readString();
//  Serial.println(webpage);


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


  while (Serial.available() > 0){
  String fromPySerial = Serial.readString();
  Serial.println(fromPySerial);
  RFduinoGZLL.sendToDevice(device, fromPySerial);
  delay(250);
  }


 
}

void passKey(String keyPass){
  keyPassSent = true;
  Serial.println("The KeyPassCharacter is: " + keyPassCharacter);
}

