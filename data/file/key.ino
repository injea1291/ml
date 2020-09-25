#include <Mouse.h>
#include <Keyboard.h>


void adl(int mn, int mx) {
  int a = random(mn, mx);
  delay(a);
}

void key(int as, int asd, int mi, int mx) {  
  switch (as){
    case 1:
      Keyboard.press(asd);
      delay(mi);
      Keyboard.release(asd);
      delay(mx);
      break;
     case 2:
      Keyboard.press(asd);
      delay(mi);
      break;
     case 3:
      Keyboard.release(asd);
      delay(mi);
      break;
     case 4:
      Keyboard.releaseAll();
      delay(mi);
      break;
  }
}


void Mou(int as, int asd, int mi, int mx) {
  switch (as){
    case 1:
      Mouse.press();
      delay(mi);
      Mouse.release();
      delay(mx);
      break;
    case 2:
      Mouse.move(asd,mi);
      delay(mx);
      break;
  }
}

String str;

void setup() {
  SerialUSB.begin(9600); 
  SerialUSB.setTimeout(5);
  randomSeed(analogRead(0));
  Mouse.begin();
  Keyboard.begin();
}

void loop() {
  if(SerialUSB.available()){
    str = SerialUSB.readString();
    if(str.charAt(0) == '(' and str.charAt(str.length()-1) == ')') {
      int s1 = str.indexOf(",");
      int s2 = str.indexOf(",",s1+1);
      int s3 = str.indexOf(",",s2+1);
      int s4 = str.indexOf(",",s3+1);
      int s5 = str.indexOf(">",s4);
      int i1 = str.substring(1, s1).toInt();
      int i2 = str.substring(s1+1, s2).toInt();
      int i3 = str.substring(s2+1, s3).toInt();
      int i4 = str.substring(s3+1, s4).toInt();
      int i5 = str.substring(s4+1, s5).toInt();
      if (i1 == 0){
        key(i2,i3,i4,i5);
      }
      else{
        Mou(i2,i3,i4,i5);
      }
    }
  }
}
