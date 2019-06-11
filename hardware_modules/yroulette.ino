#include <AccelStepper.h>

#include <SerialCommands.h> //https://github.com/ppedro74/Arduino-SerialCommands

#define HALFSTEP 8

// Motor pin definitions
#define motorPin1  8     // IN1 on the ULN2003 driver 1
#define motorPin2  9     // IN2 on the ULN2003 driver 1
#define motorPin3  10     // IN3 on the ULN2003 driver 1
#define motorPin4  11     // IN4 on the ULN2003 driver 1
#define Y_PIN 0

#define inter_rotation_delay  1 * 1000 //ms

// Initialize with pin sequence IN1-IN3-IN2-IN4 for using the AccelStepper with 28BYJ-48
AccelStepper stepper(HALFSTEP, motorPin1, motorPin3, motorPin2, motorPin4);

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
  stepper.moveTo(stepper.currentPosition() + 32);
  sender->GetSerial()->println("Led is on");
}

void cmd_stepper_minus(SerialCommands* sender)
{
  stepper.moveTo(stepper.currentPosition() - 32);
  sender->GetSerial()->println("Led is off");
}

SerialCommand cmd_stepper_plus_("+", cmd_stepper_plus, true);
SerialCommand cmd_stepper_minus_("-", cmd_stepper_minus,true);

void setup() {
  Serial.begin(115200);
  serial_commands_.SetDefaultHandler(cmd_unrecognized);
  serial_commands_.AddCommand(&cmd_stepper_plus_);
  serial_commands_.AddCommand(&cmd_stepper_minus_);
  serial_commands_.SetDefaultHandler(&cmd_unrecognized);
  
  stepper.setMaxSpeed(25.0);
  stepper.setAcceleration(10.0);
  stepper.setSpeed(50);
  stepper.moveTo(0);
  
}//--(end setup )---


void loop()
{
  
  serial_commands_.ReadSerial();
  if (stepper.distanceToGo() != 0) {
      stepper.run();
      return;
  }
  
  serial_commands_.ReadSerial();
  
  if(analogRead(Y_PIN) < 64){
    cmd_stepper_minus(&serial_commands_);
    }
  else if(analogRead(Y_PIN) > (1023 - 64)){
    cmd_stepper_plus(&serial_commands_);
    }    
 }
