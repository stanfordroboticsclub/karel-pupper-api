from time import sleep
import karelPupper

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    myPup.forward_for_time(5, 0.2)
    sleep(2)
    #myPup.rest()
main()