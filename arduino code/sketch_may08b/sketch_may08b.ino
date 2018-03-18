#include <Servo.h> 
 
#define SERVO_PIN_X 9
#define SERVO_PIN_Y 10
#define LIGHT_PIN 3

Servo servo_x;
Servo servo_y;
int i=0;
void setup() 
{
  servo_x.attach(SERVO_PIN_X);
  servo_y.attach(SERVO_PIN_Y);
  
  servo_x.write(0); //move to default position
  servo_y.write(0);
  Serial.begin(9600);
  delay(500);
  Serial.print("starting");
  
}

void loop() 
{
  if(Serial.available()>0)
  {
    char a=Serial.read();
    servo_x.write(i);
    servo_y.write(i);
    Serial.println(i);
    i+=5;
    delay(100);
}  
    
 
  delay(1);
}
