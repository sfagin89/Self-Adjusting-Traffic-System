import RPi.GPIO as GPIO
import time

# LED GPIO for Traffic Signals
rLED = 25
yLED = 8
gLED = 7

norm_cycle = [rLED, yLED, gLED]
alt_cycle = [rLED, gLED]

rCount = 0 # Total Object Count of Remote Node
lCount = 0 # Total Object Count of Local Node

# Algorithm:
# Two Intersections
# Normal behavior, both cycle through norm_cycle
# Altered behavior
## If one node is significantly different than the other (difference greater
## than 2?) then whichever (either/both) node is above/below set threshold
## will begin using the alt_cycle

try:
    while True:
        try:
            with open('rcv_file.txt') as f:
                rCount = f.read()
        except:
            print("Failed to read file")
            continue
except KeyboardInterrupt:
    print("\n")
    pass
