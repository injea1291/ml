import sys
import math
import serial
import random
import time
from time import sleep
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
import numpy as np
from threading import Thread, Lock
import winsound
from models import *
from utils.datasets import *
from utils.utils import *

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
xy = [[0, 0], [0, 0], False, False]
lock = Lock()


def beep():
    winsound.Beep(262, 2000)


def detect(cfg,
           data,
           weights,
           images,
           img_size=416,
           conf_thres=0.5,
           nms_thres=0.5):
    xyli, labli = [], []
    device = torch_utils.select_device()
    torch.backends.cudnn.benchmark = False
    model = Darknet(cfg, img_size)
    model.load_state_dict(torch.load(weights, map_location=device)['model'])
    model.to(device).eval()
    dataloader = LoadImages(images, img_size=img_size, half=False)
    classes = load_classes(parse_data_cfg(data)['names'])
    for i, (path, img, im0, vid_cap) in enumerate(dataloader):
        img = torch.from_numpy(img).unsqueeze(0).to(device)
        pred, _ = model(img)
        det = non_max_suppression(pred.float(), conf_thres, nms_thres)[0]
        if det is not None and len(det) > 0:
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls_conf, cls in det:
                label = '%s %.2f' % (classes[int(cls)], conf)
                xyxy[0:4] = list(map(lambda a: int(a) * 4, xyxy[0:4]))
                xyli.append([label, xyxy[0], xyxy[1], xyxy[2], xyxy[3]])
            xyli.sort(key=lambda xyli: xyli[1])
    return xyli


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

    mxy = maxloc[0] + w / 2, maxloc[1] + h / 2, maxloc
    mxy = list(mxy)
    return maxval, mxy, cutim


def scmc():
    global xy
    stimety, stime, beept = True, 0, Thread(target=beep, daemon=True)
    while True:
        img = creen()
        maxval, mxy, cutim = match("i", img, 87, 171, 12, 214)
        maxval1, mxy1, cutim1 = match("r", img, 87, 171, 12, 214)
        maxvalsb, mxysb, cutsb = match("sb", img, 712, 750, 1100, 1400, False)
        maxvaly, mxyy, cuty = match("y", img, 87, 171, 12, 214, False)
        if maxvalsb > 0.9:
            lock.acquire()
            xy[2] = True
            lock.release()
        if maxval > 0.99:
            xy[0] = mxy[0:2]
            cv.imshow('asd1', cutim)
            cv.moveWindow('asd1', 10, 10)
        if maxval1 > 0.999 and not math.isinf(maxval1):
            xy[1] = mxy1[0:2]
            lock.acquire()
            xy[3] = True
            lock.release()
            cv.imshow('asd', cutim1)
            cv.moveWindow('asd', 10, 200)
        if maxvaly > 0.65:
            if stimety == True:
                stime = time.time()
                stimety = False
            elif time.time() - stime > 5 and not beept.is_alive():
                beept = Thread(target=beep, daemon=True)
                beept.start()
            cv.imshow('asd2', cuty)
            cv.moveWindow('asd2', 10, 100)
        else:
            stimety = True
        print(xy)
        cv.waitKey(1)


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


def goto():
    tf = 0
    while True:
        if xy[0][0] - xy[1][0] >= 40:
            send(1, a=4)
            send(leftk, a=2)
            send(altk)
            send(altk)
            send(leftk, a=3)
            tf = 0
        elif xy[1][0] - xy[0][0] >= 40:
            send(1, a=4)
            send(rightk, a=2)
            send(altk)
            send(altk)
            send(rightk, a=3)
            tf = 0
        elif xy[0][0] - xy[1][0] >= 5:
            if tf != leftk:
                send(1, a=4)
                send(leftk, 5, 5, a=2)
                tf = leftk
        elif xy[1][0] - xy[0][0] >= 5:
            if tf != rightk:
                send(1, a=4)
                send(rightk, 5, 5, a=2)
                tf = rightk
        elif xy[0][1] > xy[1][1] + 7:
            send(1, a=4)
            send(altk, e=100, f=130)
            send(96, e=3000, f=3100)
            tf = 0
        elif xy[0][1] < xy[1][1] - 7:
            send(1, a=4)
            send(downk, a=2)
            send(altk)
            send(downk, 1000, 1100, a=3)
            tf = 0
        else:
            send(1, 500, 550, a=4)
            break


def stkey():
    global xy

    def atkctrl():
        nonlocal swcont, wcont
        radm = random.randint(0, 20)
        if swcont >= 2 and wcont <= 2:
            wcont += 1
            if radm >= 19:
                send(leftk, 20, 30, a=2)
                send(altk)
                send(altk, e=20, f=30)
                send(leftk, a=3)
                send('w', e=560, f=630)

            else:
                send(leftk, 20, 30, a=2)
                send(altk)
                send(altk, e=20, f=30)
                send(leftk, a=3)
                send(altk)
                send('w', e=560, f=630)
        else:
            if radm >= 19:
                send(leftk, 20, 30, a=2)
                send(altk)
                send(altk, e=20, f=30)
                send(leftk, a=3)
                send(ctrlk, e=560, f=630)

            else:
                send(leftk, 20, 30, a=2)
                send(altk)
                send(altk, e=20, f=30)
                send(leftk, a=3)
                send(altk)
                send(ctrlk, e=560, f=630)

    swcont = 0
    while True:
        swcont += 1
        send(1, 100, 200, a=4)
        send(96, e=900, f=930)
        send('d', e=40, f=60)
        send('d', e=600, f=620)
        send(rightk, a=2)
        send('s', e=40, f=60)
        send('s', e=250, f=280)
        send(rightk, 30, 50, a=3)
        send('a', e=40, f=60)
        send('a', e=400, f=500)

        send(altk)
        send(altk)
        send(ctrlk, e=560, f=630)

        send(altk)
        send(altk)
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
        send(downk, 530, 580, a=3)

        send(leftk, 41, 60, a=2)
        send('a', e=210, f=280)
        send('s', e=550, f=650)
        send(leftk, 41, 60, a=3)
        wcont = 0
        while True:
            if xy[3]:
                goto()
                send(32, e=500, f=550)
                img = creen()
                maxval, mxy, cutim = match("find", img, 100, 210, 395, 508, False)
                print(maxval)
                if maxval > 0.6:
                    x = 100 + mxy[2][1] + 55
                    y = 400 + mxy[2][0] + 48
                    cv.imwrite('tmp/image.jpg', img[x:x + 105, y:y + 5 + (4 * 93)])
                    labelli = detect('cfg\\arrow.cfg', 'data\\arrow.data', 'weights\\arrow.pt', 'tmp', 608, 0.5, 0.3)
                    if len(labelli) == 4:
                        for i in range(4):
                            sleep(0.5)
                            send(eval(labelli[i][0][:-5] + 'k'))
                xy[3] = False
            elif xy[2]:
                send(198, e=1000, f=1100)
                send(213, e=700, f=800)
                xy[2] = False
            elif xy[0][0] - 33 >= 29:
                atkctrl()
            elif xy[0][0] - 33 >= 10:
                send(leftk, 5, 5, a=2)
            else:
                if wcont >= 1:
                    swcont = 0
                send(leftk, 5, 5, a=3)
                break


sleep(1)
scmct = Thread(target=scmc, daemon=True)
scmct.start()
scmct.join()
