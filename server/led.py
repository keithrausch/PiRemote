import RPi.GPIO as GPIO
import time

pin = 17
wait = .25
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

while True:
    print "LED on"
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(wait)

    print "LED off"
    GPIO.output(pin, GPIO.LOW)
    time.sleep(wait)