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

ser = serial.Serial(
    port='COM4',
    baudrate=9600, timeout=0
)

hwnd = win32gui.FindWindow(None, 'MapleStory')
hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
if hwnd == 0:
    print("프로그램 찾지못함")
    sys.exit()

altk = 130
ctrlk = 128
leftk = 216
rightk = 215
upk = 218
downk = 217
xy = [[], [], False, False, True]
lock = Lock()


class Keyboard():
    def __init__(self):
        self.KeyValue, self.status, self.wait = 0, 0, False

    def __call__(self, KeyValue, es=40, ee=70, ss=40, se=70):
        s, e = self.SendPacket(1, KeyValue, ss, se, es, ee)
        print(f'(KeyBoard.Write : {KeyValue}, {s}, {e})')
        sleep(s / 1000)
        sleep(e / 1000)

    def SendPacket(self, status, KeyValue, ss, se, es=40, ee=70):
        if xy[2]:
            raise
        if self.status == 2 and self.wait == True:
            self.ra()
            self.wait = False
        if type(KeyValue) == str:
            self.KeyValue = ord(KeyValue)
        else:
            self.KeyValue = KeyValue
        self.status = status
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'({status},{self.KeyValue},{s - 5},{e})'
        ser.write(packet.encode())
        return s, e

    def p(self, KeyValue, es=40, ee=70, wait=False):
        if self.KeyValue != KeyValue or self.status != 2:
            s, e = self.SendPacket(2, KeyValue, ss=es, se=ee)
            self.wait = wait
            print(f'(KeyBoard.Press : {KeyValue},{s})')
            sleep(s / 1000)
        else:
            e = random.randint(es, ee)
            sleep(e / 1000)

    def r(self, KeyValue, es=40, ee=70):
        s, e = self.SendPacket(3, KeyValue, ss=es, se=ee)
        print(f'(KeyBoard.release : {KeyValue},{s})')
        sleep(s / 1000)

    def ra(self, es=40, ee=70):
        e = random.randint(es, ee)
        packet = f'({4},{self.KeyValue},{e - 5},{e})'
        ser.write(packet.encode())
        print(f'KeyBoard.ReleaseAll')
        sleep(e / 1000)


key = Keyboard()
beep = Thread(target=winsound.Beep, args=(300, 3000,))


def detect(cfg,
           data,
           weights,
           images,
           img_size=608,
           conf_thres=0.5,
           nms_thres=0.5,
           zoom=1):
    xyli = []
    device = torch_utils.select_device()
    torch.backends.cudnn.benchmark = False
    model = Darknet(cfg, img_size)
    model.load_state_dict(torch.load(weights, map_location=device)['model'])
    model.to(device).eval()
    img, *_ = letterbox(images, new_shape=img_size)
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img, dtype=np.float32)
    img /= 255.0
    classes = load_classes(parse_data_cfg(data)['names'])
    img = torch.from_numpy(img).unsqueeze(0).to(device)
    pred, _ = model(img)
    det = non_max_suppression(pred.float(), conf_thres, nms_thres)[0]
    if det is not None and len(det) > 0:
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], images.shape).round()
        for *xyxy, conf, cls_conf, cls in det:
            label = '%s %.2f' % (classes[int(cls)], conf)
            xyxy[0:4] = list(map(lambda a: int(a) * zoom, xyxy[0:4]))
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


