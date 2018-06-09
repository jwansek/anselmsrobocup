const int p_in = A0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(p_in, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int reading = analogRead(p_in);
  Serial.println(reading);
}
