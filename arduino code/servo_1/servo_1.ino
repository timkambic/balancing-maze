#include <Servo.h> 
 
#define SERVO_PIN_X 9
#define SERVO_PIN_Y 10
#define LIGHT_PIN 3

Servo servo_x;
Servo servo_y;

// incoming command should be "positionX,positionY,brightness,"

void setup() 
{
  servo_x.attach(SERVO_PIN_X);
  servo_y.attach(SERVO_PIN_Y);
  
  servo_x.write(15); //move to default position
  servo_y.write(15);
  
  Serial.begin(9600);
  delay(1000);
}

void loop() 
{
  
  int msg_x,msg_y,msg_brightness;
  if(Serial.available() >0)
  {
    msg_x = Serial.parseInt();
    msg_y = Serial.parseInt();
    msg_brightness = Serial.parseInt();
    Serial.read(); // flush last ',' from serial buffer,

    msg_x = constrain(msg_x,0,30); // servo should rotate between 0 and 30 deg, 
    msg_y = constrain(msg_y,0,30);
    msg_brightness = constrain(msg_brightness,0,255);
    
    servo_x.write(msg_x);
    servo_y.write(msg_y);
    
    //analogWrite(3, msg_bightness);
  }
  //delay(1);
}
