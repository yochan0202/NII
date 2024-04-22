import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model,load_model
from PIL import Image
import sys
import datetime
import cv2

#OpenCV用に追加
#import argparse
#import random
import time

# OpenCVのチックメータ（ストップウオッチ）機能をtmという名前で使えるようにする
tm = cv2.TickMeter()

tokyo_tz = datetime.timezone(datetime.timedelta(hours=9))

#シリアル通信の追加 2021/10/04
import serial
#ser = serial.Serial('COM5', 115200, timeout=0.1) 
import requests
# カメラバッファ読み飛ばし回数
CAMERA_BUF_FLUSH_NUM = 6

#寝ていると判断した際のカウント
sleep_count = 0
#首傾きと判断した際のカウント
neck_count = 0
# パラメーターの初期化
classes = ["open", "close","kubi"]
num_classes = len(classes)
image_size = 224

# モデルのロード
print('モデルのロード...')
model = load_model('./vgg16_transfer.h5')

# ビデオカメラ開始
print('ビデオカメラ開始...')
cap = cv2.VideoCapture(0)


# 画像キャプチャと検出の永久ループ
while True:
    cap_start = time.time()
    #print('...at 002')                                ###########################

    #バッファに滞留しているカメラ画像を指定回数読み飛ばし、最新画像をframeに読み込む
    for i in range(CAMERA_BUF_FLUSH_NUM):
        ret, frame = cap.read()
        
    #print('...at 003')                                ###########################
    
    # 取り込んだ画像の幅を縦横比を維持して500ピクセルに縮小
    ratio = 500 / frame.shape[1]
    frame = cv2.resize(frame, dsize=None, fx=ratio, fy=ratio)
    #frame = cv2.resize(frame, dsize=(500,500), fx=ratio, fy=ratio)

    #print('...at 004')                                ###########################
    cap_end = time.time()

    


###    ## フレームを参照して画像を推論プラグラム用に変換
    predict_start = time.time()
    image = frame
    image = cv2.resize(image,(image_size,image_size))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #data = cv2.normalize(image, image, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    data = np.asarray(image) / 255.0
    
    cv2.imshow('Image-1', image)
    print('...at 006')                                ###########################
    
    X = []
    X.append(data)
    X = np.array(X)
###
###    #推論 VGG16モデルを動かす
    result = model.predict([X])[0]
    predicted = result.argmax()
    percentage = int(result[predicted] * 100)
    
    #print(classes[predicted], percentage)
    print(classes[predicted], percentage)
    predict_end = time.time()
    
    if classes[predicted] == classes[1]:
        sleep_count = sleep_count + 1
    
    if classes[predicted] == classes[0] or classes[predicted] == classes[2]:
        sleep_count = 0
    
    if sleep_count >= 3:
        print("寝てる")
        
        ser = serial.Serial('/dev/ttyUSB0', 115200) 
        
        ser.write(b'A')
        print("ON")
        time.sleep(0.5)
        
        ser.close()
        print("end")
        
        url = 'https://script.google.com/macros/s/AKfycbxL8ozI0oYF1zourgyGPpodklQvN6kBMR_vaXiAy-OrEqYHWNi0fPJVlL6TNaQ5FhP82w/exec?data1=Sleep'
        requests.get(url)
        
        #ブザーとスプレッドシート用処理を記述
        sleep_count = 0
    
    if classes[predicted] == classes[2]:
        neck_count = neck_count + 1
    
    if classes[predicted] == classes[0] or classes[predicted] == classes[1]:
        neck_count = 0
    
    if neck_count >= 3:
        print("首傾き")
        
        ser = serial.Serial('/dev/ttyUSB0', 115200) 
        
        ser.write(b'A')
        print("ON")
        time.sleep(0.5)
        
        ser.close()
        print("end")
        
        url = 'https://script.google.com/macros/s/AKfycbxL8ozI0oYF1zourgyGPpodklQvN6kBMR_vaXiAy-OrEqYHWNi0fPJVlL6TNaQ5FhP82w/exec?data1=Neck'
        requests.get(url)
        
        #ブザーとスプレッドシート用処理を記述
        neck_count = 0
    
    # フレームを画面に描画
    cv2.imshow('Live', frame)  
    
    
    if cv2.waitKey(50) >= 0:
        break
        
    print('キャプチャ時間:')
    print(cap_end - cap_start)
    print('推論時間:')
    print(predict_end - predict_start)
    
    #print('...at 008')                                ###########################
    
    #time.sleep(args['interval'])
    time.sleep(0.1)

# 終了処理
print('終了処理...')
cv2.destroyAllWindows()
cap.release()
time.sleep(3)
#シリアル通信の追加 2021/10/04
#ser.close()


