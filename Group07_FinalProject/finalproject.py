import tensorflow as tf
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
from datetime import datetime

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]

# GPIO設定、預設LED關閉、預設聲音關閉
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.output(11,False)
GPIO.output(12,False)
voice = GPIO.PWM(13,880)
voice.stop()

# 初始化藥物編號與儲存陣列
medicine = {"1":"B群", "2":"葉黃素", "3":"魚油", "4":"鈣片"}
weekend = [[], [], [], [], [], [], []]

# 載入模型、資料格式設定、相機抓取
model = tf.keras.models.load_model('keras_model.h5', compile=False)   
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)           
cap = cv2.VideoCapture(0)

# 進入功能
while(True):
    choice = int(input("功能選項：(1)規劃每天藥品 (2)查看目前藥物規劃 (3)使用 (4)新增藥物 (5)結束 \n"))
    if(choice == 1):
        while(True):
            choice2 = int(input("想要設定星期幾的藥物? \n"))
            
            # 設定當日藥物並print出來
            print("請輸入藥物編號：(1)魚油 (2)葉黃素 (3)B群 (4)鈣片")
            weekend[choice2-1].append(medicine[str(input())])
            print("目前設定好的藥物為：")
            for i in range(len(weekend[choice2-1])):
                print(weekend[choice2-1][i] + "\t")
                
            # 判斷是否要繼續設定藥物
            choice3 = int(input("功能選擇：(1)繼續設定藥物 (2)結束 \n"))
            if(choice3 == 2):
                break
            
    elif(choice == 2):
        # 印出目前每天規劃的藥物
        for i in range(len(weekend)):
            print("星期" + str((i + 1)) + ": \t")
            for j in range(len(weekend[i])):
                print(weekend[i][j] + "\t")
            print("\n")
            
    elif(choice == 3):
        # 判斷今日要吃的藥物
        today_med = []
        today = datetime.today().weekday()
        print("今天星期" + str(today + 1) + "，要吃的藥有： \t")
        for i in range(len(weekend[today])):
            print(weekend[today][i] + "\t")
            med_num = get_key(medicine, weekend[today][i])
            today_med.append(int(med_num[0]))
            
        # 判斷相機是否開啟
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
            
        # 進入辨識畫面
        while True:
            ret, frame = cap.read()       
            if not ret:
                print("Cannot receive frame")
                break
            img = cv2.resize(frame , (398, 224))   
            img = img[0:224, 80:304]               
            image_array = np.asarray(img)          
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1 
            data[0] = normalized_image_array
            prediction = model.predict(data)       
            a,b,c,d = prediction[0]
                                
            if a > 0.9:
                print("魚油")
                answer = 1
                if answer in today_med:
                    voice.stop()
                    GPIO.output(11,True)
                    GPIO.output(12,False)
                else:
                    voice.start(99) 
                    GPIO.output(11,False)
                    GPIO.output(12,True)
            if b > 0.9:
                print("葉黃素")
                answer = 2
                if answer in today_med:
                    voice.stop()
                    GPIO.output(11,True)
                    GPIO.output(12,False)
                else:
                    voice.start(99) 
                    GPIO.output(11,False)
                    GPIO.output(12,True)
            if c > 0.9:
                print("B群")
                answer = 3
                if answer in today_med:
                    voice.stop()
                    GPIO.output(11,True)
                    GPIO.output(12,False)
                else:
                    voice.start(99) 
                    GPIO.output(11,False)
                    GPIO.output(12,True)
            if d > 0.9:
                print("鈣片")
                answer = 4
                if answer in today_med:
                    voice.stop()
                    GPIO.output(11,True)
                    GPIO.output(12,False)
                else:
                    voice.start(99)
                    GPIO.output(11,False)
                    GPIO.output(12,True)
                
            cv2.imshow('藥品辨識畫面', img)
            if cv2.waitKey(500) == ord('q'):
                break
                 
        cap.release()
        cv2.destroyAllWindows()
                
    elif(choice == 4):
        # 設定新增藥物
        while(True):
            print("功能選項：(1)新增藥物 (2)結束")
            choice4 = int(input())
            if(choice4 == 1):
                dict_len = len(medicine)
                medicine[str(dict_len + 1)] = str(input("請輸入藥物名稱："))
            elif(choice4 == 2):
                break
              
        # 列出所有藥物
        print("目前所有藥物：")
        for i in range(len(medicine)):
            print(str(i+1) + ". " + medicine[str(i+1)] + "\t")
            
GPIO.cleanup()