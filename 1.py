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



hwnd = win32gui.FindWindow(None, 'MapleStory')
left, top, right, bot = win32gui.GetWindowRect(hwnd)
if right - left < 900:
    hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)

altk, shiftk,  ctrlk, leftk, rightk, upk, downk, esc = 130, 129 , 128, 216, 215, 218, 217, 177
xy = [[], [], False, False, False, False]  # 캐릭터위치, 룬 위치, 룬/AI, 심, 채널
cren = []
lock = Lock()

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

while True:
    cren = creen()

    mxyi = match("r", cren, 86, 158, 12, 250)
    cv.imshow('asd', mxyi[3])
    cv.waitKey(1)
    print(mxyi[0:3])


def asdf():
    key(altk, 200, 240)
    key('c', 200, 240)
    key.p(rightk, 20, 40)
    key.p(upk, 20, 40)
    key.p('x', 650, 750)
    key.r(rightk)
    key.r(upk)
    key.r('x')
    key('x')
    key('x', 300, 350)
    key(ctrlk, 400, 450)
    key(shiftk)
    key(shiftk , 300,301)
    key.p(downk, 100, 140)
    key(altk, 80, 120)
    key(altk, 80, 120)
    key(altk, 500, 501)
    key(altk)
    key(altk)
    key(altk)
    key.r(downk)
    key('a')
    key('a')
    key('a')
    key('s')
    key('s', 400, 451)
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
        elif xy[0][0] >= 18 + 53:
            key.p(leftk, 20, 30)
            key(altk, 80, 110)
            key(altk)
            key(altk)
            key.r(leftk, 20, 30)
            key(ctrlk, 550, 551)
        elif xy[0][0] >= 7 + 53:
            key.p(leftk)
        else:
            key.ra()
            break
    key.p(leftk, 20, 40)
    key.p(upk, 20, 40)
    key.p('x', 650, 750)
    key.r(leftk)
    key.r(upk)
    key.r('x')
    key('x')
    key('x', 300, 350)