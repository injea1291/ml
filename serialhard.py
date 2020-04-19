import serial
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
left, top, right, bot = win32gui.GetWindowRect(hwnd)
if right - left < 900:
    hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esc = 130, 129, 128, 216, 215, 218, 217, 177
xy = [[], [], False, False, False, False]  # 캐릭터위치, 룬 위치, 룬/AI, 심, 채널
cren = []
lock = Lock()


class findRhun(Exception):
    pass


class findBoss(Exception):
    pass


class stopmove(Exception):
    pass


class Keyboard:
    def __init__(self):
        self.KeyValue, self.status, self.wait, self.raseof = 0, 0, False, True

    def __call__(self, KeyValue, es=40, ee=70, ss=40, se=70):
        s, e = self.SendPacket(1, KeyValue, ss, se, es, ee)
        print(f'(KeyBoard.Write : {KeyValue}, {s}, {e})')
        sleep(s / 1000)
        sleep(e / 1000)

    def SendPacket(self, status, KeyValue, ss, se, es=40, ee=70):
        if self.raseof:
            if xy[4]:
                raise findBoss
            elif xy[2]:
                raise findRhun
            elif xy[5]:
                raise stopmove
        if self.status == 2 and self.wait:
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
        self.status = 4
        packet = f'({4},{self.KeyValue},{e - 5},{e})'
        ser.write(packet.encode())
        print(f'KeyBoard.ReleaseAll')
        sleep(e / 1000)

    def change(self, raseof):
        self.raseof = raseof


key = Keyboard()
beep = Thread(target=winsound.Beep, args=(300, 3000,))


def detect(cfg,
           names,
           weights,
           images,
           img_size=416,
           conf_thres=0.3,
           iou_thres=0.6,
           zoom=1):
    xyli = []
    device = torch_utils.select_device()
    model = Darknet(cfg, img_size)
    attempt_download(weights)
    model.load_state_dict(torch.load(weights, map_location=device)['model'])
    model.to(device).eval()

    # dataset = LoadImages(source, img_size=img_size)
    img = letterbox(images, new_shape=img_size)[0]
    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    # ------------------------------------------------

    classes = load_classes(names)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img)[0]

    pred = non_max_suppression(pred, conf_thres, iou_thres, multi_label=False, classes=None, agnostic=False)

    for i, det in enumerate(pred):  # detections image
        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], images.shape).round()

            for *xyxy, conf, cls in det:
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
    global xy, beep, cren
    stimety, stime, xytf = [True, True], [0, 0], [0, 0]
    while True:
        cren = creen()
        mxyi = match("i", cren, ma[0], ma[1], ma[2], ma[3])
        mxysb = match("sb", cren, 712, 750, 1100, 1400, False)
        mxyr = match("r", cren, ma[0], ma[1], ma[2], ma[3])
        mxyy = match("y", cren, ma[0], ma[1], ma[2], ma[3], False)
        mxyg = match("g", cren, ma[0], ma[1], ma[2], ma[3], False)
        mxylie = match("lie", cren, 200, 720, 300, 1366)
        mxybs = match("b", cren, 65, 85, 580, 650, False)
        if mxyi[0] > 0.99:
            xy[0] = mxyi[1][0:2]
            if xy[0] == xytf:
                if stimety[1]:
                    stime[1] = time.time()
                    stimety[1] = False
                elif time.time() - stime[1] > 10:

                    xy[5] = True
                    print(xy[5])
            else:
                stimety[1] = True
            xytf = xy[0]

        if mxysb[0] > 0.9:
            lock.acquire()
            xy[3] = True
            lock.release()
        if mxyr[0] > 0.999 and not math.isinf(mxyr[0]):
            xy[1] = mxyr[1]
            lock.acquire()
            xy[2] = True
            lock.release()
            cv.imshow('asd', mxyr[3])
            cv.moveWindow('asd', 10, 200)
        if mxyy[0] > 0.65 or mxyg[0] > 0.8:
            if stimety[0]:
                stime[0] = time.time()
                stimety[0] = False
            elif time.time() - stime[0] > 5 and not beep.is_alive():
                print('사람')
                beep = Thread(target=winsound.Beep, args=(300, 3000,))
                beep.start()
        else:
            stimety[0] = True

        if mxylie[0] > 0.99 and not math.isinf(mxylie[0]) and not beep.is_alive():
            beep = Thread(target=winsound.Beep, args=(300, 3000,))
            beep.start()

        if mxybs[0] > 0.6:
            # beep = Thread(target=winsound.Beep, args=(300, 3000,))
            # beep.start()
            lock.acquire()
            xy[4] = True
            lock.release()
        cv.waitKey(1)


