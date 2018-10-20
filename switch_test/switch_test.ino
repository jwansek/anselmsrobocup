const int p_switch = 52;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(p_switch, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:  
  Serial.println(get_switch_state());
  delay(64);

}

int get_switch_state(){
  //inverse because wire attached to other side of switch
  if (digitalRead(p_switch) == LOW)
    return 0;
  else
    return 1;              
}
                                    
