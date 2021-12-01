from time import sleep
import time
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
import karelPupper
import cv2

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    sleep(1)
    # myPup.slowStand()
    # sleep(2)
    # myPup.nap()    
    # sleep(2)
    # myPup.rest()
    # myPup.turnI(3/2, 0.4)
    #myPup.turn_for_time(2, 0.4)
    
    st = time.time()
    start = myPup.getImu()
    print("took", time.time() - st)
    while myPup.getImu() > start - 3/2:
        print(myPup.getImu())
        sleep(0.1)
    print("done")
    sleep(3)
    #myPup.turnI(-3/2, 0.4)
    #myPup.wakeup()
    # sleep(2)
    # myPup.turn(3/4, 0.12)
    # sleep(2)
    # myPup.turn(-3/4, 0.12)
    #sleep(1)
    # myPup.forward_for_time(5, 0.3)
    # sleep(3)
    # myPup.move_until_blocked(0.4)
    # myPup.turn_for_time(3, 0.2, karelPupper.BehaviorState.TROT)
    # myPup.forward_for_time(3, 0.2, karelPupper.BehaviorState.WALK)
    #sleep(2)
    myPup.nap()
main()