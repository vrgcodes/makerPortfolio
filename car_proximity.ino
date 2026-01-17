int echo = 11;
int trig = 12;
int buzzer = 9;
float duration;
float distance;
float delayDuration;
int potentiometer = A0;
int pwmValue;

void setup() {
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(potentiometer, INPUT);

}

void loop() {
  int analogValue = analogRead(potentiometer);
  pwmValue = map(analogValue, 0, 1023, 0, 255);
  
  

  digitalWrite(trig, LOW);
  delay(2);
  digitalWrite(trig, HIGH);
  delay(10);
  digitalWrite(trig, LOW);

  duration = pulseIn(echo, HIGH);
  distance = duration*(0.034/2);
  delayDuration = distance*5;

  if (distance < 50){
    analogWrite(buzzer, pwmValue);
    delay(delayDuration);
    digitalWrite(buzzer, LOW);
  };

}
