from time import sleep
from numpy import pi
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
import karelPupper

def main():
    ######################
    # Moving until blocked
    ######################
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    sleep(2)
    myPup.move_until_blocked(0.4)
    sleep(2)
    myPup.nap()

    # ######################
    # # Square
    # ######################
    # myPup = karelPupper.Pupper()
    # myPup.wakeup()
    # sleep(2)
    # for i in range(3):
    #     myPup.turnI(pi/2, 1)
    #     sleep(1)
    #     myPup.forward(0.1, 0.4)
    #     sleep(1)
    # sleep(2)
    # myPup.nap()

    
main()