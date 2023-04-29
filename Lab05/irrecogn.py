import RPi.GPIO as GPIO
import json
import sys
import time

def initEnv(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.IN)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3,False)
    
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
def compairSignal(signal1, signal2, toleration):
    min_len=min(len(signal1), len(signal2))

    for i in range(min_len):
        if abs(signal1[i]-signal2[i])>toleration:
            return False
    return True
def decodeSignal(signal, signal_map, toleration):
    for name in signal_map.keys():
        if compairSignal(signal, signal_map[name], toleration):
            return name
    return None
def end():
    GPIO.cleanup()
    
PIN = int(sys.argv[1])
SIGNAL_MAP = sys.argv[2]

src= open(SIGNAL_MAP, 'r')
signal_map= json.loads(src.read())
src.close
    
initEnv(PIN)

while True:
    print("Please press key")
    s_in = getSignal(PIN)
        
    print('Your press is : %s'%(decodeSignal(s_in, signal_map, 0.001)))
    signal = decodeSignal(s_in, signal_map, 0.001)

    if signal == '1':
        GPIO.output(3, True)
    elif signal == '2':
        GPIO.output(3, False)
    else:
        break
    