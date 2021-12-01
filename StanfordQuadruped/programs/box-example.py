from time import sleep
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from numpy import pi
import karelPupper

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()
    for i in range(4):
        myPup.forward(0.5, 0.4)
        myPup.turn(pi/2, 0.4)
    myPup.nap()
main()