#include <Arduino.h>
#include <Stepper.h>
#include <LiquidCrystal.h> 

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
// Target RPM for cruise speed
#define RPM 1300
// Acceleration and deceleration values are always in FULL steps / s^2
#define MOTOR_ACCEL 16000
#define MOTOR_DECEL 16000
// Microstepping mode. If you hardwired it to save pins, set to the same value here.
#define MICROSTEPS 1
#define DIR 8
#define STEP 9

#include "A4988.h"
A4988 stepper(MOTOR_STEPS, DIR, STEP);
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// Current position (measured from origin)
double current = 182; // !!! remeasure width to make sure values are correct 

// Boundaries of the linear gantry
double MAX = 182; //!!! what is the max positive x-coord (ask enrique)
double MIN = -182;

// Calibration:
double STEPS = 1218; // # steps to move across table
double length = 364; // this is in mm (can convert to 36.4 based on Enrique's code)

// New position to move to (measured from origin)
double goal = 0;

void setup() {
  stepper.begin(RPM, MICROSTEPS);
  // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
  // stepper.setEnableActiveState(LOW);
  stepper.enable();
  stepper.setSpeedProfile(stepper.LINEAR_SPEED, MOTOR_ACCEL, MOTOR_DECEL);
  // initialize the serial port:
  Serial.begin(9600);

  lcd.begin(16, 2);            // set the lcd type: 16-character by 2-lines
  lcd.print("Hi");
}

void loop() {

  if (Serial.available() > 0){

    double goal = Serial.readStringUntil('\n').toDouble();

    Serial.print("RECIEVED: ");
    Serial.println(goal);
    
    // Net distance to move 
    double dist = abs(current-goal);

    if (MIN <= goal && goal <= MAX){
      if (current < goal){
        stepper.move(-(dist*(double(STEPS)/length))); // !!!want to remeasure width
        current += dist;
      } else if (current > goal){
        stepper.move((dist*(double(STEPS)/length)));
        current -= dist;
      } else {
        stepper.move(0);
      }
    }
    lcd.clear();
    // read all the available characters
    while (Serial.available() > 0) {
      // display each character to the LCD
      lcd.write(Serial.read());
    }
  }
}
