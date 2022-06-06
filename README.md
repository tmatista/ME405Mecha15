# ME 405 Mechatronics Pen Plotter Landing Page
#### Authors: Tim Matista, Jason Hu
#### Under the Guidance of: Professor Charlie Refvem, Cal Poly SLO
#### Date: 06/04/2022
#### 

## The Pen Plotter Project Definition
#### The Pen Plotter project was devised to allow teams to create a robotic drawing machine in any creative was possible. The requirements for this project were to create a 2-and-a-half degree of freedom robot that, when fed raw HPGL files, draws out shapes using any means necessary. The term "draw" was free to be interpreted in whatever manner we choose. The two main degrees of freedom are as well free to be chosen to be any motion EXCEPT the cartesian coordinate system. The remaining half degree of freedom is used as an actuator, or pen-up pen-down motion. 
#### All devices also must be able to be ran using benchtop power supplies in the laboratory and include a "Bell and Whistle" to uniquely define this project from any similar project done before. 


## Mecha15's Mechanical Design
#### Team Mecha15 decided to pursue a robot similar to mechanism 94 in the book, "507 Mechanical Movements". The proposed mechanism can be found here: http://507movements.com/mm_094.html
 
#### INSERT A PICTURE OF THE SYSTEM CAD? OR CAD FILES THEMSELVES? OR EVEN STRAIGHT FROM 507 MECH MOVEMENTS?

### The Discs
#### The proposed mechanism 94 operates using two discs, so we laser cut two discs out of HDPE that were donated by the Robotics Club at Cal Poly. The discs can be separated into a radial disc and a spiral disc. Both gears were cut to have a diameter of 14". 
### Spiral Disc
#### The spiral disc was laser cut out of HDPE at 1/4" thickness, it was designed to have an Archimedes spiral cut into it along with a 50 gear teeth on the outer diameter. Three triangular weight-saving shapes were cut into the spiral disc to cut down on inertial load and allow the user to view drawings below.
### Radial Disc
#### The radial disc was cut with a 4.75" radial slot in it to facilitate movement. This slot starts 0.75" away from the exact center of the disc. Circular weight-saving cuts were made in the radial disc to ease inertial load and allow the user to view drawings below. This disc is outfitted with a linear rail along its radial slot to help facilitate the motion of the pen as well as keep it upright. 
### Lazy Susans
#### Two 14" Lazy Susans (LS) were purchased from Amazon at about 17$/each. These LS are mounted between both discs to facilitate the independent movement of the discs. The discs were secured to the LS using hot glue. The LS can be found on Amazon here: https://www.amazon.com/dp/B07PW63B3Q/ref=twister_B09ZTWL4NN?_encoding=UTF8&th=1

## The Motors
### Steppers
#### Two Wantai NEMA 23 motors were chosen for the final design, as these motors are able to produce the torque needed to move both discs independently. These motors are configures in 4-wire bi-polar stepper movement and have 200 counts-per-revolution. These motors are mounted on brackets to elevate them to the desired height. Pinion gears with 15 teeth are attached to the output shafts of the motor and are designed to mesh with the radial and spiral discs gear teeth. 
### Servo
#### A single TowerPro hobby servo motor was selected to control the pen actuation. The motor was dissected and altered for manual control of the internal DC motor and potentiometer. The resistance of the potentiometer changes as the motor spins, and the reistsnace changes the reading of an ADC on the Nucleo. The servo is outfitted with a single cam on its output shaft that physically moves a pen up and down. All of this together allows the Nucleo to sense if the pen has successfuly been raised or lowered.

## The Drivers
#### Both NEMA 23 motors are driven using TMC4210 and TMC2208 driver chips. These chips were selected due to their SPI protocol and silentstepper modes of movement. These chips, along with a capacitor and header pins, were soldered to a prototyping board supplied by Charlie. This board then interfaces with the Shoe-Of-Brian mounted beneath the STM32 Nucleo Microcontroller. An exact pin-out description is as follows: 
# Need To Fix This Table
####      | Motor Driver|    Nucleo   |
####      |   Board Pin |   Board Pin |
####      |-------------|-------------|
####      | EN1         |     C3      |
####      | EN2         |     C2      |
####      | CLK         |     C7      | 
####      | nCS1        |     C0      |
####      | nCS2        |     C4      |
####      | SCK         |     B3      |
####      | MOSI        |     MOSI2   |
####      | MISO        |     MISO2   |

