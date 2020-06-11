import time

import serial
from time import sleep
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
import win32api
import random
import pytesseract
import numpy as np


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
    def __init__(self, findimgname, sx, ex, sy, ey, pixtf=False):
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.pixli = []
        if not findimgname is None:
            self.find = findimgname
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
        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)

        return mxy

    def remask(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sy:self.ey, self.sx:self.ex], cv.COLOR_BGR2GRAY)
        # mask match only can TM_SQDIFF and TM_CCORR_NORMED
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)
        return mxy

    def piximg(self, creenimg):
        cutimgy = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)
        return mxy

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
            img1 = cv.bitwise_or(img, cv.inRange(img1, np.array(i[0]), np.array(i[1])))

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


class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
            ser.write(packet.encode())
            x1 -= pm(x1)
            y1 -= pm(y1)
            sleep(6 / 1000)
        s = random.randint(ss, se)
        packet = f'(1,2,{x2},{y2},{s - 5})'
        ser.write(packet.encode())
        sleep(s / 1000)

    def c(self, es=40, ee=70, ss=40, se=70):
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(1,1,0,{s - 5},{e})'
        ser.write(packet.encode())
        print(f'Mouse.click : {s} {e}')
        sleep(s / 1000)
        sleep(e / 1000)


def goto1(x, y, z=3):
    key.ra()
    while True:
        resul = fi(cv.imread("dataimg\\i.png"), 12, 202, 87, 133, pixtf=True).piximg(creen(hwnd))
        if resul[1][0] - x >= 40:
            key.p(leftk)
            key(altk)
            key(altk)
            key.ra()
        elif x - resul[1][0] >= 40:
            key.p(rightk)
            key(altk)
            key(altk)
            key.ra()
        elif resul[1][0] - x >= z:
            key.p(leftk, wait=True)
        elif x - resul[1][0] >= z:
            key.p(rightk, wait=True)
        elif resul[1][1] > y + 7:
            key(altk, 100, 130)
            key(96, 3000, 3100)
        elif resul[1][1] < y - 7:
            key.p(upk, 20, 40)
            key.p(downk)
            key(altk)
            key.r(upk, 20, 40)
            key.r(downk, 1000, 1100)
        else:
            key.ra()
            break


try:
    ser = serial.Serial(
        port='COM4',
        baudrate=9600, timeout=0
    )
except:
    print("아두이노 노")
hwnd = win32gui.FindWindow(None, 'MapleStory')
left, top, right, bot = win32gui.GetWindowRect(hwnd)
if right - left < 900:
    hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esck, spacek, bsk, tabk, returnk = 130, 129, 128, 216, 215, 218, 217, 177, 32, 8, 179, 176

mo = Mouse(left, top)
key = Keyboard()
fili = [fi(None, 506, 510, 323, 333), fi(None, 476, 750, 558, 559), fi(None, 625, 660, 113, 123),
        fi(None, 1274, 1275, 367, 368)]
fili[0].pixli.append([[255, 255, 255], [255, 255, 255]])
fili[1].pixli.append([[255, 255, 255], [255, 255, 255]])
fili[2].pixli.append([[68, 238, 255], [68, 238, 255]])
fili[3].pixli.append([[68, 238, 255], [68, 238, 255]])
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# cv.imwrite('10.png', creen(hwnd))
while True:
    while True:
        resul = fi(creen(hwnd)[678:683, 1294:1312], 1265, 1285, 677, 684, True)
        resul.pixli.append([[241, 224, 224], [241, 230, 230]])
        if resul.re(creen(hwnd))[0] > 0.99:
            break
        goto1(68, 28)
        while True:
            key(32, 600, 700)
            key(returnk, 600, 700)
            key(returnk, 600, 700)

            if not fili[3].pixpix(creen(hwnd)):
                sleep(2)
                for i in pytesseract.image_to_string(creen(hwnd)[388:418, 450:560]):
                    try:
                        int(i)
                    except:
                        break
                    key(ord(i), 500, 600)
                key(tabk, 300, 400)
                key(spacek, 300, 350)
                if not fili[3].pixpix(creen(hwnd)):
                    key(returnk, 600, 700)
                    continue
            st = time.time()
            atf = False
            while time.time() - st < 90:
                resul = fili[2].pixpix(creen(hwnd))
                if resul:
                    atf = True
                    break
                else:
                    mo(731, 436)
                    mo.c(1000, 1100)
            if atf: break

        sleep(7)

        while True:
            sleep(1)
            cren = creen(hwnd)
            resul = fili[2].pixpix(cren)
            if resul:
                resul = fili[0].pixpix(cren)
                if resul:
                    mo(490, 360)
                    sleep(5)
                    mo.c()

                resul = fili[1].pixpix(cren)
                if resul:
                    mo(476 + resul[1], 558)
                    sleep(5)
                    mo.c()
                    mo(500, 500)
            else:
                sleep(3)
                mo(510, 550)
                mo.c(500, 600)
                mo(650, 550)
                mo.c(2000, 2100)
                key(32, 200, 300)
                key(32, 200, 300)
                break
        sleep(7)

    key(esck, 500, 550)
    key(upk, 500, 550)
    key(returnk, 500, 550)
    key(returnk, 5000, 5100)
    key(rightk, 500, 550)

    if fi(cv.imread('dataimg\\ddd.png'), 630, 722, 239, 310).re(creen(hwnd))[0] > 0.99:
        break
    mo(613, 402)
    mo.c(500, 550)
    key(returnk, 500, 550)

    key(91, 500, 550)
    key(93, 500, 550)
    key(46, 500, 550)
    key(59, 500, 550)
    key(47, 500, 550)
    key(39, 500, 550)
    resul = fi(None, 135, 222, 262, 302)
    resul.pixli.append([[255, 255, 255], [255, 255, 255]])
    mo(135 + resul.pixpix(creen(hwnd))[1], 262 + resul.pixpix(creen(hwnd))[2])
    mo.c(500, 550)
    key(returnk, 8000, 8100)
    key(esck, 500, 550)
    key(esck, 500, 550)
    key(esck, 500, 550)
    key(esck, 500, 550)
    key(esck, 500, 550)
    mo(27, 61)
    mo.c(500, 510)
