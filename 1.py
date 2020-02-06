import sys
import serial
import time
from time import sleep
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
from threading import Thread, Lock
import winsound
from models import *
from utils.datasets import *
from utils.utils import *

import random

hwnd = win32gui.FindWindow(None, 'MapleStory')
hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
if hwnd == 0:
    print("프로그램 찾지못함")
    sys.exit()

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
    img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    win32gui.DeleteObject(cbmp.GetHandle())
    cDC.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img


def match(a, img, b, c, d, e, f=True):
    img = img.copy()
    cutim = img[b:c, d:e]
    cutimgy = cv.cvtColor(cutim, cv.COLOR_BGR2GRAY)
    find = cv.imread(f'dataimg\\{a}.jpg', cv.IMREAD_GRAYSCALE)
    ms = cv.imread(f'dataimg\\{a}m.jpg', cv.IMREAD_GRAYSCALE)
    w, h = find.shape[::-1]
    if f:
        res = cv.matchTemplate(cutimgy, find, cv.TM_CCORR_NORMED, mask=ms)
    else:
        res = cv.matchTemplate(cutimgy, find, cv.TM_CCOEFF_NORMED)

    minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
    cv.rectangle(cutim, maxloc, (maxloc[0] + w, maxloc[1] + h), (255, 0, 0), 1)

    mxy = maxval, [maxloc[0] + w / 2, maxloc[1] + h / 2], list(maxloc), cutim
    mxy = list(mxy)

    return mxy

a,b,c,d = True, False, False, True

if (a and not b or c) and not d:
    print(1)