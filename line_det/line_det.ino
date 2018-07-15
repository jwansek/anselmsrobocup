// These constants won't change.  They're used to give names
// to the pins used:
const int p_pt1 = A0;  // Analog input pin for pt array
const int p_pt2 = A1;  
const int p_pt3 = A2;  
const int p_pt4 = A3;  
const int threshold = 600; //thresh for line detection
const int p_ping_cap = 52; //Digital output pin for ball capture ultrasonic sensor
const int p_echo_cap = 50; //Digital input pin for ball capture ultrasonic sensor

void setup() 
{
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(p_ping_cap, OUTPUT);
  pinMode(p_echo_cap, INPUT);
}

void loop() 
{
  //Each iteration of the loop change the value of lineOn from 0-4, with 1-4 being
  //which phototransistor array light has been detected and 0 if none were
  //Serial.print(get_pt_reading());
  Serial.print(0);
  Serial.print("\t");
  //reading of the left ultrasonic sensor
  Serial.print(60);
  Serial.print("\t");
  //reading of the right ultrasonic sensor
  Serial.print(60);
  Serial.print("\t");
  //reading of the compass sensor
  Serial.print(15);
  Serial.print("\t");
  //if the switch is in the 'on' position
  Serial.print(0);
  Serial.print("\t");
  //Reading of the capture detection
  Serial.println(get_US_reading(p_ping_cap, p_echo_cap));
  //Serial.println(0);
  
    
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

