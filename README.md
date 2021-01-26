# ASLRoboticHand

## Inspiration ##
Hiring a sign language translator to translate between ASL and English can be cost prohibitive for many places and thus many people who speak ASL are not able to get the support they need everywhere they go. We wanted to create an inexpensive translation system between ASL and English so that ASL translation could be more widely available. 

## What It Does ##
We created a robotic hand that can perform the sign language alphabet by taking in input text from a computer. A Leap Motion sensor takes in hand position and movement to translate ASL to English. 

## How It Works ##
THe robot hand uses torsion springs that allows the fingers of the hand to be striaght. The strings are connected to the base of the string using strings connected to servo motors. These motors pull the strings and thus the fingers of the hands down and to the left and the right, allowing for movement of the hand. The exoskeleton of the hand will be 3D printed using PLA filament. The hand will rest on a laser cut box which will contain the arduino and the motors.  

The Leap motion sensor takes in position and movement information about the hand. We then transformed the data to calculate consecutive fingertip distances, finger bend angle, and knuckle slope. We used Linear Discriminant Analysis to recognize the sign the user was creating.  

## How To Use It ##
If you wish to train the model, you can email me for the data we created. It is too large to include in the Github repository. The parts for the hand as well as links to where we purchased them are listed in the Proposal section of the document. 

## Built With ##
- [Sklearn](https://scikit-learn.org/stable/)
- [Leap Motion Controller](https://www.ultraleap.com/product/leap-motion-controller/)
