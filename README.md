# NII
ラズベリーパイ・カメラとESP32を使用して、居眠り運転事故防止装置として利用するプログラム

ESP32のプログラム
handle_f:プレスセンサーとブザーセンサーを使用
sleep_f:バイブレーションセンサー使用

ラズベリーパイ内のパイソンプログラム
handle.py:プレスセンサーからの信号を受け取り、ブザーを作動し警告
スプレッドシートに状態を記入
predict_bs.py:カメラから瞼の開閉・首の傾きを検知し、ESP32のバイブレーションを作動し警告
スプレッドシートに状態を記入
