from time import sleep
from numpy import pi
import sys, os

def main():
    ############################
    ### Pupper chases its tail
    ############################
    myPup = Pupper(name="Coco")
    myPup.wakeup()
    sleep(2)
    for i in range(4):
        myPup.turn(pi/2, 1, "trot")
        sleep(1)
        myPup.forward(0.4, 0.2)
        sleep(1)
    sleep(1)

    










if __name__ == '__main__' and __package__ is None:    
    sys.path.append(os.path.abspath(os.path.join('..')))
    from karelPupper import Pupper
    main()