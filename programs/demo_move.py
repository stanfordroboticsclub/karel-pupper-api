from time import sleep
import sys, os


def main():
    #########################
    # Sniffing nearest object
    #########################
    myPup = Pupper()
    myPup.wakeup()
    sleep(2)
    myPup.move_until_blocked(0.3)
    myPup.nod()
    myPup.nod()
    sleep(2)

















if __name__ == '__main__' and __package__ is None:    
    sys.path.append(os.path.abspath(os.path.join('..')))
    from karelPupper import Pupper
    main()