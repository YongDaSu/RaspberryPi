import sys
import Adafruit_DHT
import time
import csv

ThingSpeak_WriteApiKey = 'AKO0DNU0KUUH787K'
# 每 `detection_period` 秒偵測一次
detection_period = 5

# 取得目前的溫濕度
#humidity, temperature = get_sensor_data()

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

#開啟一個Lab03.csv檔，寫入模式為a+(新增在檔案後面，不會覆蓋資料)。
with open('Lab03_plus.csv', 'a+', newline='') as csvfile:
    #建立寫入物件
    writer = csv.writer(csvfile)
    #寫入標題
    writer.writerow(['time', 'temperature', 'humidity'])


#持續顯示時間及溫濕度，並寫入CSV
while True:
    
    try:
        #讀取溫濕度數值，並更改delay_seconds
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, delay_seconds=0.5)
        #如果有讀取到，顯示目前時間 溫度 濕度
        if humidity is not None and temperature is not None:
          print(time.ctime() + ", tesmperature:{0:0.1f} 度C, humidity: {1:0.1f} %".format(temperature, humidity))
          #寫入一筆資料到csvfile
          with open('Lab03_plus.csv', 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([str(time.ctime()), temperature, humidity])
            '''
          ThingSpeak_API_URL = f'https://api.thingspeak.com/update?api_key={ThingSpeak_WriteApiKey}&' \
                         f'field1={"{0:0.1f}".format(temperature)}&' \
                         f'field2={"{0:0.1f}".format(humidity)}'
          query = requests.get(ThingSpeak_API_URL)
          print(f'HTTP: {query.status_code}') # 查看 HTTP 狀態碼，若為 200 表示傳送成功
          print(now+',', 'temperature:', temperature, '度C,', 'humidity:', humidity, '%') # 標準輸出溫溼度於本地端
            '''
        #假如沒辦法讀取，離開
        else:
          print('Failed to get reading. Try again!')
          #sys.exit(1)
          continue
          
        time.sleep(detection_period)
    
    #建立一個可以跳出迴圈的interrupt
    except KeyboardInterrupt:
        break



