import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model,load_model
from PIL import Image
import sys
import datetime

#OpenCV用に追加
import argparse
import random
import time

import cv2

#シリアル通信の追加 2021/10/04
#import serial
#ser = serial.Serial('COM5', 115200, timeout=0.1) 

#年月日時分秒の追加 2021/10/04
import datetime

# カメラバッファ読み飛ばし回数
CAMERA_BUF_FLUSH_NUM = 6

#寝ていると判断した際のカウント
sleep_count = 0

# ラベル毎の枠色をランダムにセット
##colors = {}
##random.seed()
##for key in CLASS_LABELS.keys():
##    colors[key] = (random.randrange(255),
##                   random.randrange(255),
##                   random.randrange(255))

# パラメーターの初期化
classes = ["opena", "closea"]
num_classes = len(classes)
image_size = 224

# モデルのロード
print('モデルのロード...')
model = load_model('./vgg16_transfer.h5')

# ビデオカメラ開始
print('ビデオカメラ開始...')
cap = cv2.VideoCapture(0)

# OpenCVのチックメータ（ストップウオッチ）機能をtmという名前で使えるようにする
tm = cv2.TickMeter()

tokyo_tz = datetime.timezone(datetime.timedelta(hours=9))
#dt = datetime.datetime.now(tokyo_tz)

# 画像キャプチャと検出の永久ループ
while True:
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
    
    # フレームを画面に描画
    cv2.imshow('Live', frame)  
    


###    ## フレームを参照して画像を推論プラグラム用に変換
    #image = Image.open(sys.argv[1])
    #image = Image.open('./img/low_compression.jpg')
    #image = image.convert("RGB")
    image = frame
    image = cv2.resize(image,(image_size,image_size))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    data = np.asarray(image) / 255.0
    
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
    
    if classes[predicted] == classes[1]:
        sleep_count = sleep_count + 1
    
    if sleep_count >= 3:
        print("寝てる")
        #ブザーとスプレッドシート用処理を記述
        sleep_count = 0
    
###    
###    hand = 'HAND:' + str(predicted)
###    
###    ##    print(predicted)                                ###########################
###    print(hand)                                        ###########################
###    #print('...at 007')                                ###########################
###    
###    ser.write(str.encode(str(predicted)))
    
###    outText = 'Hand:'
###    outText = outText + str(predicted) 
###    outText = outText + ','
###    outText = outText + str(percentage)
    outText = 'JPEG FILE make now'


       ##################################

    if cv2.waitKey(50) >= 0:
        break
    
    #print('...at 008')                                ###########################
    
    #time.sleep(args['interval'])
    time.sleep(0.5)

# 終了処理
print('終了処理...')
cv2.destroyAllWindows()
cap.release()
time.sleep(3)
#シリアル通信の追加 2021/10/04
#ser.close()


