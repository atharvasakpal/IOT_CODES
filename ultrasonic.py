import Rpi.GPIO as GPIO

import time

TRIG = 16
ECHO = 18

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)  # Trigger   
GPIO.setup(ECHO, GPIO.IN)   # Echo

def get_distance():
    #send 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    #Measure the time for echo response
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
    #Calculate distance
    duration = stop_time - start_time
    distance = (duration * 34300)/2  # Speed of sound is 34300 cm/s
    return round(distance, 2)

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

    

