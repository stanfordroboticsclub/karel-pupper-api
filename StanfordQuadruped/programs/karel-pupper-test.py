from time import sleep
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
import karelPupper
import cv2

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    sleep(2)
    # myPup.slowStand()
    # sleep(2)
    # myPup.nap()    
    # sleep(2)
    # myPup.rest()
    
    #myPup.wakeup()
    # sleep(2)
    # myPup.turn(3/4, 0.12)
    # sleep(2)
    # myPup.turn(-3/4, 0.12)
    #sleep(1)
    # myPup.forward_for_time(5, 0.3)
    # sleep(3)
    myPup.move_until_blocked(0.4)
    # myPup.turn_for_time(3, 0.2, karelPupper.BehaviorState.TROT)
    # myPup.forward_for_time(3, 0.2, karelPupper.BehaviorState.WALK)
    #sleep(2)
    myPup.nap()
main()