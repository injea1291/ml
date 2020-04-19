import cv2.cv2 as cv
from ctypes import windll
import win32gui
import win32ui
import numpy as np
import time
import random
import sys
import win32con



arli = list(range(4))
findt = False


def cir(*arowimage):
    a = 1
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

    for i in arowimage:
        b = random.randint(1, 1000000)

        mor = cv.morphologyEx(i, cv.MORPH_GRADIENT, kernel)
        morg = cv.cvtColor(mor, cv.COLOR_BGR2GRAY)
        circles = cv.HoughCircles(morg, cv.HOUGH_GRADIENT, 1, 37, param1=50, param2=35, minRadius=8, maxRadius=30)

        if circles is None:
            arli[a - 1] = 0
        else:

            circles = np.uint16(np.around(circles))
            x = circles[0, 0, 0] - circles[0, 0, 2]
            y = circles[0, 0, 1] - circles[0, 0, 2]
            cv.circle(i, (circles[0, 0, 0], circles[0, 0, 1]), circles[0, 0, 2], (0, 255, 0), 1)
            cv.circle(i, (circles[0, 0, 0], circles[0, 0, 1]), 2, (0, 0, 255), 3)
            cv.rectangle(i, (x, y), (x + circles[0, 0, 2] * 2, y + circles[0, 0, 2] * 2), (0, 0, 255))
            cv.imshow(f"{str(a)}", i)

            cr = 18
            morgcut = morg[circles[0, 0, 1] - cr:circles[0, 0, 1] + cr, circles[0, 0, 0] - cr:circles[0, 0, 0] + cr]

            cv.imwrite(f'c:\\ML2\\cvarow\\{b}.jpg', morgcut)
            cv.imshow(f"{str(a) * 2}", morgcut)
            arli[a - 1] = 1

        a += 1


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

if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, 'MapleStory')
    hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    if hwnd == 0:
        print("프로그램 찾지못함")
        sys.exit()
    img1 = np.zeros((85, 372, 3), np.uint8)
    bs = 701

    while True:
        img = creen()
        mxy = match("find", img, 100, 210, 395, 508, False)
        if mxy[0] > 0.6 and findt == False:
            findt = True
            x = 100 + mxy[2][1] + 55
            y = 400 + mxy[2][0] + 48
            img1 = img[x:x + 105, y:y + 5 + (4 * 93)].copy()
            cv.imwrite(f"images\\{bs}.jpg", img1)
            bs += 1
        elif mxy[0] < 0.7:
            findt = False

        print(mxy[0])

        cv.imshow('arowb', img1)
        cv.waitKey(1)
        time.sleep(0.5)
