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
- [ ] Milestone 3 (Advanced Control and Design)
  - [ ] Stream Camera feed
  - [ ] Lidar USB sensor  
  - [ ] Camera getting images
  - [ ] Is blocked routine
  - [ ] Turn on radius
  - [ ] Move for distance
  - [ ] Advanced Maneuvers
  - [ ] Rolling over
  - [ ] Recovery
  - [ ] Dancing
- [ ] Milestone 4 (Examples and Documentation)
  - [ ] Square
  - [ ] 180 degree turns
  - [ ] Camera Usage
  - [ ] Camera isBlocked / Color detections
  - [ ] Maze   
