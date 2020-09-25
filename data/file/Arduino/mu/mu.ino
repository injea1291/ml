#include <Keyboard.h>


int radm;
int altk = 130;
int ctrlk = 128;

int ek = 101;
int dk = 100;
int sk = 115;
int ak = 97;
int xk = 120;
int vk = 118;
int wk = 119;

int leftk = 216;
int rightk = 215;
int upk = 218;
int downk = 217;

bool wyn = false;
int wcont = 0;

void adl(int mn, int mx) {
  int a = random(mn, mx);
  delay(a);
}

void key(int asd) {
  Keyboard.press(asd);
  adl(40, 110);
  Keyboard.release(asd);
}

void atkctrl(){
  radm = random(0,10);
  if(wyn == true){
    wcont++;
    if(radm >= 7){
      key(altk);
      adl(41,70);
      key(altk);
      adl(41,70);
      key(wk);
      adl(560,630);
    }
    else{
      key(altk);
      adl(41,70);
      key(altk);
      adl(41,70);
      key(altk);
      adl(41,70);
      key(wk);
      adl(560,630);
    }
    if(wcont >= 3){
      wcont = 0;
      wyn = false;
    }
  }
  else{
    if(radm >= 7){
      key(altk);
      adl(41,70);
      key(altk);
      adl(41,70);
      key(ctrlk);
      adl(560,630);
    }
    else{
      key(altk);
      adl(41,70);
      key(altk);
      adl(41,70);
      key(altk);
      adl(41,70);
      key(ctrlk);
      adl(560,630);
    }
  }

  
    
  
}

void atkdsa(){
  key(altk);
  adl(41,70);
  key(altk);
  adl(41,70);
  Keyboard.press(leftk);
  adl(41,60);
  key(dk);
  adl(41,60);
  Keyboard.release(leftk);
  adl(320,410);
  adl(41,60);
  Keyboard.press(rightk);
  adl(41,70);
  key(sk);
  adl(280,330);
  Keyboard.release(rightk);
  adl(40,70);
  key(ak);
  adl(41,70);
  key(ak);
  adl(400,500);
}

void wran(){
  radm = random(0,2);
  if(radm == 1) {
    wyn = true;
  }
}


 
void setup() {
  Keyboard.begin();
  randomSeed(analogRead(0));
  delay(3000);
}

void loop() {
  radm = random(3);
  if(radm == 1){
    key(198);
    adl(900,1000);
  }
  adl(100,200);
  key(altk);
  adl(41,70);
  Keyboard.press(rightk);
  adl(21,41);
  Keyboard.press(upk);
  adl(21,41);
  Keyboard.press(xk);
  adl(255,278);
  
  
  Keyboard.release(rightk);
  adl(21,41);
  Keyboard.release(upk);
  adl(21,41);
  Keyboard.release(xk);
  adl(102,157);
  key(xk);
  adl(370,420);
  atkdsa();
  key(altk);
  adl(41,70);
  key(altk);
  adl(41,70);
  key(ctrlk);
  adl(560,630);
  
  key(altk);
  adl(41,70);
  key(altk);
  adl(41,70);
  key(ctrlk);
  adl(560,590);
  
  key(118);
  
  adl(101,150);
  
  Keyboard.press(rightk);
  adl(21,41);
  Keyboard.press(upk);
  adl(21,41);
  Keyboard.press(xk);
  adl(120,160);
  Keyboard.release(xk);
  adl(21,41);
  Keyboard.release(rightk);
  adl(21,41);
  Keyboard.release(upk);
  adl(171,210);
  key(xk);
  adl(300,350);
  
  radm = random(0,2);
  if(radm == 1){
    key(altk);
    adl(41,60);
  }
  
  key(ek);
  adl(800,900);
  Keyboard.press(downk);
  adl(41,60);
  
  radm = random(0,2);
  if(radm == 1){
    key(altk);
    adl(41,70);
  }
  
  key(altk);
  adl(41,70);
  Keyboard.release(downk);
  adl(550,650);
  
  
  Keyboard.press(leftk);
  adl(41,60);
  key(ak);
  adl(41,60);
  Keyboard.release(leftk);
  adl(190,240);

  key(sk);
  adl(550,650);
  
  wran();
  atkctrl();
  wran();
  atkctrl();
  wran();
  atkctrl();

 
  
  atkctrl();
  atkctrl();
  atkctrl();
  
}
