#multiproc_test
import RPi.GPIO as GPIO
import time
import multiprocessing
#from multiprocessing import Process, Queue, Pool
from queue import Queue

manager = multiprocessing.Manager()
shared_queue = manager.Queue()

rLED = 25
yLED = 8
gLED = 7


def flash_led():
    norm_queue = Queue()
    norm_queue.put(rLED)
    norm_queue.put(yLED)
    norm_queue.put(gLED)

    alt_queue = Queue()
    alt_queue.put(rLED)
    alt_queue.put(gLED)

    err_queue = Queue()
    err_queue.put(rLED)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rLED, GPIO.OUT)
    GPIO.setup(yLED, GPIO.OUT)
    GPIO.setup(gLED, GPIO.OUT)
    GPIO.output(rLED, GPIO.LOW)
    GPIO.output(yLED, GPIO.LOW)
    GPIO.output(gLED, GPIO.LOW)

    mode = 0
    time.sleep(1)
    try:
        while True:
            if not shared_queue.empty():
                mode = shared_queue.get()
                #making norm_queue is reset when mode changes
                temp = norm_queue.get()
                if temp != gLED:
                    norm_queue.put(temp)
                    temp = norm_queue.get()
                    if temp != gLED:
                        norm_queue.put(temp)
                        temp = norm_queue.get()
                norm_queue.put(temp)
                #making alt_queue is reset when mode changes
                temp = alt_queue.get()
                if temp != gLED:
                    alt_queue.put(temp)
                    temp = alt_queue.get()
                alt_queue.put(temp)



            if mode == 1:
                led = norm_queue.get()
                norm_queue.put(led)
            elif mode == 2:
                led = alt_queue.get()
                alt_queue.put(led)
            else:
                led = err_queue.get()
                err_queue.put(led)

            GPIO.output(led, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led, GPIO.LOW)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        #print("\nflash_led exiting\n")
        pass

def ctrl_led():
    try:
        while True:
            shared_queue.put(1)
            time.sleep(10)
            shared_queue.put(2)
            time.sleep(10)
            shared_queue.put(0)
            time.sleep(10)
    except KeyboardInterrupt:
        #print("ctrl_led exiting\n")
        pass

def main():
    try:
        first = multiprocessing.Process(target=ctrl_led, args=())
        second = multiprocessing.Process(target=flash_led, args=())
        first.start()
        second.start()
        first.join()
        second.join()
    except KeyboardInterrupt:
        #print("main exiting\n")
        pass

if __name__ == '__main__':
    main()
    print("script exiting\n")