def scmc():
    global xy, beep
    stimety, stime = True, 0
    while True:
        img = creen()
        mxyi = match("i", img, 87, 171, 12, 214)
        mxysb = match("sb", img, 712, 750, 1100, 1400, False)
        mxyr = match("r", img, 87, 171, 12, 214)
        mxyy = match("y", img, 87, 171, 12, 214, False)
        mxyg = match("g", img, 87, 171, 12, 214, False)
        mxylie = match("lie", img, 200, 720, 300, 1366)

        if mxyi[0] > 0.99:
            xy[0] = mxyi[1][0:2]
        if mxysb[0] > 0.9:
            lock.acquire()
            xy[3] = True
            lock.release()
        if mxyr[0] > 0.999 and not math.isinf(mxyr[0]) and xy[4]:
            xy[1] = mxyr[1]
            lock.acquire()
            xy[2] = True
            xy[4] = False
            lock.release()
            cv.imshow('asd', mxyr[3])
            cv.moveWindow('asd', 10, 200)
        if mxyy[0] > 0.65 or mxyg[0] > 0.8:
            if stimety == True:
                stime = time.time()
                stimety = False
            elif time.time() - stime > 5 and not beep.is_alive():
                beep = Thread(target=winsound.Beep, args=(300, 3000,))
                beep.start()
            else:
                print(time.time() - stime)
        else:
            stimety = True

        if mxylie[0] > 0.99 and not beep.is_alive() and not math.isinf(mxylie[0]):
            print(mxylie[0])
            beep = Thread(target=winsound.Beep, args=(300, 3000,))
            beep.start()
            cv.imshow('asd1', mxylie[3])
            cv.moveWindow('asd1', 10, 300)
        cv.waitKey(1)


def goto():
    while True:
        if xy[0][0] - xy[1][0] >= 40:
            key.p(leftk)
            key(altk)
            key(altk)
            key.ra()
        elif xy[1][0] - xy[0][0] >= 40:
            key.p(rightk)
            key(altk)
            key(altk)
            key.ra()
        elif xy[0][0] - xy[1][0] >= 3:
            key.p(leftk, wait=True)
        elif xy[1][0] - xy[0][0] >= 3:
            key.p(rightk, wait=True)
        elif xy[0][1] > xy[1][1] + 7:
            key(altk, 100, 130)
            key(96, 3000, 3100)
        elif xy[0][1] < xy[1][1] - 7:
            key.p(downk)
            key(altk)
            key.ra(1000, 1100)
        else:
            break


def useai():
    global xy, beep
    stime = time.time()
    while True:
        time.sleep(1)
        if time.time() - stime > 5 and xy[4] == True:
            lieimg = creen()
            lieli = detect('cfg\\lie.cfg', 'data\\lie.data', 'weights\\lie8.pt', lieimg)
            if lieli:
                print(lieli)
                cv.rectangle(lieimg, (lieli[0][1], lieli[0][2]), (lieli[0][3], lieli[0][4]), (0, 0, 0))
                cv.imwrite(f'{time.time()}.jpg', lieimg)
                if not beep.is_alive():
                    beep = Thread(target=winsound.Beep, args=(300, 3000,))
                    beep.start()
            stime = time.time()


