#led_ctrl_test
import RPi.GPIO as GPIO
import time

# LED GPIO for Traffic Signals
rLED = 25
yLED = 8
gLED = 7

norm_cycle = [rLED, yLED, gLED]
alt_cycle = [rLED, gLED]
err_cycle = [rLED]

cycle_mode = 0

GPIO.setmode(GPIO.BCM)
for x in norm_cycle:
    GPIO.setup(x, GPIO.OUT)
    GPIO.output(x, GPIO.LOW)

try:
    while True:

        cycle_mode = int(input("Enter the input: ") or cycle_mode)

        if cycle_mode == 1:
            for x in norm_cycle:
                GPIO.output(x, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(x, GPIO.LOW)
        elif cycle_mode == 2:
            for x in alt_cycle:
                GPIO.output(x, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(x, GPIO.LOW)
        else:
            GPIO.output(rLED, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(rLED, GPIO.LOW)

except KeyboardInterrupt:
    for x in norm_cycle:
        GPIO.output(x, GPIO.LOW)
    GPIO.cleanup()
    print("\n")
    pass
