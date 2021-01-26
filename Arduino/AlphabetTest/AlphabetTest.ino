// Fingers 1-5 are represented by servo numbers 1-5 (the thumb is finger 5) 

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver servoDriver = Adafruit_PWMServoDriver();
Adafruit_MotorShield motorShield(0x60); 

Adafruit_StepperMotor *stepper1 = motorShield.getStepper(200, 1);
Adafruit_StepperMotor *stepper2 = motorShield.getStepper(200, 2);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. 
#define SERVOMIN  150 // The 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // The 'maximum' pulse length count (out of 4096)
#define USMIN  600 // The rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // The rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 60 // Analog servos run at ~60 Hz updates
#define STEPPER_SPEED 10 // The default stepper motor speed (rpm) 

void setup() {
  while (!Serial);
  Serial.begin(9600);           
  Serial.println("Hello");

  motorShield.begin(); 
  servoDriver.begin();

  stepper1->setSpeed(STEPPER_SPEED);
  stepper2->setSpeed(STEPPER_SPEED);
  
  // In theory the internal oscillator is 25MHz but it really isn't
  // that precise. You can 'calibrate' by tweaking this number till
  // you get the frequency you're expecting!
  servoDriver.setOscillatorFrequency(27000000);  // The int.osc. is closer to 27MHz  
  servoDriver.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~60 Hz updates

  delay(10);

  normalizePosition(); 
}

// Specified finger is fully bent
void bend(uint8_t servonum) { 
  Serial.println(servonum);
  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) {
    servoDriver.setPWM(servonum, 0, pulselen);
  }

  delay(500);
  for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
    servoDriver.setPWM(servonum, 0, pulselen);
  }
}

// Specified finger is slightly bent
void curl(uint8_t servonum) { 
  Serial.println(servonum);
  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) {
    servoDriver.setPWM(servonum, 0, pulselen);
  }

  delay(500);
  for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
    servoDriver.setPWM(servonum, 0, pulselen);
  }
}

void normalizePosition() { 
  
}

void swingThumb() { 
  
}

void curlWrist() { 
  
}

void bendWrist() { 
  
}

void rotateLeft() { 
  
}

void rotateRight() { 
  
}

void parseChar(char c) { 
  switch(c) { 
    case 'a' : 
      bend(1); bend(2); bend(3); bend(4); 
      break; 
    case 'b' : 
      bend(5); 
      break; 
    case 'c' : 
      curl(1); curl(2); curl(3); curl(4); curl(5); 
      break;
    case 'd' : 
      bend(2); bend(3); bend(4); bend(5); 
      break;
    case 'e' : 
      break;
    case 'f' : 
      break;
    case 'g' : 
      break;
    case 'h' :
      break;
    case 'i' :
      break;
    case 'j' : 
      break;
    case 'k' : 
      break;
    case 'l' :
      break;
    case 'm' : 
      break;
    case 'n' :
      break;
    case 'o' :
      break;
    case 'p' :
      break;
    case 'q' : 
      break;
    case 'r' :
      break;
    case 's' : 
      break;
    case 't' :
      break;
    case 'u' :
      break;
    case 'v' :
      break;
    case 'w' :
      break;
    case 'x' :
      break;    
    case 'y' :
      break; 
    case 'z' :
      break;       
    case ' ' : 
      delay(500); 
      break;   
  }
  delay(500); 
  normalizePosition(); 
}

void loop() {
  if(Serial.available() > 0) { 
    parseChar(Serial.read());
  }
}
