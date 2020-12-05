#include <Keyboard.h>

int radm;
int altk = 130;
int ctrlk = 128;

int ek = 101;
int dk = 100;
int sk = 115;
int ak = 97;
int ck = 99;
int xk = 120;
int vk = 118;
int wk = 119;
int f1 = 194;
int f2 = 195;
int endk = 213;
int leftk = 216;
int rightk = 215;
int upk = 218;
int downk = 217;

int stackdot;
int stackpoz;
int stackmat;
int stackmi = 196;
int asd = 2;
int act[3];
int spc;

void adl(int mn, int mx) {
  int a = random(mn, mx);
  delay(a);
}

void key(int asd) {
  Keyboard.press(asd);
  adl(40, 110);
  Keyboard.release(asd);
}

void ct(int asd){
  stackdot++;
  stackpoz++;
  stackmat++;
  stackmi++;
  spc++;
  int action;
  act[0] = 0;
  action++;

  if(spc >= 5){
    if(stackdot >= 28){
      act[action] = 1;
      action++;
    }
    if(stackpoz >= 28){
      act[action] = 2;
      action++;
    }
    if(stackmat >= 52){
      act[action] = 3;
      action++;
    }
  }
  
  
  int select = random(0,action);
  switch (act[select])
  {
    case 0:
      radm = random(1,11);
      if (radm >= 7){
        key(ctrlk);
        adl(20,40);
        Keyboard.press(asd);
        adl(40,60);
        key(ctrlk);
        adl(30,50);
        key(xk);
        adl(30,50);
        key(xk);
        adl(20,40);
        Keyboard.release(asd);
        adl(400,450);
      }
      else{
        key(ctrlk);
        adl(20,40);
        Keyboard.press(asd);
        adl(40,60);
        key(xk);
        adl(30,50);
        key(xk);
        adl(20,40);
        Keyboard.release(asd);
        adl(440,480);
      }
      break;
    case 1:
      key(vk);
      adl(20,40);
      Keyboard.press(asd);
      adl(40,60);
      key(vk);
      adl(550,620);
      key(xk);
      adl(30,50);
      key(xk);
      adl(20,40);
      Keyboard.release(asd);
      adl(400,460);
      stackdot = 0;
      spc = 0;
      break;
    case 2:
      key(ck);
      adl(20,40);
      Keyboard.press(asd);
      adl(40,60);
      key(ck);
      adl(30,50);
      key(xk);
      adl(30,50);
      key(xk);
      adl(20,40);
      Keyboard.release(asd);
      adl(400,450);
      stackpoz = 0;
      spc = 0;
      break;
    case 3:
      key(sk);
      adl(20,40);
      Keyboard.press(asd);
      adl(40,60);
      key(sk);
      adl(750,780);
      key(xk);
      adl(30,50);
      key(xk);
      adl(20,40);
      Keyboard.release(asd);
      adl(400,460);
      stackmat = 0;
      spc = 0;
      break;
  }
}


void setup() {
  Keyboard.begin();
  randomSeed(analogRead(0));
  delay(3000);
}

void loop() {
  if (stackmi >= 196){
    if (asd >= 1){
      key(f1);
      adl(2450,2500);
      asd = 0;
    }
    key(f2);
    adl(950,1000);
    key(endk);
    adl(600,650);
    stackmi = 0;
    asd++;
  }
  key(leftk);
  adl(50,80);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  ct(leftk);
  key(rightk);
  adl(70,100);
  ct(downk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  ct(rightk);
  
  key(altk);
  adl(45,70);
  Keyboard.press(upk);
  adl(30,50);
  key(xk);
  adl(30,50);
  key(xk);
  adl(20,40);
  Keyboard.release(upk);
  adl(350,420);

  
}
