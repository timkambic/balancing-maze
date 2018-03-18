#include <Servo.h> 
 
#define SERVO_PIN_X 9
#define SERVO_PIN_Y 10
#define LIGHT_PIN 3

Servo servo_x;
Servo servo_y;

void setup() 
{
  servo_x.attach(SERVO_PIN_X);
  servo_y.attach(SERVO_PIN_Y);
  
  servo_x.write(0); //move to default position
  servo_y.write(0);
  delay(5000);
}

void loop() 
{
  int msg_x = analogRead(A0);
  int msg_y = analogRead(A1);
  msg_x = map(msg_x,0,1023,0,60);
  msg_y = map(msg_y,0,1023,0,60);
  servo_x.write(msg_x);
  servo_y.write(msg_y);
    
    
 
  delay(1);
}
