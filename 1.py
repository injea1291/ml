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

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esc = 130, 129, 128, 216, 215, 218, 217, 177
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

class fi:
    def __init__(self, findimgname, sx, sy, ex, ey, masktf=True):

        self.sx, self.sy, self.ex, self.ey = sx, sy, ex, ey
        self.masktf = masktf
        self.find = cv.imread(f'dataimg\\{findimgname}.jpg', cv.IMREAD_GRAYSCALE)
        if self.masktf:
            self.ms = cv.imread(f'dataimg\\{findimgname}m.jpg', cv.IMREAD_GRAYSCALE)
        self.w, self.h = self.find.shape[::-1]

    def re(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sx:self.sy, self.ex:self.ey], cv.COLOR_BGR2GRAY)
        if self.masktf:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)
        else:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)
        mxy = list(mxy)

        return mxy

    def rei(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sx:self.sy, self.ex:self.ey], cv.COLOR_BGR2GRAY)
        if self.masktf:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)
        else:
            res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)
        mxy = maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc), cutimgy
        mxy = list(mxy)
        return mxy

mali = [[86, 171, 12, 214, 33, 69], [86, 158, 12, 250, 92, 54]]
ma = mali[1]
fili = list(range(7))
fili[0] = fi("i", ma[0], ma[1], ma[2], ma[3])
fili[1] = fi("sb", 712, 750, 1100, 1400, False)
fili[2] = fi("r", ma[0], ma[1], ma[2], ma[3])
fili[3] = fi("y", ma[0], ma[1], ma[2], ma[3], False)
fili[4] = fi("g", ma[0], ma[1], ma[2], ma[3], False)
fili[5] = fi("lie", 300, 580, 1000, 1366)
fili[6] = fi("b", 65, 85, 580, 650, False)

def scmc():
    global xy, beep, cren
    stimety, stime = [True, True], [0, 0]
    resul = list(range(len(fili)))

    while True:
        cren = creen()
        for e, i in enumerate(fili):
            resul[e] = i.rei(cren)
        print(resul[0][:3])



scmc()
