#include <Servo.h>
#include <SerialCommands.h> //https://github.com/ppedro74/Arduino-SerialCommands

#define HALFSTEP 8
#define SERVO_PIN 3
#define Y_PIN 0
#define NEUTRAL_PWM 1500

#define inter_rotation_delay  1 * 1000 //ms

Servo myservo;

char serial_command_buffer_[32];
SerialCommands serial_commands_(&Serial, serial_command_buffer_, sizeof(serial_command_buffer_), "\r\n", " ");

//This is the default handler, and gets called when no other command matches. 
// Note: It does not get called for one_key commands that do not match
void cmd_unrecognized(SerialCommands* sender, const char* cmd)
{
  sender->GetSerial()->print("Unrecognized command [");
  sender->GetSerial()->print(cmd);
  sender->GetSerial()->println("]");
}

void cmd_stepper_plus(SerialCommands* sender)
{
  myservo.writeMicroseconds(NEUTRAL_PWM + 10);
  delay(1000);
  myservo.writeMicroseconds(NEUTRAL_PWM );
 
 // sender->GetSerial()->println("Led is on");
}

void cmd_stepper_minus(SerialCommands* sender)
{

  myservo.writeMicroseconds(NEUTRAL_PWM - 10);
  delay(1000);
  myservo.writeMicroseconds(NEUTRAL_PWM);
 }

SerialCommand cmd_stepper_plus_("+", cmd_stepper_plus, true);
SerialCommand cmd_stepper_minus_("-", cmd_stepper_minus,true);

void setup() {
  Serial.begin(115200);
  serial_commands_.SetDefaultHandler(cmd_unrecognized);
  serial_commands_.AddCommand(&cmd_stepper_plus_);
  serial_commands_.AddCommand(&cmd_stepper_minus_);
  serial_commands_.SetDefaultHandler(&cmd_unrecognized);

  myservo.attach(5); 
  myservo.writeMicroseconds(1480);  
  
}//--(end setup )---


void loop()
{
  
  serial_commands_.ReadSerial();

  serial_commands_.ReadSerial();
  
  if(analogRead(Y_PIN) < 64){
    cmd_stepper_minus(&serial_commands_);
    }
  else if(analogRead(Y_PIN) > (1023 - 64)){
    cmd_stepper_plus(&serial_commands_);
    }    
 }
