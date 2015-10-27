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

// pin for the Green Led
//int LEDpin = 2;
//int LEDpin2 = 3;

//potentiometer analog pins
int xpin = 2;
int ypin = 4;
int zpin = 6;

int xval = 0;
int yval = 0;
int zval = 0;

int xvalp = 0;
int yvalp = 0;
int zvalp = 0;

double x;
double y;
double z;



void setup()
{
  Serial.begin(9600);
//  pinMode(LEDpin, OUTPUT);
//  pinMode(LEDpin2, OUTPUT);
  pinMode(xpin, INPUT); //read pin data
  pinMode(ypin, INPUT); 
  pinMode(zpin, INPUT);

  RFduinoGZLL.txPowerLevel = 0;

  // start the GZLL stack
  RFduinoGZLL.begin(role);
}

void loop()
{
  char xdata[4];   //declare char array
  char ydata[4];
  char zdata[4];
  char mydata[12];

  String xstr; //declaring string
  String ystr;
  String zstr;
  String mystr;

  xval = analogRead(xpin); //read values from potentiometers
  xval = map(xval, 0, 1023, 0, 255);
  yval = analogRead(ypin);
  yval = map(yval, 0, 1023, 0, 255);
  zval = analogRead(zpin);
  zval = map(zval, 0, 1023, 0, 255);

//  xval = 100;
//  yval = 200;
//  zval = 300;

  

  //the next 15+ lines of code are to maintain 12 index length char array for sending data to host.
  if (xval >= 100)
  {
    xstr = String(xval); //convert xval pot data from int to string
  }
  else if (xval < 100 && xval >= 10) {
    xstr = String(0) + String(xval);
  }
  else if (xval < 10) {
    xstr = String(0) + String(0) + String(xval);
  }
  
  
  if (yval >= 100)
  {
    ystr = String(yval);
  }
  else if (yval < 100 && yval >= 10) {
    ystr = String(0) + String(yval);
  }
  else if (yval < 10) {
    ystr = String(0) + String(0) + String(yval);
  }
  
  
  if (zval >= 100)
  {
    zstr = String(zval); 
  }
  else if (zval < 100 && zval >= 10) {
    zstr = String(0) + String(zval);
  }
  else if (xval < 10) {
    zstr = String(0) + String(0) + String(zval);
  }

  //StringvalueToPassIn.toCharArray(charArray, lengthOfArray)
  xstr.toCharArray(xdata, 4); //passing the value of the string to the character array
  ystr.toCharArray(ydata, 4);
  zstr.toCharArray(zdata, 4);
 

  mystr = xstr+"," + ystr+"," + zstr; //total of 12 characters. 9 ints, 2 commas, 1 null character at end

  
  mystr.toCharArray(mydata, 12);

// Serial.print(xdata);
//  Serial.print(", ");
//  Serial.print(ydata);
//  Serial.print(", ");
//  Serial.print(zdata);
//  Serial.print(", ");
  Serial.println(mydata);

 //sendToHost(CharDataToSend, char buffer length) Host will only recieve and interpret Char arrays
 RFduinoGZLL.sendToHost(mydata, 12);
    delay(250);


}

void RFduinoGZLL_onReceive(device_t device, int rssi, char *data, int len)
{
  // ignore acknowledgement without payload
  if (len > 0)
  {
    // set the Green led if this device is the closest device
    device_t closest_device = (device_t)data[0];
    //digitalWrite(green_led, (role == closest_device));
  }
}
