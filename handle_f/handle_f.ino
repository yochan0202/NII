#define press_pin 32 //INA:33 INB:32
float ain,vo,rf;

unsigned long startTime = 0; // タイマー用の変数
const long interval = 2000; // 2秒間のインターバル
unsigned long currentTime = 0;

#define bzPIN 25
#define BEAT 500
byte val; //受け取る

#define DO 261.6  //周波数の記述

void playmusic1() {
      ledcWriteTone(0, DO);
      delay(BEAT);  //鳴る時間
      ledcWriteTone(0, DO);
      delay(BEAT);
      ledcWriteTone(0, 0);
}

void setup() {
   Serial.begin(115200);
  ledcSetup(0, 12000, 8);
  ledcAttachPin(bzPIN, 0);  //ピンとチャンネル指定
 
  pinMode(press_pin, INPUT);
  startTime = millis();
}

void loop() {
 ain = analogRead(press_pin);
    vo = ain * 3.3 / 4096;//分解能？
    rf = 10000 * vo / (3.3 - vo);
    // Serial.printf("rf = %d\n",rf);
    
    if (rf == 0) {
        currentTime = millis(); // 現在時刻を取得
      if (currentTime - startTime >= interval){
            Serial.write('B');
            // playmusic1();
        }
    } else {
        // 条件以外ではカウントをリセット
       startTime = millis(); // タイマーをリセット
    }

    delay(100);
  if(Serial.available() > 0){ // 受信データがあるか？
    val = Serial.read();//ser.write(b'B')からのシリアルで送られたものを入れる // 1文字だけ読み込む
      if(val == 'B'){
        playmusic1();// put your setup code here, to run once:
      } 
  }
}