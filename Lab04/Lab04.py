import RPi.GPIO as GPIO
import time

# ??????
voice_dic = {'Do':523, 'Re':589, 'Mi':659, 'Fa':698, 'So':784, 'La':880, 'Si':988, 'Do':1047}

# ??GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

#??voice??
voice = GPIO.PWM(11,50)
voice.start(10.0)
GPIO.output(11,True)

while True:
    try:
        # ????
        for key in voice_dic:
          voice.ChangeFrequency(voice_dic[key])
          
          # ?????LED?
          if(key == 'Re' or key =='Fa' or key =='La' or key =='Do'):
            GPIO.output(12,True)
          else:
            GPIO.output(12,False)
          time.sleep(1)
        
    except KeyboardInterrupt:
        break
        
GPIO.cleanup()