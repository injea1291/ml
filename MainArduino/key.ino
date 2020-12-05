#include <Mouse.h>
#include <Keyboard.h>

void split(String results[], int len, String input, char spChar) {
  String temp = input;
  for (int i=0; i<len; i++) {
    int idx = temp.indexOf(spChar);
    results[i] = temp.substring(0,idx);
    temp = temp.substring(idx+1);
  }
}

void key(int cas, String data) {  
  switch (cas){
    case 0:
      Keyboard.press(data.toInt());
      break;
    case 1:
      Keyboard.release(data.toInt());
      break;
    case 2:
      Keyboard.releaseAll();
      break;
  }
}


void Mou(int cas, String data) {
  String datas[2];
  switch (cas){
    case 0:
      split(datas,2,data,',');
      Mouse.move(datas[0].toInt(),datas[1].toInt());
      break;
    case 1:
      Mouse.press(MOUSE_LEFT);
      break;
    case 2:
      Mouse.press(MOUSE_RIGHT);
      break;
    case 3:
      Mouse.release(MOUSE_LEFT);
      break;
    case 4:
      Mouse.release(MOUSE_RIGHT);
      break;
  }
}

void setup() {
  SerialUSB.begin(9600); 
  SerialUSB.setTimeout(5);
  randomSeed(analogRead(0));
  Mouse.begin();
  Keyboard.begin();
}

void loop() {
  char readChar[64];
  SerialUSB.readBytesUntil(33,readChar,64);
  String rd = String(readChar);
  int idx2 = rd.indexOf('$');
  int mk = rd.substring(0,1).toInt();
  int cas = rd.substring(1,2).toInt();
  String data = rd.substring(2,idx2);
  switch(mk){
    case 0:
      SerialUSB.println("version");
      break;
    case 1:
      key(cas,data);
      break;
    case 2:
      Mou(cas,data);
      break;
  }
}
