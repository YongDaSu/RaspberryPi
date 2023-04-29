import RPi.GPIO as GPIO
import sys
import time
import json

def initEnv(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.IN)
def end():
    GPIO.cleanup()
def getSignal(pin):
    start, stop = 0, 0
    signals = []
    while True:
        while GPIO.input(pin) == 0:
            None
        start = time.time()

        while GPIO.input(pin) == 1:
            stop = time.time()
            duringUp = stop - start
            if duringUp > 0.1 and len(signals) > 0:
                return signals[1:]
        signals.append(duringUp)
        
PIN = int(sys.argv[1])
OUT_FILE = sys.argv[2]

initEnv(PIN)
keys = {}
while True: 
    key_name = input('Please input key name (input exit for exit):')
    if key_name == 'exit':
        break
    keys[key_name] = getSignal(PIN)
end()
    
src = open(OUT_FILE, 'w')
src.write(json.dumps(keys))
src.close()
        
