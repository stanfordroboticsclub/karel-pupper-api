from StanfordQuadruped.djipupper import Config
import numpy as np
import time
from StanfordQuadruped.src.Controller import Controller
from StanfordQuadruped.src.JoystickInterface import JoystickInterface
from StanfordQuadruped.src.Command import Command
from StanfordQuadruped.src.State import State
from StanfordQuadruped.djipupper import HardwareInterface
from StanfordQuadruped.djipupper.IndividualConfig import SERIAL_PORT  # make the configs more consistent
from StanfordQuadruped.djipupper.Config import Configuration
from StanfordQuadruped.djipupper.Kinematics import four_legs_inverse_kinematics
from StanfordQuadruped.src.Utilities import deadband, clipped_first_order_filter
import argparse
from enum import Enum

import datetime
import os
import msgpack
import cv2
from imutils.video import VideoStream
import imutils

DIRECTORY = "logs/"
FILE_DESCRIPTOR = "walking"
BLURRY_THRESHOLD = 3
EPISLON = 0.1
class BehaviorState(Enum):
        DEACTIVATED = -1
        REST = 0
        TROT = 1
        WALK = 2
class Pupper:      
    def __init__(self, name="pupper", args=None, LOG=False):
        # Eventually have arguments passed in
        # Create config
        self.config = Configuration()
        self.name = name
        
        self.hardware_interface = HardwareInterface.HardwareInterface(port=SERIAL_PORT)
        time.sleep(0.1)
        self.controller = Controller(self.config, four_legs_inverse_kinematics)
        self.state = State(height= -0.05) # self.config.default_z_ref
        self.vs = VideoStream(usePiCamera=0).start()
        self.LOG = LOG
        self.stand_pos = [-0.21014294028282166, 0.8376691341400146, -1.4759116172790527, 
        0.21139997243881226, 0.8433789014816284, -1.4809609651565552, 
        -0.20969551801681519, 0.8478103876113892, -1.49553382396698, 
        0.21148520708084106, 0.8540953993797302, -1.5018829107284546]
        self.STAND_THRESHOLD_MAX = 8
        self.STAND_THRESHOLD_MIN = 4
        self.look_state = "center"
        print(name, "is ready to go!")
    def get_joint_positions(self):
        return self.hardware_interface.get_pos()
    def wakeup(self):
        """Main program"""
        
        last_loop = time.time()
        if self.LOG:
            print("Wokeup.")
        
        self.hardware_interface.serial_handle.reset_input_buffer()
        time.sleep(0.1)

        self.hardware_interface.activate()
        time.sleep(1)
        self.state.activation = 1
        self.slowStand()
        time.sleep(1)
        command = Command(self.config.default_z_ref)
        self.controller.run(self.state, command)
        self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
    '''
    only slow stand from bottom position (clarify what the default position is)
    '''
    def slowStand(self):
        cur = self.state.height # 0
        target = self.config.default_z_ref
        startTime = time.time()
        last_loop = startTime
        command = Command(-0.03)
        while abs(cur) < abs(target):
            if time.time() - last_loop >= self.config.dt:
                command.height = ((time.time() - startTime) / 2) * target - 0.03
                cur = command.height
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()

    def is_blocked(self):
        img = cv2.cvtColor(self.vs.read(), cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(img, cv2.CV_16S)
        mean, stddev = cv2.meanStdDev(lap)
        if stddev[0,0] < BLURRY_THRESHOLD:
            return True
        return False
    
    '''
    The Pupper rests by returning to its sleeping position. It deactivates at the end.
    '''
    def rest(self):
        if self.LOG:
            print("PUPPER IS RESTING")
        self.nap()
        time.sleep(0.1)
        self.hardware_interface.deactivate()
        time.sleep(0.1)
        self.state.activation = 0

    '''
    The Pupper naps but does not deactivate
    '''
    def nap(self):
        cur = self.state.height
        orig = cur
        target = self.config.default_z_ref
        startTime = time.time()
        last_loop = startTime
        command = Command(self.config.default_z_ref)
        while cur <= -0.03: # equal here?
            if time.time() - last_loop >= self.config.dt:
                command.height = orig + ((time.time() - startTime) / 2) * abs(target)
                cur = command.height
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()
    '''
    The Pupper turns left with positive angle. Angle is in radians and speed is in
    radians / s.
    '''
    def turn(self, angle, speed, behavior="trot"):
        if behavior == "trot":
            behavior = BehaviorState.TROT
        elif behavior == "walk":
            behavior = BehaviorState.WALK
        if self.LOG:
            print("TURNING AT", angle, " RADIANS at", speed, " rad/s")
        speed = np.clip(speed, -self.config.max_yaw_rate, self.config.max_yaw_rate)
        target_time = abs(angle) * 2/ abs(speed) 
        speed = np.sign(angle) * speed
        self.turn_for_time(target_time, speed, behavior)

    def getImu(self):
        return self.hardware_interface.get_imu()
    
    # Left increasing yaw
    def turnI(self, angle, speed, behavior=BehaviorState.TROT):
        command = Command(self.config.default_z_ref)
        speed = np.clip(speed, -self.config.max_yaw_rate, self.config.max_yaw_rate)
        start = self.hardware_interface.get_imu()
        speed = np.sign(angle) * speed
        x_vel = 0
        y_vel = 0
        command.horizontal_velocity = np.array([x_vel, y_vel])
        command.yaw_rate = speed
        command.trot_event = True
        if behavior == BehaviorState.WALK:
            command.trot_event = False
            command.walk_event = True
        elif behavior != BehaviorState.TROT:
            print("Can't rest while moving forward")
            return
        startTime = time.time()
        last_loop = startTime
        
        target = start + angle
        sine_dif = abs(np.sin(start) - np.sin(target))
        cos_dif = abs(np.cos(start) - np.cos(target))
        while sine_dif > EPISLON or cos_dif > EPISLON:
            if time.time() - last_loop >= self.config.dt:
                # print(start)
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                start = self.hardware_interface.get_imu()
                sine_dif = abs(np.sin(start) - np.sin(target))
                cos_dif = abs(np.cos(start) - np.cos(target))
                # print(start, target, sine_dif, cos_dif)
                last_loop = time.time()
        # else:
        #     target = start - abs(angle)
        #     command.yaw_rate = -speed
        #     while sine_dif > EPISLON or cos_dif > EPSILON:
        #         self.controller.run(self.state, command)
        #         self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
        #         start = self.hardware_interface.get_imu()
        #         last_loop = time.time()
        command = Command(self.config.default_z_ref)
        command.stand_event = True

        self.controller.run(self.state, command)
        self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
            
        
    def forward(self, distance, speed, behavior="trot"):
        if behavior == "trot":
            behavior = BehaviorState.TROT
        if behavior == "walk":
            behavior = BehaviorState.WALK
        speed = np.clip(speed, -self.config.max_yaw_rate, self.config.max_yaw_rate)
        target_time = abs(distance) / abs(speed) 
        speed = np.sign(distance) * speed
        self.forward_for_time(target_time, speed, behavior)

    '''
    The Pupper can turn for time in seconds (s)
    '''
    def turn_for_time(self, duration, speed, behavior=BehaviorState.TROT):
        command = Command(self.config.default_z_ref)
        speed = np.clip(speed, -self.config.max_yaw_rate, self.config.max_yaw_rate)
        x_vel = 0
        y_vel = 0
        command.horizontal_velocity = np.array([x_vel, y_vel])
        command.yaw_rate = speed
        command.trot_event = True
        if behavior == BehaviorState.WALK:
            command.trot_event = False
            command.walk_event = True
        elif behavior != BehaviorState.TROT:
            print("Can't rest while moving forward")
            return
        startTime = time.time()
        last_loop = startTime
        while (time.time() - startTime < duration):
            if time.time() - last_loop >= self.config.dt:
                # print(time.time() - last_loop)
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()
        command = Command(self.config.default_z_ref)
        command.stand_event = True

        self.controller.run(self.state, command)
        self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)

    '''
    The Pupper moves forward for time in seconds (s) at a specified speed [0, 1]
    '''
    def forward_for_time(self, duration, speed, behavior=BehaviorState.TROT):
        command = Command(self.config.default_z_ref)
        speed = np.clip(speed, -self.config.max_x_velocity, self.config.max_x_velocity)

        x_vel = speed
        y_vel = 0
        command.horizontal_velocity = np.array([x_vel, y_vel])
        command.yaw_rate = 0
        command.trot_event = True
        if behavior == BehaviorState.WALK:
            command.walk_event = True
        elif behavior != BehaviorState.TROT:
            print("Can't rest while moving forward")
            return
        startTime = time.time()
        last_loop = startTime
        while (time.time() - startTime < duration):
            if time.time() - last_loop >= self.config.dt:
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()
        command = Command(self.config.default_z_ref)
        command.stand_event = True

        self.controller.run(self.state, command)
        self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
    
    def move_until_blocked(self, speed, behavior=BehaviorState.TROT):
        command = Command(self.config.default_z_ref)
        speed = np.clip(speed, -self.config.max_x_velocity, self.config.max_x_velocity)
        x_vel = speed
        y_vel = 0
        command.horizontal_velocity = np.array([x_vel, y_vel])
        command.yaw_rate = 0
        command.trot_event = True
        if behavior == BehaviorState.WALK:
            command.walk_event = True
        elif behavior != BehaviorState.TROT:
            print("Can't rest while moving forward")
            return
        startTime = time.time()
        last_loop = startTime
        blocked = False
        loop = 0
        while not blocked:
            if loop % 3 == 0:
                blocked = self.is_blocked()
            if time.time() - last_loop >= self.config.dt - 0.001:
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)                
                last_loop = time.time()
                loop += 1
        command = Command(self.config.default_z_ref)
        command.stand_event = True

        self.controller.run(self.state, command)
        self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
    
    def getImage(self):
        return cv2.flip(imutils.rotate(self.vs.read(), 180), 1)
    def saveImage(self, name):
        print("Saved picture to", "images/" + name)
        cv2.imwrite("images/" + name, self.getImage())
    def slowRest(self):
        cur = self.config.default_z_ref
        orig = cur
        target = self.config.default_z_ref
        startTime = time.time()
        last_loop = startTime
        command = Command(self.config.default_z_ref)
        while cur <= -0.03:
            if time.time() - last_loop >= self.config.dt:
                command.height = orig + ((time.time() - startTime) / 2) * abs(target)
                cur = command.height
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()
    def look_up(self):
        command = Command(self.config.default_z_ref)
        last_loop = time.time()
        going_up = 0
        while True:
            if going_up > 15:
                break
            if time.time() - last_loop >= self.config.dt:
                self.__update_command(command, pitch_rate=2, height_rate=-0.1)
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()
                going_up += 1
    def look_down(self):
        command = Command(self.config.default_z_ref)
        last_loop = time.time()
        going_up = 0
        while True:
            if going_up > 15:
                break
            if time.time() - last_loop >= self.config.dt:
                self.__update_command(command, pitch_rate=-2, height_rate=0.1)
                self.controller.run(self.state, command)
                self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                last_loop = time.time()
                going_up += 1
    def nod(self):
        command = Command(self.config.default_z_ref)
        last_loop = time.time()
        going_up = 0
        while True:
            if going_up > 60:
                break
            if going_up > 30:
                if time.time() - last_loop >= self.config.dt:
                    self.__update_command(command, pitch_rate=-2, height_rate=0.1)
                    self.controller.run(self.state, command)
                    self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                    last_loop = time.time()
                    going_up += 1
            else:
                if time.time() - last_loop >= self.config.dt:
                    self.__update_command(command, pitch_rate=2, height_rate=-0.1)
                    self.controller.run(self.state, command)
                    self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                    last_loop = time.time()
                    going_up += 1
    def look(self, direction="left"):
        command = Command(self.config.default_z_ref)
        last_loop = time.time()
        loop_count = 0
        while True:
            if direction == "left" and self.look_state == "center":
                if loop_count > 20:
                    self.look_state = "left"
                    break
                if time.time() - last_loop >= self.config.dt:
                    self.__update_command(command, yaw_rate=-1)
                    self.controller.run(self.state, command)
                    self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
                    last_loop = time.time()
                    loop_count += 1
           
    '''
    roll - walking at angle
    height - walking shorter
    '''
    def __update_command(self, command, pitch_rate=0, roll_rate=0, height_rate=0, yaw_rate=0):
        message_dt = 1.0 / 20
        pitch = pitch_rate
        deadbanded_pitch = deadband(pitch, self.config.pitch_deadband)
        pitch_rate = clipped_first_order_filter(
            self.state.pitch,
            deadbanded_pitch,
            self.config.max_pitch_rate,
            self.config.pitch_time_constant,
        )
        command.pitch = self.state.pitch + message_dt * pitch_rate

        height_movement = height_rate
        command.height = (
            self.state.height - message_dt * self.config.z_speed * height_movement
        )
        yaw_movement = yaw_rate
        command.yaw = (
            self.state.yaw_rate - message_dt * self.config.max_yaw_rate * yaw_movement
        )
        roll_movement = roll_rate
        command.roll = (
            self.state.roll + message_dt * self.config.roll_speed * roll_movement
        )
    def __del__(self):
        self.slowRest()
        self.rest()
        print(self.name, "going to sleep!")


    