def goto(x, y, z=3):
    key.ra()
    while True:
        if xy[0][0] - x >= 40:
            key.p(leftk)
            key(altk)
            key(altk)
            key.ra()
        elif x - xy[0][0] >= 40:
            key.p(rightk)
            key(altk)
            key(altk)
            key.ra()
        elif xy[0][0] - x >= z:
            key.p(leftk, wait=True)
        elif x - xy[0][0] >= z:
            key.p(rightk, wait=True)
        elif xy[0][1] > y + 7:
            key(altk, 100, 130)
            key(96, 3000, 3100)
        elif xy[0][1] < y - 7:
            key.p(upk, 20, 40)
            key.p(downk)
            key(altk)
            key.r(upk, 20, 40)
            key.r(downk, 1000, 1100)
        else:
            break


def useai():
    global xy, beep, cren
    stime = time.time()
    while True:
        time.sleep(1)
        if time.time() - stime > 5 and not xy[2]:
            lieimg = cren.copy()
            lieli = detect('cfg\\yolov3-spp-2cls.cfg', 'data\\lie.names', 'weights\\lie.pt', lieimg)
            if lieli:
                print(lieli)
                cv.imwrite(f'{time.time()}.jpg', lieimg)
                if not beep.is_alive():
                    beep = Thread(target=winsound.Beep, args=(300, 3000,))
                    beep.start()
            stime = time.time()
            print('end gpu')


mali = [[86, 171, 12, 214, 33, 69], [86, 158, 12, 250, 23, 18]]
ma = mali[1]


