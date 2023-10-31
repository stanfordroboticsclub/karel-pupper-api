import cv2
from time import sleep
import sys, os
from numpy import pi

def main():
    ############################
    # Pupper Captures the Moment
    ############################
    myPup = karelPupper.Pupper("Coco")
    myPup.wakeup()

    myPup.turn(pi/4, 1, "trot")
    myPup.look_up()
    sleep(1)
    myPup.saveImage("left.jpg")

    myPup.turn(-pi/4, 1, "trot")
    myPup.look_up()
    sleep(1)
    myPup.saveImage("middle.jpg")

    myPup.turn(-pi/4, 1, "trot")
    myPup.look_up()
    sleep(1)
    myPup.saveImage("right.jpg")
    myPup.look_down()

    sleep(1)
        














if __name__ == '__main__' and __package__ is None:    
    sys.path.append(os.path.abspath(os.path.join('..')))
    import karelPupper
    main()