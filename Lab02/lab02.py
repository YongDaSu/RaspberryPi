import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
pwm = GPIO.PWM(11,1000)
pwm1 = GPIO.PWM(12,1000)
pwm.start(0)
pwm1.start(0)

while True:
    
    try:
        for i in range(0,100,1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.001)
        time.sleep(1)
        for i in range(100,-1,-1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.001)
        time.sleep(1)
        ##2
        for i in range(0,100,1):
            pwm1.ChangeDutyCycle(i)
            time.sleep(0.001)
        time.sleep(1)
        for i in range(100,-1,-1):
            pwm1.ChangeDutyCycle(i)
            time.sleep(0.001)
        time.sleep(1)
        
    except KeyboardInterrupt:
        break
        
GPIO.cleanup()