def stkey():
    global xy, beep, cren
    fstart = False
    swcont = 0

    def caden():
        nonlocal swcont
        swcont += 1

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
                    key('w', 450, 490)

                else:
                    key.p(leftk, 20, 30)
                    key(altk)
                    key(altk, 20, 30)
                    key.r(leftk)
                    key(altk)
                    key('w', 450, 490)
            else:
                if radm >= 19:
                    key.p(leftk, 20, 30)
                    key(altk)
                    key(altk, 20, 30)
                    key.r(leftk)
                    key(ctrlk, 550, 580)

                else:
                    key.p(leftk, 20, 30)
                    key(altk)
                    key(altk, 20, 30)
                    key.r(leftk)
                    key(altk)
                    key(ctrlk, 490, 520)

        key.ra(200, 400)
        key(leftk)
        key(96, 900, 930)
        key('d', 40, 60)
        key('d', 520, 540)
        key.p(rightk)
        key('s', 40, 60)
        key('s', 270, 290)
        key.r(rightk, 30, 50)
        key('a', 40, 60)
        key('a', 400, 550)

        while xy[0][0] < 125:
            key(altk)
            key(altk)
            key(ctrlk, 580, 600)

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
        key.r(downk, 520, 540)

        key.p(leftk, 41, 60)
        key('a', 210, 240)
        key('s', 550, 610)
        key.r(leftk, 41, 60)
        wcont = 0
        while True:
            if xy[3]:
                key(194, 1000, 1100)
                key(213, 750, 800)
                xy[3] = False
            elif xy[0][0] >= 31 + 33:
                atkctrl()
            elif xy[0][0] >= 10 + 33:
                key.p(leftk, 5, 5)
            else:
                if wcont >= 1:
                    swcont = 0
                key.r(leftk, 5, 5)
                break

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

        key.p(downk, 41, 60)

        radm = random.randint(0, 2)
        if radm == 1:
            key(altk, 41, 70)

        key(altk, 41, 70)
        key.r(downk, 530, 580)

        key.p(lr, 1200, 1300)
        key.r(lr)

    def caden2():

        while xy[0][0] < 90:
            if xy[0][1] >= 25:
                goto(ma[4], ma[5])
            if xy[0][0] >= 20:
                key.p(leftk, wait=True)
            elif xy[0][0] <= 16:
                key.p(rightk, wait=True)
            s = random.randint(40, 70)
            e = random.randint(40, 70)
            packet = f'(1,218,{s - 5},{e})'
            ser.write(packet.encode())
            print(f'(KeyBoard.Write : 218, {s}, {e})')
            sleep(s / 1000)
            sleep(e / 1000)

        key.ra()
        key(rightk, 150, 180)
        key(altk, 200, 240)
        key('c', 130, 170)
        key.p(rightk, 20, 40)
        key.p(upk, 20, 40)
        key.p('x', 400, 501)
        key.r(rightk)
        key.r(upk)
        key.r('x')
        key('x')
        key('x', 300, 350)
        key(ctrlk, 400, 450)
        key(shiftk)
        key(shiftk, 300, 351)
        radm = random.randint(0, 1)
        if radm == 0:
            key.p(upk, 30, 50)
            key.p(downk, 100, 140)
            key(altk, 80, 120)
            key(altk, 80, 120)
            key(altk, 500, 550)
            key(altk)
            key(altk)
            key(altk)
            key.r(upk, 30, 50)
            key.r(downk)

        else:
            key.p(upk, 30, 50)
            key.p(downk, 100, 140)
            key(altk, 80, 120, 1000, 1050)
            key.r(upk, 30, 50)
            key.r(downk)

        key('a')
        key('a')
        key('s')
        key('s', 400, 451)
        radm = random.randint(0, 1)
        if radm == 0:
            key(altk)
        key.p(upk)
        key('e')
        key('e')
        key.r(upk, 500, 551)
        key.p(leftk)
        key(altk)
        key(altk)
        key.r(leftk)
        key(ctrlk, 700, 750)
        while True:
            if xy[3]:
                key(194, 1000, 1100)
                key(213, 750, 800)
                xy[3] = False
            elif xy[0][0] >= 25 + 45:
                key.p(leftk, 20, 40)
                key(altk, 110, 140)
                key(altk)
                key(altk)
                key.r(leftk, 20, 40)
                key(ctrlk, 550, 590)
            elif xy[0][0] >= 7 + 45:
                key.p(leftk)
            else:
                key.ra()
                break

        key(altk)
        key.p(leftk, 20, 40)
        key.p(upk, 20, 40)
        key.p('x')
        key.r(leftk)
        key.r(upk, 400, 501)
        key.r('x')
        key('x')
        key('x', 300, 351)
        key('a')
        key('a', 300, 351)
        key.p(rightk)
        key('f', 40, 70, 80, 110)
        key.r(rightk)

    while True:
        try:
            key.change(True)
            caden2()
        except findRhun:
            key.change(False)
            time.sleep(1)
            goto(xy[1][0], xy[1][1])
            key(32, 500, 550)
            img = cren.copy()
            mxy = match("find", img, 100, 210, 395, 508, False)
            print(mxy[0])
            if mxy[0] > 0.6:
                x = 100 + mxy[2][1] + 55
                y = 400 + mxy[2][0] + 48
                cv.imwrite(f'r{time.time()}.jpg', img[x:x + 105, y:y + 5 + (4 * 93)])
                labelli = detect('cfg\\yolov3-spp-4cls.cfg', 'data\\arrow.names', 'weights\\arrow.pt',
                                 img[x:x + 105, y:y + 5 + (4 * 93)])
                print(labelli)
                if len(labelli) == 4:
                    for i in labelli:
                        sleep(0.5)
                        key(eval(i[0][:-5] + 'k'))
                    goto(ma[4], ma[5])
            else:
                goto(ma[4], ma[5])

            xy[2] = False
        except findBoss:

            xy[2] = True
            key.change(False)
            if fstart:
                key(esc)
                key(176)
                key(rightk, 200, 300)
                key(176, 100, 150)
                key(176, 5000, 5100)
            findplayer = True

            while True:
                cheak = match('ye', cren, 742, 790, 790, 840, False)
                if cheak[0] > 0.98:
                    stime = time.time()
                    while time.time() - stime < 4:
                        player = match("y", cren, ma[0], ma[1], ma[2], ma[3], False)
                        if player[0] > 0.64:
                            key(esc)
                            key(176)
                            key(rightk, 200, 300)
                            key(176, 100, 150)
                            key(176, 2000, 2100)
                            findplayer = True
                            break
                        else:
                            findplayer = False

                    if not findplayer:
                        break
            goto(ma[4], ma[5])
            xy[2] = False
            xy[4] = False
            fstart = True
        except stopmove:

            key.change(False)
            key(esc)
            goto(ma[4], ma[5])
            xy[5] = False


def main():
    beep.start()
    scmct = Thread(target=scmc, daemon=True)
    useait = Thread(target=useai, daemon=True)
    scmct.start()
    useait.start()
    sleep(1)
    stkey()


main()
