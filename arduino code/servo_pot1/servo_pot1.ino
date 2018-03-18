#include <Servo.h>

Servo servo_x;
Servo servo_y;
void setup() {
  servo_x.attach(9);
  servo_y.attach(10);
  Serial.begin(9600);
  servo_x.write(0);
  servo_y.write(0);
  
}

void loop() {
  int a = analogRead(A3);
  int b = map(a,0,1023,0,180);
  servo_x.write(b);
  servo_y.write(b);
  Serial.println(b);
  delay(10);

}
