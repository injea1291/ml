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

while True:
    img = cr()
    max_val, max_loc, w, h, cutim = match("i", 87, 171, 12, 214)
    if max_val > 0.99:
        ix, iy = max_loc[0] + w / 2, max_loc[1] + h / 2
        print(ix)