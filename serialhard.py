import sys
import math
import serial
import random
from time import sleep
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
import numpy as np
from threading import Thread

ser = serial.Serial(
    port='COM4',
    baudrate=9600, timeout=0
)

hwnd = win32gui.FindWindow(None, 'MapleStory')
if hwnd == 0:
    print("프로그램 찾지못함")
    sys.exit()

altk = 130
ctrlk = 128
leftk = 216
rightk = 215
upk = 218
downk = 217
xy = [[0, 0], [0, 0]]


def creen():
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hdc = win32gui.GetWindowDC(hwnd)

    uihdc = win32ui.CreateDCFromHandle(hdc)

    cDC = uihdc.CreateCompatibleDC()
    cbmp = win32ui.CreateBitmap()
    cbmp.CreateCompatibleBitmap(uihdc, w, h)

    cDC.SelectObject(cbmp)
    cDC.BitBlt((0, 0), (w, h), uihdc, (0, 0), win32con.SRCCOPY)
    signedIntsArray = cbmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    win32gui.DeleteObject(cbmp.GetHandle())
    cDC.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img


def match(a, img, b, c, d, e, f=True):
    cutim = img[b:c, d:e]
    cutimgy = cv.cvtColor(cutim, cv.COLOR_BGR2GRAY)
    find = cv.imread(f'{a}.jpg', cv.IMREAD_GRAYSCALE)
    ms = cv.imread(f'{a}m.jpg', cv.IMREAD_GRAYSCALE)
    w, h = find.shape[::-1]
    if f:
        res = cv.matchTemplate(cutimgy, find, cv.TM_CCORR_NORMED, mask=ms)
    else:
        res = cv.matchTemplate(cutimgy, find, cv.TM_CCOEFF_NORMED)

    minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
    cv.rectangle(cutim, maxloc, (maxloc[0] + w, maxloc[1] + h), (255, 0, 0), 1)
    x, y = maxloc[0] + w / 2, maxloc[1] + h / 2
    return maxval, x, y, cutim


def scmc():
    global xy
    while True:
        maxval, x, y, cutim = match("i", creen(), 87, 171, 12, 214)
        maxval1, x1, y1, cutim1 = match("r", creen(), 87, 171, 12, 214)
        if maxval > 0.99:
            xy[0] = x, y
            cv.imshow('asd1', cutim)
            cv.moveWindow('asd1', 10, 100)
            cv.waitKey(1)
        if maxval1 > 0.999 and not math.isinf(maxval1):
            xy[1] = x1, y1
            cv.imshow('asd', cutim1)
            cv.moveWindow('asd', 10, 10)
            cv.waitKey(1)
        print(xy)

def send(b, c=40, d=70, e=40, f=70, a=1):
    if type(b) == str:
        b = ord(b)
    rint = random.randint(c, d)
    rdelay = random.randint(e, f)
    if a == 1:
        packet = f'({a},{b},{rint},{rdelay - 5})'
        ser.write(packet.encode())
        print(f'({a},{b},{rint},{rdelay})')
        sleep(rint / 1000)
        sleep(rdelay / 1000)
    else:
        packet = f'({a},{b},{rint - 5},{rdelay})'
        ser.write(packet.encode())
        print(f'({a},{b},{rint})')
        sleep(rint / 1000)





def stkey():
    global xy
    def atkctrl():
        nonlocal swcont, wcont
        radm = random.randint(0, 20)
        if swcont >= 2:
            wcont += 1
            if radm >= 19:
                send(leftk, 20, 30, a=2)
                send(altk, e=41, f=70)
                send(altk, e=20, f=30)
                send(leftk, 41, 70, a=3)
                send('w', e=560, f=630)

            else:
                send(leftk, 20, 30, a=2)
                send(altk, e=41, f=70)
                send(altk, e=20, f=30)
                send(leftk, 41, 70, a=3)
                send(altk, e=41, f=70)
                send('w', e=560, f=630)

            if wcont >= 3:
                wcont = 0
                swcont = 0
        else:
            if radm >= 19:
                send(leftk, 20, 30, a=2)
                send(altk, e=41, f=70)
                send(altk, e=20, f=30)
                send(leftk, 41, 70, a=3)
                send(ctrlk, e=560, f=630)

            else:
                send(leftk, 20, 30, a=2)
                send(altk, e=41, f=70)
                send(altk, e=20, f=30)
                send(leftk, 41, 70, a=3)
                send(altk, e=41, f=70)
                send(ctrlk, e=560, f=630)

    swcont = 0
    while True:
        swcont += 1
        wcont = 0
        send(96, e=900, f=930)
        send('d', e=40, f=60)
        send('d', e=600, f=620)
        send(rightk, 41, 70, a=2)
        send('s', e=40, f=60)
        send('s', e=250, f=280)
        send(rightk, 30, 50, a=3)
        send('a', e=40, f=60)
        send('a', e=400, f=500)

        send(altk, e=41, f=70)
        send(altk, e=41, f=70)
        send(ctrlk, e=560, f=630)

        send(altk, e=41, f=70)
        send(altk, e=41, f=70)
        send(ctrlk, e=560, f=590)
        send(118, e=101, f=150)

        send(rightk, 21, 41, a=2)
        send(upk, 21, 41, a=2)
        send('x', 120, 160, a=2)
        send('x', 21, 41, a=3)
        send(rightk, 21, 41, a=3)
        send(upk, 171, 210, a=3)
        send('x', e=300, f=350)

        radm = random.randint(0, 2)
        if radm == 1:
            send(altk, e=41, f=60)

        send('e', e=800, f=900)
        send(downk, 41, 60, a=2)

        radm = random.randint(0, 2)
        if radm == 1:
            send(altk, e=41, f=70)

        send(altk, e=41, f=70)
        send(downk, e=530, f=580)

        send(leftk, 41, 60, a=2)
        send('a', e=41, f=60)
        send(leftk, 170, 220, a=3)

        send('s', e=550, f=650)

        while xy[0][0] - 33 >= 31:
            atkctrl()

            if xy[0][0] - 33 >= 3:
                send("l")



def main():
    scmct = Thread(target=scmc)
    scmct.daemon = True
    scmct.start()
    stkey()

if __name__ == '__main__':
    main()
