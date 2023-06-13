from time import sleep
import time
import sys, os
import numpy as np

def main():
    myPup = Pupper(name="Pup")
    myPup.rest()

if __name__ == '__main__' and __package__ is None:    
    sys.path.append(os.path.abspath(os.path.join('..')))
    from karelPupper import Pupper
    main()
