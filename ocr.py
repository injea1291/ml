import time
import pytesseract
from cls import *


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

ser = serial.Serial(
    port='COM3',
    baudrate=9600, timeout=0
)

hwnd = win32gui.FindWindow(None, 'MapleStory')
left, top, right, bot = win32gui.GetWindowRect(hwnd)
if right - left < 900:
    hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
mo = Mouse(left, top,ser)
key = Keyboard(ser)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esck, spacek, bsk, tabk, returnk = 130, 129, 128, 216, 215, 218, 217, 177, 32, 8, 179, 176


fili = [fi(None, 506, 510, 323, 333), fi(None, 476, 750, 558, 559), fi(None, 625, 660, 113, 123),
        fi(None, 1274, 1275, 367, 368)]
fili[0].pixli.append([[255, 255, 255], [255, 255, 255]])
fili[1].pixli.append([[255, 255, 255], [255, 255, 255]])
fili[2].pixli.append([[68, 238, 255], [68, 238, 255]])
fili[3].pixli.append([[68, 238, 255], [68, 238, 255]])
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

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
