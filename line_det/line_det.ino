#include <Wire.h>
//setup compass stuff
int HMC6352Address = 0x42;
// This is calculated in the setup() function
int slaveAddress;
byte headingData[2];
int i, headingValue;
int initcompass;

// These constants won't change.  They're used to give names
// to the pins used:
//############  Pins #############
const int p_pt1 = A0;  // Analog input pin for pt array
const int p_pt2 = A1;  
const int p_pt3 = A2;  
const int p_pt4 = A3;  
const int threshold = 500; //thresh for line detection
const int p_cap_trig = 52;
const int p_cap_echo = 53;

void setup() 
{
  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  slaveAddress = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI
  
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  Wire.begin();
  initcompass = get_compass_reading();  //get initial compass value to calculate correction heading

  pinMode(p_cap_trig, OUTPUT);
  pinMode(p_cap_echo, INPUT);
}

void loop() 
{
  //Each iteration of the loop change the value of lineOn from 0-4, with 1-4 being
  //which phototransistor array light has been detected and 0 if none were
  Serial.print(get_pt_reading());
  //Serial.print(0);
  Serial.print("\t");
  
  //reading of the left ultrasonic sensor
  Serial.print(60);
  Serial.print("\t");
  
  //reading of the right ultrasonic sensor
  Serial.print(60);
  Serial.print("\t");
  
  //reading of the compass sensor
  int headingcorrection = initcompass - get_compass_reading();
  Serial.print(headingcorrection);
  Serial.print("\t");
  
  //if the switch is in the 'on' position
  Serial.print(0);
  Serial.print("\t");
  
  //Reading of the capture detection
  //Serial.println(0);
  Serial.println(ball_in_capture());
  
    
  // wait 64 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(64);
}

int get_pt_reading()
{
  if (analogRead(p_pt1) >= threshold)
    return 1;
  else if (analogRead(p_pt2) >= threshold)
    return 2;
  else if (analogRead(p_pt3) >= threshold)
    return 3;
  else if (analogRead(p_pt4) >= threshold)
    return 4;
  else
    return 0;
}

long microsecondsToCentimeters(long microseconds) 
{
   return microseconds / 29 / 2;
}

long get_US_reading(int p_ping, int p_echo)
{
  digitalWrite(p_ping, LOW);
  delayMicroseconds(2);
  digitalWrite(p_ping, HIGH);
  delayMicroseconds(10);
  digitalWrite(p_ping, LOW);
  return microsecondsToCentimeters(pulseIn(p_echo, HIGH));
}

int ball_in_capture()
{
  if (get_US_reading(p_cap_trig, p_cap_echo) <= 4)
    return 1;
  else
    return 0;
}

int get_compass_reading()
{
  // Send a "A" command to the HMC6352
  // This requests the current heading data
  Wire.beginTransmission(slaveAddress);
  Wire.write("A");              // The "Get Data" command
  Wire.endTransmission();
  //delay(10);                   // The HMC6352 needs at least a 70us (microsecond) delay
  // Read the 2 heading bytes, MSB first
  // The resulting 16bit word is the compass heading in 10th's of a degree
  // For example: a heading of 1345 would be 134.5 degrees
  Wire.requestFrom(slaveAddress, 2);        // Request the 2 byte heading (MSB comes first)
  i = 0;
  while(Wire.available() && i < 2)
  { 
    headingData[i] = Wire.read();
    i++;
  }
  headingValue = headingData[0]*256 + headingData[1];  // Put the MSB and LSB together
  return int(headingValue / 10);
}
