from djipupper import Config
import numpy as np
import time
from src.Controller import Controller
from src.JoystickInterface import JoystickInterface
from src.Command import Command
from src.State import State
from djipupper import HardwareInterface
from djipupper.IndividualConfig import SERIAL_PORT  # make the configs more consistent
from djipupper.Config import Configuration
from djipupper.Kinematics import four_legs_inverse_kinematics
from src.Utilities import deadband, clipped_first_order_filter
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

class BehaviorState(Enum):
    DEACTIVATED = -1
    REST = 0
    TROT = 1
    WALK = 2
# TODO: figure out how to know if you are left standing or resting
class Pupper:      

    # if __name__ == "__main__":
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("--zero", help="zero the motors", action="store_true")
    #     parser.add_argument("--log", help="log pupper data to file", action="store_true")
    #     parser.add_argument("--home", help="home the motors (moves the legs)", action="store_true")
    #     FLAGS = parser.parse_args()
    #     main(FLAGS)
    def __init__(self, args=None, LOG=False):
        # Eventually have arguments passed in
        # Create config
        self.config = Configuration()
        self.hardware_interface = HardwareInterface.HardwareInterface(port=SERIAL_PORT)
        time.sleep(0.1)
        self.controller = Controller(self.config, four_legs_inverse_kinematics)
        self.state = State(height= -0.05) # self.config.default_z_ref
        self.input_curve = lambda x: np.sign(x) * min(x ** 2, 1)
        self.vs = VideoStream(usePiCamera=0).start()
        self.LOG = LOG
    def wakeup(self):
        """Main program"""

        # Print summary of configuration to console for tuning purposes
        # print("Summary of gait parameters:")
        # print("overlap time: ", self.config.overlap_time)
        # print("swing time: ", self.config.swing_time)
        # print("z clearance: ", self.config.z_clearance)
        # print("default height: ", self.config.default_z_ref)
        # print("x shift: ", self.config.x_shift)

        # if FLAGS.log:
        #     today_string = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        #     filename = os.path.join(
        #         DIRECTORY, FILE_DESCRIPTOR + "_" + today_string + ".csv"
        #     )
        #     log_file = open(filename, "w")
        #     hardware_interface.write_logfile_header(log_file)

        # if FLAGS.zero:
        #     hardware_interface.set_joint_space_parameters(0, 4.0, 4.0)
        #     hardware_interface.set_actuator_postions(np.zeros((3,4)))
        #     input(
        #         "Do you REALLY want to calibrate? Press enter to continue or ctrl-c to quit."
        #     )
        #     print("Zeroing motors...", end="")
        #     hardware_interface.zero_motors()
        #     hardware_interface.set_max_current_from_file()
        #     print("Done.")
        # else:
        #     print("Not zeroing motors!")

        # if FLAGS.home:
        #     print("Homing motors...", end="", flush=True)
        #     hardware_interface.home_motors()        
        #     time.sleep(5)
        #     print("Done.")
            
        # print("Waiting for L1 to activate robot.")

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
        #     while True:
        #         if state.activation == 0:
        #             time.sleep(0.02)
        #             command = Command()
        #             if command.activate_event == 1:
        #                 print("Robot activated.")
        #                 time.sleep(0.1)
        #                 hardware_interface.serial_handle.reset_input_buffer()
        #                 time.sleep(0.1)
        #                 hardware_interface.activate()
        #                 time.sleep(0.1)
        #                 state.activation = 1
        #                 continue
        #         elif state.activation == 1:
        #             now = time.time()
        #             if FLAGS.log:
        #                 any_data = hardware_interface.log_incoming_data(log_file)
        #                 if any_data:
        #                     print(any_data['ts'])
        #             if now - last_loop >= config.dt:
        #                 command = joystick_interface.get_command(state)
        #                 if command.deactivate_event == 1:
        #                     print("Deactivating Robot")
        #                     print("Waiting for L1 to activate robot.")
        #                     time.sleep(0.1)
        #                     hardware_interface.deactivate()
        #                     time.sleep(0.1)
        #                     state.activation = 0
        #                     continue
        #                 controller.run(state, command)
        #                 hardware_interface.set_cartesian_positions(
        #                     state.final_foot_locations
        #                 )
        #                 last_loop = now
        # except KeyboardInterrupt:
        #     if FLAGS.log:
        #         print("Closing log file")
        #         log_file.close()
    '''
    only slow stand from bottom position (clarify what the default position is)
    '''
    def slowStand(self):
        print(self.state.height)
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
        #print(stddev[0, 0])
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
    def turn(self, angle, speed, behavior=BehaviorState.TROT):
        if self.LOG:
            print("TURNING AT", angle, " RADIANS at", speed, " rad/s")
        speed = np.clip(speed, -self.config.max_yaw_rate, self.config.max_yaw_rate)
        target_time = abs(angle) / abs(speed) 
        speed = np.sign(angle) * speed
        self.turn_for_time(target_time, speed, behavior)
        

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
        while not blocked:
            # if time.time() - last_loop >= self.config.dt - 0.001:
            self.controller.run(self.state, command)
            self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
            last_loop = time.time()
            blocked = self.is_blocked()
            # print(last_loop - time.time())
        command = Command(self.config.default_z_ref)
        command.stand_event = True

        self.controller.run(self.state, command)
        self.hardware_interface.set_cartesian_positions(self.state.final_foot_locations)
    
    def getImage(self):
        return cv2.flip(imutils.rotate(self.vs.read(), 180), 1)
    
    

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
    '''
    roll - walking at angle
    height - walking shorter
    '''
    def __update_command(self, command):
        message_dt = 1.0 / 20
        pitch = 0
        deadbanded_pitch = deadband(pitch, self.config.pitch_deadband)
        pitch_rate = clipped_first_order_filter(
            self.state.pitch,
            deadbanded_pitch,
            self.config.max_pitch_rate,
            self.config.pitch_time_constant,
        )
        command.pitch = self.state.pitch + message_dt * pitch_rate

        height_movement = 0
        command.height = (
            self.state.height - message_dt * self.config.z_speed * height_movement
        )

        roll_movement = 0
        command.roll = (
            self.state.roll + message_dt * self.config.roll_speed * roll_movement
        )


    
