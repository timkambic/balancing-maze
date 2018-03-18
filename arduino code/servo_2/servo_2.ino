#include <Servo.h>
#include <PID_v1.h>

#define SERVO_PIN_X 9
#define SERVO_PIN_Y 10
#define LIGHT_PIN 3
// SERVO MOTORS
Servo servo_x;
Servo servo_y;

void setup() 
{
  //INIT SERVO
  servo_x.attach(SERVO_PIN_X);
  servo_y.attach(SERVO_PIN_Y);
  servo_x.write(15); //move to default position
  servo_y.write(15);
  // init serial
  Serial.begin(9600);
  delay(500);
}

void loop() 
{
  if(Serial.available() >0)
  {
     int input_x = Serial.parseInt();
     int input_y = Serial.parseInt();
     int brightness = Serial.parseInt();
     Serial.read(); // flush last ',' from serial buffer,
     
     input_x = constrain(input_x,0,30); // servo should rotate between 0 and 30 deg, 
     input_y = constrain(input_y,0,30);
     brightness = constrain(brightness,0,255);
     
     servo_x.write(input_x);
     servo_y.write(15);
     
      //analogWrite(3, msg_bightness);
  }
  delay(1);
}
