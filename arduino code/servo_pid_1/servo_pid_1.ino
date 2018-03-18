#include <Servo.h>
#include <PID_v1.h>

#define SERVO_PIN_X 9
#define SERVO_PIN_Y 10
#define LIGHT_PIN 3
// PID
double setpoint_x,input_x,output_x;
double setpoint_y,input_y,output_y;
double Kp=1;
double Ki=0;
double Kd=0;
PID x_PID(&input_x,&output_x,&setpoint_x,Kp,Ki,Kd,DIRECT);
PID y_PID(&input_y,&output_y,&setpoint_y,Kp,Ki,Kd,DIRECT);
// SERVO MOTORS
Servo servo_x;
Servo servo_y;
// time
long previousMillis = 0;   
unsigned long currentMillis;    
int interval = 10; // 
void setup() 
{
  // INIT PID
  x_PID.SetSampleTime(interval);
  y_PID.SetSampleTime(interval);
  x_PID.SetOutputLimits(0,30);
  y_PID.SetOutputLimits(0,30);
  x_PID.SetMode(AUTOMATIC);
  y_PID.SetMode(AUTOMATIC);
  //INIT SERVO
  servo_x.attach(SERVO_PIN_Y);
  servo_y.attach(SERVO_PIN_X);
  servo_x.write(15); //move to default position
  servo_y.write(15);
  // init serial
  Serial.begin(9600);
  delay(500);
}

void loop() 
{
  currentMillis = millis();
  if(currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    if(Serial.available() >0)
    {
      setpoint_x = Serial.parseInt();
      input_x = Serial.parseInt();
      setpoint_y = Serial.parseInt();
      input_y = Serial.parseInt();
      int brightness = Serial.parseInt();
      Serial.read(); // flush last ',' from serial buffer,
  
      x_PID.Compute();
      y_PID.Compute();
      /*
      output_x = constrain(output_x,0,30); // servo should rotate between 0 and 30 deg, 
      output_x = constrain(output_y,0,30);
      brightness = constrain(msg_brightness,0,255);
      */
      servo_x.write(output_x);
      servo_y.write(output_y);
      Serial.write((char)output_x);
      Serial.write((char)output_y);
      
      //analogWrite(3, msg_bightness);
    }
  }
  delay(1);
}
