## IMPORT ALL THE REQUIRED LIBRARIES ##
import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED

GPIO.setmode(GPIO.BCM)

## SETTING UP THE GPIO PINS ##
LED = 13
TRIG = 23
ECHO = 20

## TO DISABLE THE WARNINGS ##
GPIO.setwarnings(False) 

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

## To GENERATE THE SPECIFIED DUTY CYCLE ##
L = GPIO.PWM(LED, 100)


print('Waiting for Sensor......')
time.sleep(2)
print('In Progress...')


def freq():

    ## TRIGGER SET TO HIGH ##
    GPIO.output(TRIG, True)
    time.sleep(0.0001)

    ## TRIGGER SET TO LOW ##
    GPIO.output(TRIG, False)

    ## Time Calculation ##
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
    
    ## TO FIND DIFFERENCE BETWEEN TWO RECORDED TIME STAMPS
    TimeDifference = StopTime - StartTime
    freq = (TimeDifference * 34300) / 2
    return freq

try:
    while True:
        dis = freq()
        print ("Distance Measured -> " + str(dis) + "cm")

        ## if distance is more or less than required distance then message will be sent respectively ##
        if dis <= 100 and dis > 15:
            print('Accurate Distance')
            L.ChangeDutyCycle((100-dis))

        elif dis < 15 and dis > 0:
            L.start(100)
            print('Object Very Close')
       
        else:
            L.start(0)
            print('Far Distance')
            
        ## Delay of 1 second ##
        time.sleep(1)

except KeyboardInterrupt:
    L.stop()
    GPIO.cleanup()


