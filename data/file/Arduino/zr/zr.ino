#include <Keyboard.h>
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
int radm;

void adl(int mn, int mx) {
  int a = random(mn, mx);
  delay(a);
}

void key(int asd, int mi=40, int mx=110) {
  Keyboard.press(asd);
  adl(mi, mx);
  Keyboard.release(asd);
}

void dob(int asd) {
  key(asd);
  adl(41,70);
  key(asd);
  adl(41,70);
  key(asd);
}


void asdf(int asd){
  radm = random(1,101);
  if(radm <= 20){
    key(vk);
    adl(450,500);
    key(vk);
    adl(450,500);
    key(vk);
    adl(450,490);
  }
  else if(radm >=60){
    key(vk);
    adl(41,70);
    Keyboard.press(vk);
    adl(40, 70);
    Keyboard.release(vk);
    adl(350,400);
    
    key(vk);
    adl(41,70);
    Keyboard.press(vk);
    adl(40, 70);
    Keyboard.release(vk);
    adl(350,400);
    
    key(vk);
    adl(41,70);
    Keyboard.press(vk);
    adl(40, 70);
    Keyboard.release(vk);
    adl(350,390);
  }
  else{
    Keyboard.press(vk);
    adl(1450,1500);
    Keyboard.release(vk);
  }
  
  dob(upk);
  adl(41,70);
  
  key(altk);
  adl(41,70);
  key(altk);
  adl(41,70);
  key(altk);
  adl(70,100);
  radm = random(0,2);
  if(radm == 0){
    key(ck);
    adl(870,920);
    key(ck);
    adl(870,920);
  }
  else{
    key(ck,1650,1700);
  }

  key(sk);
  adl(650,700);
  
  key(altk);
  adl(41,70);
  key(altk);
  adl(41,70);
  key(altk);
  
  adl(160,190);
  dob(asd);
  adl(200,250);
  key(sk);
  adl(40,70);
  radm = random(0,4);
  if(radm == 0){
    key(ctrlk);
    adl(40,70);
    key(ctrlk);
    adl(41,70);
  }
  else{
    key(ctrlk);
    adl(41,70);
  }
  
  Keyboard.press(asd);
  adl(140,180);


  Keyboard.press(upk);
  adl(51,70);
  Keyboard.press(downk);
  adl(50,70);
  Keyboard.press(altk);
  adl(51,70);
  Keyboard.release(upk);
  adl(30,50);
  Keyboard.release(asd); 
  adl(30,50);
  Keyboard.release(downk);
  adl(30,50);
  Keyboard.release(altk);

  
  
  adl(1300,1400);

  if(asd == rightk){
    Keyboard.press(leftk);
    adl(1200,1300);
    Keyboard.release(leftk);
  }
  else{
    Keyboard.press(rightk);
    adl(1200,1300);
    Keyboard.release(rightk);
  }
  
}
void setup() {
  Keyboard.begin();
  randomSeed(analogRead(0));
  delay(3000);
}


void loop() {
  asdf(rightk);
  asdf(leftk);
}
