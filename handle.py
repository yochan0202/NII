import serial
import time
import requests

while True:
    ser = serial.Serial('/dev/ttyUSB1', 115200)    
    #プレスセンサーからの信号
    received_data = ser.read().decode().strip()
    #val = ser.read()
    #if val == 5:
    if received_data == 'B':
        print("ハンドル")
         
        
        ser.write(b'B')
        print("BUZA1 ON")
        time.sleep(0.5)
        
        ser.close()
        print("end")
        
        url = 'https://script.google.com/macros/s/AKfycbxL8ozI0oYF1zourgyGPpodklQvN6kBMR_vaXiAy-OrEqYHWNi0fPJVlL6TNaQ5FhP82w/exec?data1=Handle'
        requests.get(url)