# ME 405 Mechatronics Pen Plotter Landing Page
#### Authors: Tim Matista, Jason Hu
#### Under the Guidance of: Professor Charlie Refvem, Cal Poly SLO

## The Pen Plotter Project Definition
#### The Pen Plotter project was devised to allow teams to create a robotic drawing machine in any creative was possible. The requirements for this project were to create a 2-and-a-half degree of freedom robot that, when fed raw HPGL files, draws out shapes using any means necessary. The term "draw" was free to be interpreted in whatever manner we choose. The two main degrees of freedom are as well free to be chosen to be any motion EXCEPT the cartesian coordinate system. The remaining half degree of freedom is used as an actuator, or pen-up pen-down motion. 
#### All devices also must be able to be ran using benchtop power supplies in the laboratory. 
#### Team Mecha15 decided to pursue a robot similar to mechanism 94 in the book, "507 Mechanical Movements". The proposed mechanism can be found here: http://507movements.com/mm_094.html

## Mecha15's Mechanical Design
## The Discs
#### The proposed mechanism 94 operates using two discs, so we laser cut two discs out of HDPE that were donated by the Robotics Club at Cal Poly. The discs can be separated into a radial disc and a spiral disc. Both gears were cut to have a diameter of 14". 
### Spiral Disc
#### The spiral disc was laser cut out of HDPE at 1/4" thickness, it was designed to have an Archimedes spiral cut into it along with a 50 gear teeth on the outer diameter. Three triangular weight-saving shapes were cut into the spiral disc to cut down on inertial load and allow the user to view drawings below.
### Radial Disc
#### The radial disc was cut with a 4.75" radial slot in it to facilitate movement. This slot starts 0.75" away from the exact center of the disc. Circular weight-saving cuts were made in the radial disc to ease inertial load and allow the user to view drawings below.
### Lazy Susans
#### Two 14" Lazy Susans (LS) were purchased from Amazon at about 15$/each. These LS are mounted between both discs to facilitate the independent movement of the discs. The discs were secured to the LS using hot glue.

## The Motors
#### Two Wantai NEMA 23 motors were chosen for the final design, as these motors are able to produce the torque needed to move both discs independently. These motors are configures in 4-wire bi-polar stepper movement and have 200 counts-per-revolution. These motors are mounted on brackets to elevate them to the desired height. Pinion gears with 15 teeth are attached to the output shafts of the motor and are designed to mesh with the radial and spiral discs gear teeth. 
