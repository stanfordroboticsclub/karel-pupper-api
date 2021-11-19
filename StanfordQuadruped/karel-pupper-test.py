from time import sleep
import karelPupper
import cv2

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    # sleep(2)
    # myPup.turn(3/4, 0.12)
    # sleep(2)
    # myPup.turn(-3/4, 0.12)
    sleep(1)
    #myPup.forward_for_time(10, 0.2)
    im = myPup.getImage()
    cv2.imwrite('/home/pi/karelPupper/test_images/test.png', im)
    # myPup.turn_for_time(3, 0.2, karelPupper.BehaviorState.TROT)
    # myPup.forward_for_time(3, 0.2, karelPupper.BehaviorState.WALK)
    sleep(2)
    #myPup.rest()
main()