#define ledPin 25
#define on HIGH
#define off LOW
byte val; //受け取る

void vibration() {
  digitalWrite(ledPin, on); 
  delay(500);
  digitalWrite(ledPin, on); 
  delay(500);
  digitalWrite(ledPin, off);
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT); 
}

void loop() {
  delay(100);
  if(Serial.available() > 0){ // 受信データがあるか？
    val = Serial.read();//ser.write(b'A')からのシリアルで送られたものを入れる // 1文字だけ読み込む
      if(val == 'A'){
        vibration();// put your setup code here, to run once:
      }
  }
}