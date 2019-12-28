import sys
import time
import random
import math
import serial
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
import numpy as np

import detect1

ser = serial.Serial(
    port='COM4',
    baudrate=9600, timeout=0
)


findt = False
hwnd = win32gui.FindWindow(None, 'MapleStory')
if hwnd == 0:
    print("프로그램 찾지못함")
    sys.exit()



def match(a, b, c, d, e, f=True):
    cutim = img[b:c, d:e]
    cutimg = cv.cvtColor(cutim, cv.COLOR_BGR2GRAY)
    find = cv.imread(f'{a}.jpg', cv.IMREAD_GRAYSCALE)
    ms = cv.imread(f'{a}m.jpg', cv.IMREAD_GRAYSCALE)
    w, h = find.shape[::-1]
    if f:
        res = cv.matchTemplate(cutimg, find, cv.TM_CCORR_NORMED, mask=ms)
    else:
        res = cv.matchTemplate(cutimg, find, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    cv.rectangle(cutim, max_loc, (max_loc[0] + w, max_loc[1] + h), (255, 0, 0), 1)

    return max_val, max_loc, w, h, cutim


def cr():
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hdc = win32gui.GetWindowDC(hwnd)

    uihdc = win32ui.CreateDCFromHandle(hdc)

    cDC = uihdc.CreateCompatibleDC()
    cbmp = win32ui.CreateBitmap()
    cbmp.CreateCompatibleBitmap(uihdc, w, h)

    cDC.SelectObject(cbmp)
    cDC.BitBlt((0, 0), (w, h), uihdc, (0,0), win32con.SRCCOPY)
    signedIntsArray = cbmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    win32gui.DeleteObject(cbmp.GetHandle())
    cDC.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img
def send(a):
    global op, sop
    op = a
    if sop != op:
        print(op)
        sop = op
        ser.write(op.encode())
max_val1 = 0
op, sop, res1 = "", "", ""
ix, iy, rx, ry = 0, 0, 0, 0
send("e")
send("a")
while True:
    img = cr()
    max_val, max_loc, w, h, cutim = match("i", 87, 171, 12, 214)
    if max_val > 0.99:
        ix, iy = max_loc[0] + w / 2, max_loc[1] + h / 2

    if max_val1 > 0.999 and not math.isinf(max_val1):
        cv.imshow('asd', cutim1)
        cv.moveWindow('asd', 10, 10)
        cv.waitKey(1)
        if ix - rx >= 40:
            send("j")
        elif rx - ix >= 40:
            send("k")
        elif ix - rx >= 5:
            send("l")
        elif rx - ix >= 5:
            send("r")
        else:
            if iy > ry + 7:
                max_val1, max_loc1, w1, h1, cutim1 = match("r", 87, 171, 12, 214)
                send("u")
                time.sleep(2)
                send("e")
            elif iy < ry - 7:
                send("d")
                time.sleep(1)
                send("e")
            else:
                send("s")
                time.sleep(1)
                img = cr()
                max_val2, max_loc2, w2, h2, cutim2 = match("find", 100, 210, 395, 508, False)
                print("글자찾",max_val2)
                if max_val2 > 0.6:
                    x = 100 + max_loc2[1] + 55
                    y = 400 + max_loc2[0] + 48
                    cv.imwrite('tmp/image.jpg', img[x:x + 105, y:y + 5 + (4 * 93)])
                    labelli = detect1.asd()
                    print(labelli)
                    if len(labelli) == 4:
                        for i in labelli:
                            time.sleep(0.5)
                            if i[0] == 'r':
                                send("0")
                            elif i[0] == 'l':
                                send("1")
                            elif i[0] == 'u':
                                send("2")
                            elif i[0] == 'd':
                                send("3")
                            send("e")
                        max_val1 = 0
                        while True:
                            img = cr()
                            max_val, max_loc, w, h, cutim = match("i", 87, 171, 12, 214)
                            if max_val > 0.98:
                                ix, iy = max_loc[0] + w / 2, max_loc[1] + h / 2

                            if ix >= 43:
                                send("j")
                            else:
                                max_val1, max_loc1, w1, h1, cutim1 = match("r", 87, 171, 12, 214)
                                break
                    else:
                        max_val1, max_loc1, w1, h1, cutim1 = match("r", 87, 171, 12, 214)
                        send("e")
                else:
                    max_val1, max_loc1, w1, h1, cutim1 = match("r", 87, 171, 12, 214)
                    send("e")

    else:
        max_val1, max_loc1, w1, h1, cutim1 = match("r", 87, 171, 12, 214)
        rx, ry = max_loc1[0] + w1 / 2, max_loc1[1] + h1 / 2
        res = ser.readline()

        if res.decode()[:-2] == '1':
            res1 = res.decode()[:-2]
            print(res1)
        if res1 == '1':
            maxvalsb, maxlocsb, wsb, hsb, cutsb = match("sb", 712, 750, 1100, 1400, False)
            if maxvalsb > 0.9:
                send("5")
            elif ix - 33 >= 40 :
                send("4")
            elif ix - 33 >= 3:
                send("l")
            else:

                send("e")
                send("a")
                res1 = ""

