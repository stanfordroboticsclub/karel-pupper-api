# karel-pupper-api
<p align="center">
  <img src="https://user-images.githubusercontent.com/21105308/144390767-f9bf2737-a8c6-4a9e-b2e7-a1c12ed70820.jpg" alt="Pupper" width="800"/>
</p>

# Description
This repo was developed to make pupper simpler to program. The main features of implemented in this repo are basic movement (moving forward, turning) and access to image frames to do computer vision. The naming conventions and features are modeled after the great CS106A classic, Karel.

# Approach
- Focusing on user ease-of-use and scalability
- Providing predictable and understandable commands and controls
- Allowing easy deployment and development workflow
- Building off of existing StanfordQuadruped repo, replacing JoyStick interface with karel-pupper commands


# Environment Setup
First, make sure that you have completed the instructions for ssh and internet (https://pupper.readthedocs.io/en/latest/guide/software_installation.html#) and
note what the IP address of the pi is. You will need it to ssh in the future wirelessly.

## Saving the PI address to your computer
Type these commands and replace it with the IP address of your pi in the terminal you are using. This will
save your ip address and update the terminal to save your variable for future
runs.
```bash
export pi=put.address.here
source ~/.bashrc
```
# Installation
## Alternative way to add SSH key to pi
```bash
# Run this in your personal computer terminal to generate an ssh key
# When it asks for what file to put it in, notate what that path is
ssh-keygen
# This will copy the ssh file from the path specified to the pi
ssh-copy-id -i (filepath) pi@IP.ADDRESS
```
*Note: Also make sure SSH and the webcam are enabled on the pi (https://phoenixnap.com/kb/enable-ssh-raspberry-pi)*

# Installing the repo
Write all of your karel-pupper code within the `programs` folder.
On your computer, clone the repo.
```bash
git clone https://github.com/stanfordroboticsclub/karel-pupper-api.git
```
Then, run this command to push the repository to the pi through ssh.
```bash
./deploy-first-time.sh
```
## run.sh
```bash
# Run ./run.sh within the root repo directory (karel-pupper-api) to push only the programs folder to the pi and run the program on pupper
./run.sh 
# You can specify what specific program you want to run as an argument
./run.sh my_program.py
```
## reset.sh
```bash
# Run ./reset.sh within the root repo directory (karel-pupper-api) to deactivate the pupper from any position
./reset.sh 
```
## deploy.sh
```bash
# Run ./deploy.sh within the root repo directory (karel-pupper-api) to push only the programs folder to the pi
./deploy.sh
```
## Usage
Importing karelPupper class
```python
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
import karelPupper
```
Initialize Pupper object and configuration
```python
myPup = karelPupper.Pupper()
```
Waking up pupper (activate)
```python
myPup.wakeup()
```
https://user-images.githubusercontent.com/21105308/144733202-af8c7995-d686-4817-b3bf-b51f17d40a59.mov


Resting up pupper (deactivate)
```python
myPup.rest()
```
https://user-images.githubusercontent.com/21105308/144733176-4d11b253-b27f-4fe0-9c9b-71878fb0d2b7.mov

Turning pupper with IMU
```python
myPup.turnI(-np.pi / 2, 1.2)
```
https://user-images.githubusercontent.com/21105308/144733345-50a5e163-2a14-4f63-91c3-5e9b99b90c20.mov

Move until blocked
```python
myPup.move_until_blocked(0.4)
```
https://user-images.githubusercontent.com/21105308/144733439-99dc2021-1cb7-4842-9a65-d3af0fd861a8.mov

Getting image
```python
myPup.getImage()
```

Getting IMU yaw angle (turning angle)
```python
myPup.getImu()
```

Forward
```python
myPup.forward(distance, speed, behavior=BehaviorState.TROT)
```

nap (rests without deactivating)
```python
myPup.nap()
```

<!-- ROADMAP -->
## Roadmap

- [x] Milestone 1 (Setup)
  - [x] API Structure and Design!
  - [x] Plan for High-level -> Low-level design
- [x] Milestone 2 (Basic Control)
  - [x] Turning for specified angle
  - [x] Moving Different Speeds
  - [x] Moving Different Gaits
  - [x] Standing up routine
  - [x] Stopping routine
- [x] Milestone 3 (Advanced Control and Design)
  - [x] Stream Camera feed
  ~~- [ ] Lidar USB sensor 
  - [x] Camera getting images
  - [x] Is blocked routine
  - [ ] Turn on radius
  - [x] Move for distance
  - [ ] Advanced Maneuvers
  - [ ] Rolling over
  - [x] Recovery
  - [ ] Dancing
- [x] Milestone 4 (Examples and Documentation)
  - [x] Square
  - [ ] 180 degree turns
  - [x] Camera Usage
  - [x] Camera isBlocked / Color detections
  - [ ] Maze   

# Reflections
Working and debugging on physical system was hard! Often, simple features to implement were not that simple, and we spent a lot of time on setting up our environment. Getting ssh, wifi, and deployment to work were hurdles that we had to overcome to do testing. This, among other issues like Pupper breaking itself, clicking its own configuration buttons, wires getting caught, power plug slightly being unplugged, motors spazzing out due to loop rate issues, and more. Our approach was to use Karel commands as inspiration, but an alternative would be to build one general movement command with a lot of parameters and provide getters to images and sensors for the user to use. This would be more for advanced users, and the usability of our code might be less accessible. Future directions include adding more functionality for moving, adding capability to control multiple puppers from one program, and interfacing with simulation. We've learned so many things from how the low-level control of Pupper works as well as how to implement scalable commands for all types of experienced programmers. Pupper was so much fun to work with and we look forward to what comes next!

TODO: Put programs folder inside of the main karel-pupper-api folder and create setup script to allow importing of parent directories