## Firmware
#### The software used to impliment the robot was written in Python, for its under-the-hood libaries make calculations, matrix operations and motor movement fairly easy. The software is split up into (??6??) files:
#### main.py
#### task_motor.py
#### newtonraphson.py
#### tmc4210driver.py
#### filereader.py

### filereader.py
#### This file takes in a raw .hpgl file, parses it, then saves each X, Y, and command coordinate to a .txt file. The command coordinate is simply either a 0 or a 1 corresponding to pen up/pen down respectively. This is done by seperating the .hpgl file at every semicolon, denoting different operations, and then by commas, denoting x and y coordinates. This file will also determine if the distance between two points is greater than a set threshold and interpolates between points as needed. This file will also determine if the requested point is within the workspace that the plotter can reach and adjust points if they are not possible to draw. This file runs as a pre-processing procedure before any finite state machine is created. (BEFORE TASKS START RUNNING?)

### tmc4210driver.py
#### This file is used to instantiate the TMC4210 chip for motor control. It also defines any methods that are used by the task_motor file such as SPI.send_recv, bytearray decoders, or bytearray translators. (EXPLAIN WHAT THE METHODS ACTUALLY DO)

### task_motor.py
#### This file initiates each motor object by sending the correct byte arrays to their respective registers, setting the values of P_MUL, P_DIV, A_MAX, pulse_div, and ramp_div. A table containing these parameters is listed below. 
####  |  Variable  |   Value    |
####  |-------------------------|
####  | A_MAX      |
####  | pulse_div  |
####  | ramp_div   |
####  | P_MUL      |
####  | P_DIV      |

### newtonraphson.py
#### The Newton Raphson file uses the newton raphson method of finding the roots of a non-linear equation to converge on values of theta for the motors. Hand calculations of the Newton Raphson process are attached below. 

### main.py
#### The main file is responsible for scheduling and instantiating the tasks that run all the files described above. We opted with a round-robin scheduling instead of a priority scheduling technique. The scheduling for the running of each task is outlined in the table below. 
####
####  Task Name  |  Period (ms)
#### |-----------|-------------|
#### | 
####
####
####
####

## Difficulties
### Software
#### 100k vs 1M in the SPI. pmul/pdiv (WRITE ABOUT THESE)
### Hardware
#### This project was fraught with hardware difficulties, most stemming from the motors used for the project. Firstly, the provided (part number) motors did not have the torque required to spin the lazy susan bearings. These motors were replaced with (part number) NEMA (number) stepper motors from the Cal Poly Robotics Club. Unfortunately, one of these replacement motors has a shorting problem when the wires are moved. With much difficulty, this has successfuly been mitigated.

## Features
#### Test test

## Bell-and-Whistle: Live Plotting
#### The additional feature added to our system is a live plotting system that uses UART to communicate drawing progress from the Nucleo to the computer. (ADD PICTURE HERE)

## Operation (SHOULD I ALSO INCLUDE A SECTION ON HOW THE WIRES AND THINGS CONNECT?)
#### To run the systme, start by saving a drawing as "(PUT NAME HERE).hpgl" to the Nucleo. Next, move the motors so that the gears are **not** meshed with the disks. This is important because the motors automatically move to their "home" position which may not be what you expect it to be. Next, ensure that the pen is in the raised position. If it isn't this can be manually adjusted by running the "(FILENAME).py". Slide a piece of paper under the disks, switch on both power supplies and soft reboot the Nucleo by pressing ctrl+D. The code will report when it has finished parsing your drawing into usable code and the motors may start moving to their home location. When all of this has finished, move the gears into place to mesh with the disks, and press any key to coninue.
