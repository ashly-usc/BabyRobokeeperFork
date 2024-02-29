// include the library code:
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

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.print("Hi");
  // initialize the serial communications:
  Serial.begin(9600);
}

void loop() {
  // when characters arrive over the serial port...
  if (Serial.available()>0) {
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    lcd.clear();
    // read all the available characters
    char c = "";
    String longer = "";
    while (Serial.available() > 0) {
      // display each character to the LCD
      c = Serial.read();
      if(c != '\n'){
        lcd.write(c);
        longer += c;
      }
    }

    Serial.print("RECIEVED: ");
    Serial.println(longer);
    double goal = longer.toDouble();
    
    double dist = abs(current-goal);

    // Serial.print("a");
    if (MIN <= goal && goal <= MAX){
      // Serial.print("b");
      if (current < goal){
        stepper.move(-(dist*(double(STEPS)/length))); // !!!want to remeasure width
        current += dist;
        // Serial.print("c");
      } else if (current > goal){
        stepper.move((dist*(double(STEPS)/length)));
        current -= dist;
        // Serial.print("d");
      } else {
        stepper.move(0);
        // Serial.print("e");
      }
      // Serial.print("f");
    }
    // Serial.print("g");
  }
}
