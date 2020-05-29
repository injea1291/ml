import serial
from time import sleep
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
import win32api
from threading import Thread, Lock
import winsound
from models import *
from utils.datasets import *
from utils.utils import *
import random


class Keyboard:
    def __init__(self):
        self.keyvalue, self.status, self.wait, self.raseof = 0, 0, False, True

    def __call__(self, keyvalue, es=40, ee=70, ss=40, se=70):
        s, e = self.snedpacket(1, keyvalue, ss, se, es, ee)
        print(f'(KeyBoard.Write : {keyvalue}, {s}, {e})')
        sleep(s / 1000)
        sleep(e / 1000)

    def snedpacket(self, status, keyvalue, ss, se, es=40, ee=70):
        if self.status == 2 and self.wait:
            self.ra()
            self.wait = False
        if type(keyvalue) == str:
            self.keyvalue = ord(keyvalue)
        else:
            self.keyvalue = keyvalue
        self.status = status
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(0,{status},{self.keyvalue},{s - 5},{e})'
        ser.write(packet.encode())
        return s, e

    def p(self, keyvalue, es=40, ee=70, wait=False):
        if self.keyvalue != keyvalue or self.status != 2:
            s, e = self.snedpacket(2, keyvalue, ss=es, se=ee)
            self.wait = wait
            print(f'(KeyBoard.Press : {keyvalue},{s})')
            sleep(s / 1000)
        else:
            e = random.randint(es, ee)
            sleep(e / 1000)

    def r(self, keyvalue, es=40, ee=70):
        s, e = self.snedpacket(3, keyvalue, ss=es, se=ee)
        print(f'(KeyBoard.release : {keyvalue},{s})')
        sleep(s / 1000)

    def ra(self, es=40, ee=70):
        e = random.randint(es, ee)
        self.status = 4
        packet = f'(0,{4},{self.keyvalue},{e - 5},{e})'
        ser.write(packet.encode())
        print(f'KeyBoard.ReleaseAll')
        sleep(e / 1000)


class fi:
    def __init__(self, findimgname, sx, ex, sy, ey, masktf=False, pixtf=False):
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.masktf = masktf
        self.find = cv.imread(f'dataimg\\{findimgname}.png')
        self.w, self.h = self.find.shape[1::-1]
        if pixtf:
            self.pixli = fi.pixex(self.find)

        self.find = cv.cvtColor(self.find, cv.COLOR_BGR2GRAY)
        if self.masktf:
            self.ms = cv.imread(f'dataimg\\{findimgname}m.png', cv.IMREAD_GRAYSCALE)

    def re(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sx:self.ex, self.sy:self.ey], cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)

        return mxy

    def remask(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sx:self.ex, self.sy:self.ey], cv.COLOR_BGR2GRAY)
        # mask match only can TM_SQDIFF and TM_CCORR_NORMED
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)
        return mxy

    def pix(self, creenimg):
        cutimgy = cv.inRange(creenimg[self.sx:self.ex, self.sy:self.ey], np.array(self.pixli[0]),
                             np.array(self.pixli[0]))

        for i in self.pixli[1:]:
            cutimgy = cv.bitwise_or(cutimgy,
                                    cv.inRange(creenimg[self.sx:self.ex, self.sy:self.ey], np.array(i), np.array(i)))
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)
        return mxy

    @staticmethod
    def pixex(img):
        pixli = []
        w, h = img.shape[1::-1]
        for i in range(w):
            for e in range(h):
                if not pixli.count(list(img[e, i])):
                    pixli.append(list(img[e, i]))
        return pixli


def creen():
    le, to, ri, bo = win32gui.GetWindowRect(hwnd)
    w = ri - le
    h = bo - to

    hdc = win32gui.GetWindowDC(hwnd)

    uihdc = win32ui.CreateDCFromHandle(hdc)

    cdc = uihdc.CreateCompatibleDC()
    cbmp = win32ui.CreateBitmap()
    cbmp.CreateCompatibleBitmap(uihdc, w, h)

    cdc.SelectObject(cbmp)
    cdc.BitBlt((0, 0), (w, h), uihdc, (0, 0), win32con.SRCCOPY)
    signedintsarray = cbmp.GetBitmapBits(True)
    img = np.frombuffer(signedintsarray, dtype='uint8')
    img.shape = (h, w, 4)
    img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    win32gui.DeleteObject(cbmp.GetHandle())
    cdc.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img


class Mouse:
    def __call__(self, es=40, ee=70, ss=40, se=70):
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(1,1,0,{s - 5},{e})'
        ser.write(packet.encode())
        sleep(s / 1000)
        sleep(e / 1000)

    def m(self, x, y, ss=40, se=70):
        def pm(a):
            if a > 0:
                return 1
            elif a == 0:
                return 0
            else:
                return -1

        x1,x2 = divmod(x,127)
        y1,y2 = divmod(y,127)

        for i in range(max(abs(x1),abs(y1))):
            packet = f'(1,2,{127*pm(x1)},{127*pm(y1)},0)'
            ser.write(packet.encode())
            x1 -= pm(x1)
            y1 -= pm(y1)
            sleep(5 / 1000)
        s = random.randint(ss, se)
        packet = f'(1,2,{x2},{y2},{s - 5})'
        ser.write(packet.encode())
        sleep(s / 1000)



ser = serial.Serial(
    port='COM3',
    baudrate=9600, timeout=0
)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esc = 130, 129, 128, 216, 215, 218, 217, 177
pos1, pos = 0, 0
mo = Mouse()
print(win32api.GetCursorPos())
sleep(1)
mo.m(500,300)
print(win32api.GetCursorPos())