from time import sleep
import karelPupper

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    sleep(2)
    myPup.turn(3/2, 0.2)
    sleep(2)
    myPup.turn(-3/2, 0.2)
    # myPup.turn_for_time(3, 0.2, karelPupper.BehaviorState.TROT)
    # myPup.forward_for_time(3, 0.2, karelPupper.BehaviorState.WALK)
    sleep(2)
    #myPup.rest()
main()