from time import sleep
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from numpy import pi
import karelPupper

def main():
    myPup = karelPupper.Pupper()
    myPup.wakeup()

main()