def stkey():
    global xy, beep
    swcont = 0

    def atkctrl():
        nonlocal swcont, wcont
        radm = random.randint(0, 20)
        if swcont >= 2 and wcont <= 2:
            wcont += 1
            if radm >= 19:
                key.p(leftk, 20, 30)
                key(altk)
                key(altk, 20, 30)
                key.r(leftk)
                key('w', 560, 630)

            else:
                key.p(leftk, 20, 30)
                key(altk)
                key(altk, 20, 30)
                key.r(leftk)
                key(altk)
                key('w', 560, 630)
        else:
            if radm >= 19:
                key.p(leftk, 20, 30)
                key(altk)
                key(altk, 20, 30)
                key.r(leftk)
                key(ctrlk, 560, 630)

            else:
                key.p(leftk, 20, 30)
                key(altk)
                key(altk, 20, 30)
                key.r(leftk)
                key(altk)
                key(ctrlk, 560, 630)

    while True:
        try:
            swcont += 1
            key.ra(200, 400)
            key(96, 900, 930)
            key('d', 40, 60)
            key('d', 600, 620)
            key.p(rightk)
            key('s', 40, 60)
            key('s', 250, 280)
            key.r(rightk, 30, 50)
            key('a', 40, 60)
            key('a', 400, 500)

            key(altk)
            key(altk)
            key(ctrlk, 560, 630)

            key(altk)
            key(altk)
            key(ctrlk, 560, 590)
            key(118, 101, 150)

            key.p(rightk, 21, 41)
            key.p(upk, 21, 41)
            key.p('x', 120, 160)
            key.r('x', 21, 41)
            key.r(rightk, 21, 41)
            key.r(upk, 171, 210)
            key('x', 300, 350)

            radm = random.randint(0, 2)
            if radm == 1:
                key(altk, 41, 60)

            key('e', 800, 900)
            key.p(downk, 41, 60)

            radm = random.randint(0, 2)
            if radm == 1:
                key(altk, 41, 70)

            key(altk, 41, 70)
            key.r(downk, 530, 580)

            key.p(leftk, 41, 60)
            key('a', 210, 280)
            key('s', 550, 650)
            key.r(leftk, 41, 60)
            wcont = 0
            while True:
                if xy[3]:
                    key(198, 1000, 1100)
                    key(213, 700, 800)
                    xy[3] = False
                elif xy[0][0] - 33 >= 29:
                    atkctrl()
                elif xy[0][0] - 33 >= 10:
                    key.p(leftk, 5, 5)
                else:
                    if wcont >= 1:
                        swcont = 0
                    key.r(leftk, 5, 5)
                    break
        except:
            xy[2] = False
            print(xy)
            goto()
            key(32, 500, 550)
            img = creen()
            print(img.shape)
            mxy = match("find", img, 100, 210, 395, 508, False)
            print(mxy[0])
            if mxy[0] > 0.6:
                x = 100 + mxy[2][1] + 55
                y = 400 + mxy[2][0] + 48
                labelli = detect('cfg\\arrow.cfg', 'data\\arrow.data', 'weights\\arrow.pt',
                                 img[x:x + 105, y:y + 5 + (4 * 93)], 608, 0.5, 0.3)
                print(labelli)
                if len(labelli) == 4:
                    for i in labelli:
                        sleep(0.5)
                        key(eval(i[0][:-5] + 'k'))
            xy[4] = True


def zero(lr):
    def dob(keyV, d1, d2):
        key(keyV, 41, 70)
        key(keyV, 41, 70)
        key(keyV, d1, d2)

    radm = random.randint(1, 101)
    if radm <= 20:
        key('v', 450, 500)
        key('v', 450, 500)
        key('v', 450, 490)
    elif radm >= 60:
        key('v', 41, 70)
        key.p('v', 40, 70)
        key.r('v', 350, 400)

        key('v', 41, 70)
        key.p('v', 40, 70)
        key.r('v', 350, 400)

        key('v', 41, 70)
        key.p('v', 40, 70)
        key.r('v', 350, 390)
    else:
        key.p('v', 1450, 1500)
        key.r('v')

    dob(upk, 41, 70)

    key(altk, 41, 70)
    key(altk, 41, 70)
    key(altk, 70, 100)
    radm = random.randint(0, 2)
    if radm == 0:
        key('c', 870, 920)
        key('c', 870, 920)
    else:
        key('c', 1650, 1700)

    key('s', 650, 700)

    key(altk, 41, 70)
    key(altk, 41, 70)
    key(altk, 160, 190)
    dob(lr, 200, 250)
    key('s', 40, 70)
    radm = random.randint(0, 4)
    if radm == 0:
        key(ctrlk, 40, 70)
        key(ctrlk, 41, 70)
    else:
        key(ctrlk, 41, 70)

    key.p(lr, 140, 180)

    key.p(upk, 51, 70)
    key.p(downk, 50, 70)
    key.p(altk, 51, 70)
    key.r(upk, 30, 50)
    key.r(lr, 30, 50)
    key.r(downk, 30, 50)
    key.r(altk, 1300, 1400)

    key.p(lr, 1200, 1300)
    key.r(lr)


sleep(1)


scmct = Thread(target=scmc, daemon=True)
useait = Thread(target=useai, daemon=True)
scmct.start()
useait.start()
stkey()
