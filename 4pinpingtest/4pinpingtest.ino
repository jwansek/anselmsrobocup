const int p_trig = 46;
const int p_echo = 41;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(p_trig, OUTPUT);
  pinMode(p_echo, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(get_US_reading(p_trig, p_echo));

  delay(128);

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

long microsecondsToCentimeters(long microseconds) 
{
   return microseconds / 29 / 2;
}

