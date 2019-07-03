#include <AccelStepper.h>

#include <SerialCommands.h> //https://github.com/ppedro74/Arduino-SerialCommands

#define BAUD 115200
#define HALFSTEP 8

// Motor pin definitions
#define motorPin1  8     // IN1 on the ULN2003 driver 1
#define motorPin2  9     // IN2 on the ULN2003 driver 1
#define motorPin3  10     // IN3 on the ULN2003 driver 1
#define motorPin4  11     // IN4 on the ULN2003 driver 1
#define X_PIN 0
#define Y_PIN 1
#define CLICK_PIN 12

#define VALVE_RELAY_PIN 13

#define inter_rotation_delay  1 * 1000 //ms



int   valve_timer = 0; // n ms milliseconds left for the valve to be open
int t0 = 0;


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
  stepper.moveTo(stepper.currentPosition() + 1);
}

void cmd_stepper_minus(SerialCommands* sender)
{
  stepper.moveTo(stepper.currentPosition() - 1);
}




void cmd_stepper_big_minus(SerialCommands* sender)
{
  stepper.moveTo(stepper.currentPosition() - 64);
}


void cmd_stepper_big_plus(SerialCommands* sender)
{
  stepper.moveTo(stepper.currentPosition() + 64);
}

void cmd_valve_open(SerialCommands* sender)
{
  digitalWrite(VALVE_RELAY_PIN, LOW);
}

void cmd_valve_close(SerialCommands* sender)
{
  digitalWrite(VALVE_RELAY_PIN,HIGH);
}

void open_valve_ms(int t){
  valve_timer = t;
 }

void cmd_run_step(SerialCommands* sender){
  int pos =  stepper.currentPosition();

  digitalWrite(VALVE_RELAY_PIN, LOW);

  delay(2000);
    stepper.moveTo(pos - 32);
  while(stepper.distanceToGo() != 0) {
      stepper.run();
  }
  digitalWrite(VALVE_RELAY_PIN, HIGH);
  
  delay(1000);
  stepper.moveTo(pos - 64);
  while(stepper.distanceToGo() != 0) {
      stepper.run();
  }
   delay(1000);
  }

SerialCommand cmd_stepper_plus_(">", cmd_stepper_plus, true);
SerialCommand cmd_stepper_minus_("<", cmd_stepper_minus,true);
SerialCommand cmd_stepper_big_plus_("+", cmd_stepper_big_plus, true);
SerialCommand cmd_stepper_big_minus_("-", cmd_stepper_big_minus,true);
SerialCommand cmd_run_step_("S", cmd_run_step,true);



void setup() {

  
  pinMode(VALVE_RELAY_PIN, OUTPUT); 
  digitalWrite(VALVE_RELAY_PIN,HIGH);
  
  pinMode(CLICK_PIN, INPUT_PULLUP); 
  t0 = millis();
  
  Serial.begin(BAUD);
  serial_commands_.SetDefaultHandler(cmd_unrecognized);
  serial_commands_.AddCommand(&cmd_stepper_plus_);
  serial_commands_.AddCommand(&cmd_stepper_minus_);
  serial_commands_.AddCommand(&cmd_stepper_big_plus_);
  serial_commands_.AddCommand(&cmd_stepper_big_minus_);
  serial_commands_.AddCommand(&cmd_run_step_);
  
  serial_commands_.SetDefaultHandler(&cmd_unrecognized);
  
  stepper.setMaxSpeed(50.0);
  stepper.setAcceleration(10.0);
  stepper.setSpeed(50);
  stepper.moveTo(0);
  
}//--(end setup )---


void loop()
{
  
  int t1 = t0;
  t0 = millis();
  int dt = t0 - t1;
  serial_commands_.ReadSerial();
  if (stepper.distanceToGo() != 0) {
      stepper.run();
      return;
  }
  
  serial_commands_.ReadSerial();
  if(digitalRead(CLICK_PIN) != 1){
    cmd_run_step(&serial_commands_);
  }
   
   if(analogRead(X_PIN) < 64){
    
    cmd_stepper_big_plus(&serial_commands_);
    }
  else if(analogRead(X_PIN) > (1023 - 64)){
    
    cmd_stepper_big_minus(&serial_commands_);
    }    
    
  if(analogRead(Y_PIN) < 64){
    cmd_stepper_minus(&serial_commands_);
    }
  else if(analogRead(Y_PIN) > (1023 - 64)){
    cmd_stepper_plus(&serial_commands_);
    }    

    delay(30);
 }
 
