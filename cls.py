import serial
import random
import cv2.cv2 as cv
from time import sleep
import numpy as np
import win32gui
import win32ui
import win32con
import win32api


class Keyboard:
    def __init__(self, ser):
        self.keyvalue, self.status, self.wait, self.raseof = 0, 0, False, True
        self.ser = ser
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
        self.ser.write(packet.encode())
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
        self.ser.write(packet.encode())
        print(f'KeyBoard.ReleaseAll')
        sleep(e / 1000)

    def change(self, raseof):
        self.raseof = raseof


class Mouse:
    def __init__(self, x, y, ser):
        self.x = x
        self.y = y
        self.ser = ser

    def __call__(self, x, y, ss=40, se=70):
        x1, y1 = win32api.GetCursorPos()
        print(f'Mouse.goto : {x},{y}')
        self.m((x + self.x) - x1, (y + self.y) - y1, ss, se)

    def m(self, x, y, ss=40, se=70):
        def pm(a):
            if a > 0:
                return 1
            elif a == 0:
                return 0
            else:
                return -1

        x1, x2 = divmod(x, 127 if x > 0 else -127)
        y1, y2 = divmod(y, 127 if y > 0 else -127)
        x1 *= pm(x)
        y1 *= pm(y)
        for i in range(max(abs(x1), abs(y1))):
            packet = f'(1,2,{127 * pm(x1)},{127 * pm(y1)},1)'
            self.ser.write(packet.encode())
            x1 -= pm(x1)
            y1 -= pm(y1)
            sleep(6 / 1000)
        s = random.randint(ss, se)
        packet = f'(1,2,{x2},{y2},{s - 5})'
        self.ser.write(packet.encode())
        sleep(s / 1000)

    def c(self, es=40, ee=70, ss=40, se=70):
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(1,1,0,{s - 5},{e})'
        self.ser.write(packet.encode())
        print(f'Mouse.click : {s} {e}')
        sleep(s / 1000)
        sleep(e / 1000)


class fi:
    def __init__(self, findimgname, sx, ex, sy, ey, pixtf=False):
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.pixli = []
        if not findimgname is None:
            self.find = cv.imread(f'dataimg\\{findimgname}.png')
            self.w, self.h = self.find.shape[1::-1]
            if pixtf:
                self.pixli = fi.pixex(self.find)
            self.find = cv.cvtColor(self.find, cv.COLOR_BGR2GRAY)

    def setmaskimg(self, maskimg):
        self.ms = maskimg

    def re(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sy:self.ey, self.sx:self.ex], cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        # cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def remask(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sy:self.ey, self.sx:self.ex], cv.COLOR_BGR2GRAY)
        # mask match only can TM_SQDIFF and TM_CCORR_NORMED
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def piximg(self, creenimg):
        cutimgy = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def pixpix(self, creenimg):
        w, h = self.ex - self.sx, self.ey - self.sy
        creenimg = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        for i in range(w):
            for e in range(h):
                if creenimg[e, i] == 255:
                    return [True, i, e]
        return False

    @staticmethod
    def inRange(img, rgb):
        img1 = cv.inRange(img, np.array(rgb[0][0]), np.array(rgb[0][1]))
        for i in rgb[1:]:
            img1 = cv.bitwise_or(img1, cv.inRange(img, np.array(i[0]), np.array(i[1])))
        return img1

    @staticmethod
    def pixex(img):
        pixli = []
        w, h = img.shape[1::-1]
        for i in range(w):
            for e in range(h):
                if not pixli.count([list(img[e, i]), list(img[e, i])]):
                    pixli.append([list(img[e, i]), list(img[e, i])])
        return pixli


def creen(hwnd):
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
