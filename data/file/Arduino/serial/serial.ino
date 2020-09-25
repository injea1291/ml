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


int wcont = 0;
int swcont = 0;

int ch;
int rfud[4];
int c = 'e';
void adl(int mn, int mx) {
  int a = random(mn, mx);
  delay(a);
}

void key(int asd, int mi = 40, int mx = 70) {
  Keyboard.press(asd);
  adl(mi, mx);
  Keyboard.release(asd);
}

void atkctrl() {
  radm = random(0, 20);
  if (swcont >= 2) {
    wcont++;
    if (radm >= 19) {
      Keyboard.press(leftk);
      adl(20, 30);
      key(altk);
      adl(41, 70);
      key(altk);
      adl(20, 30);
      Keyboard.release(leftk);
      adl(41, 70);
      key(wk);
      adl(560, 630);
    }
    else {
      Keyboard.press(leftk);
      adl(20, 30);
      key(altk);
      adl(41, 70);
      key(altk);
      adl(20, 30);
      Keyboard.release(leftk);
      adl(41, 70);
      key(altk);
      adl(41, 70);
      key(wk);
      adl(560, 630);
    }
    if (wcont >= 3) {
      wcont = 0;
      swcont = 0;
    }
  }
  else {
    if (radm >= 19) {
      Keyboard.press(leftk);
      adl(20, 30);
      key(altk);
      adl(41, 70);
      key(altk);
      adl(20, 30);
      Keyboard.release(leftk);
      adl(41, 70);
      key(ctrlk);
      adl(560, 630);
    }
    else {
      Keyboard.press(leftk);
      adl(20, 30);
      key(altk);
      adl(41, 70);
      key(altk);
      adl(20, 30);
      Keyboard.release(leftk);
      adl(41, 70);
      key(altk);
      adl(41, 70);
      key(ctrlk);
      adl(560, 630);
    }
  }
}

void atkdsa() {
  key(dk);
  adl(40, 60);
  key(dk);
  adl(650, 670);
  Keyboard.press(rightk);
  adl(41, 70);
  key(sk);
  adl(40, 60);
  key(sk);
  adl(250, 280);
  Keyboard.release(rightk);
  adl(30, 50);
  key(ak);
  adl(40, 60);
  key(ak);
  adl(400, 500);
}


void st() {
  swcont++;
  key(96);
  adl(900, 930);
  atkdsa();



  key(altk);
  adl(41, 70);
  key(altk);
  adl(41, 70);
  key(ctrlk);
  adl(560, 630);

  key(altk);
  adl(41, 70);
  key(altk);
  adl(41, 70);
  key(ctrlk);
  adl(560, 590);

  key(118);

  adl(101, 150);

  Keyboard.press(rightk);
  adl(21, 41);
  Keyboard.press(upk);
  adl(21, 41);
  Keyboard.press(xk);
  adl(120, 160);
  Keyboard.release(xk);
  adl(21, 41);
  Keyboard.release(rightk);
  adl(21, 41);
  Keyboard.release(upk);
  adl(171, 210);
  key(xk);
  adl(300, 350);

  radm = random(0, 2);
  if (radm == 1) {
    key(altk);
    adl(41, 60);
  }

  key(ek);
  adl(800, 900);
  Keyboard.press(downk);
  adl(41, 60);

  radm = random(0, 2);
  if (radm == 1) {
    key(altk);
    adl(41, 70);
  }

  key(altk);
  adl(41, 70);
  Keyboard.release(downk);
  adl(530, 580);


  Keyboard.press(leftk);
  adl(41, 60);
  key(ak);
  adl(41, 60);
  Keyboard.release(leftk);
  adl(170, 220);

  key(sk);
  adl(550, 650);

  SerialUSB.println(1);
}


void setup() {
  SerialUSB.begin(9600);
  randomSeed(analogRead(0));
  delay(3000);


}

void loop() {
  while (SerialUSB.available()) {
    ch = SerialUSB.read();
  }



  if (ch == 'a' && c != ch) {
    st();
    c = ch;
  }

  if (ch == 'r' && c != ch) {
    Keyboard.releaseAll();
    Keyboard.press(rightk);
    c = ch;
  }

  if (ch == 'l' && c != ch) {
    Keyboard.releaseAll();
    Keyboard.press(leftk);
    c = ch;
  }

  if (ch == 'u' && c != ch) {
    Keyboard.releaseAll();
    key(altk);
    adl(100, 130);
    key(96);
    c = ch;
  }

  if (ch == 'd' && c != ch) {
    Keyboard.releaseAll();
    Keyboard.press(downk);
    adl(41, 60);
    key(altk);
    adl(41, 70);
    Keyboard.release(downk);
    c = ch;
  }

  if (ch == 's' && c != ch) {
    Keyboard.releaseAll();
    key(32);
    c = ch;
  }
  if (ch == 'j' && c != ch) {
    Keyboard.releaseAll();
    Keyboard.press(leftk);
    adl(30, 50);
    key(altk);
    adl(41, 70);
    key(altk);
    adl(30, 50);
    Keyboard.release(leftk);
  }
  if (ch == 'k' && c != ch) {
    Keyboard.releaseAll();

    Keyboard.press(rightk);
    adl(30, 50);
    key(altk);
    adl(41, 70);
    key(altk);
    adl(30, 50);
    Keyboard.release(rightk);
  }


  if (ch == 'e' && c != ch) {
    Keyboard.releaseAll();
    wcont = 0;
    c = ch;
  }

  if (ch == '0' && c != ch) {
    key(rightk);
    c = ch;
  }
  if (ch == '1' && c != ch) {
    key(leftk);
    c = ch;
  }
  if (ch == '2' && c != ch) {
    key(upk);
    c = ch;
  }
  if (ch == '3' && c != ch) {
    key(downk);
    c = ch;
  }
  if (ch == '4') {
    atkctrl();
    c = ch;
  }
  if (ch == '5') {
    key(198);
    adl(1000, 1100);
    key(213);
    adl(700, 800);
    c = ch;
  }
}
