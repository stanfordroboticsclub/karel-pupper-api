# karel-pupper-api

![Pupper](https://user-images.githubusercontent.com/21105308/144390767-f9bf2737-a8c6-4a9e-b2e7-a1c12ed70820.jpg)

# Description
This repo was developed to make pupper simpler to program. The main features of implemented in this repo are basic movement (moving forward, turning) and access to image frames to do computer vision. The naming conventions and features are modeled after the great CS106A classic, Karel.

# Environment Setup
First, make sure that you have completed the instructions for ssh and internet (https://pupper.readthedocs.io/en/latest/guide/software_installation.html#) and
note what the IP address of the pi is. You will need it to ssh in the future wirelessly.
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
Your karel-pupper code should be contained within the `programs` folder.
On your computer, clone the repo.
```bash
git clone https://github.com/stanfordroboticsclub/karel-pupper-api.git
```
## deploy-folder.sh
```bash
# Run ./deploy-folder.sh within the root repo directory (karel-pupper-api) to push the folder to the pi
./deploy-folder.sh
```
## deploy.sh
```bash
# Run ./deploy.sh within the root repo directory (karel-pupper-api) to push only the programs folder to the pi
./deploy.sh
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
  - [ ] Lidar USB sensor  
  ~~- [ ] Camera getting images~~
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



