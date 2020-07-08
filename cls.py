import random
import serial
import cv2.cv2 as cv
from time import sleep
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
from ctypes import *
import os


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int),
                ("uc", POINTER(c_float)),
                ("points", c_int)]


class DETNUMPAIR(Structure):
    _fields_ = [("num", c_int),
                ("dets", POINTER(DETECTION))]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


hasGPU = True

cwd = os.path.dirname(__file__)
os.environ['PATH'] = cwd + ';' + os.environ['PATH']
winGPUdll = os.path.join(cwd, "yolo_cpp_dll.dll")
winNoGPUdll = os.path.join(cwd, "yolo_cpp_dll_nogpu.dll")
lib = CDLL(winGPUdll, RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

copy_image_from_bytes = lib.copy_image_from_bytes
copy_image_from_bytes.argtypes = [IMAGE, c_char_p]


def network_width(net):
    return lib.network_width(net)


def network_height(net):
    return lib.network_height(net)


predict = lib.network_predict_ptr
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

if hasGPU:
    set_gpu = lib.cuda_set_device
    set_gpu.argtypes = [c_int]

init_cpu = lib.init_cpu

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int), c_int]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_batch_detections = lib.free_batch_detections
free_batch_detections.argtypes = [POINTER(DETNUMPAIR), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict_ptr
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_net_custom = lib.load_network_custom
load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
load_net_custom.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

predict_image_letterbox = lib.network_predict_image_letterbox
predict_image_letterbox.argtypes = [c_void_p, IMAGE]
predict_image_letterbox.restype = POINTER(c_float)

network_predict_batch = lib.network_predict_batch
network_predict_batch.argtypes = [c_void_p, IMAGE, c_int, c_int, c_int,
                                  c_float, c_float, POINTER(c_int), c_int, c_int]
network_predict_batch.restype = POINTER(DETNUMPAIR)


def array_to_image(arr):
    import numpy as np
    # need to return old values to avoid python freeing memory
    arr = arr.transpose(2, 0, 1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
    data = arr.ctypes.data_as(POINTER(c_float))
    im = IMAGE(w, h, c, data)
    return im, arr


def detect_image(net, meta, custom_image_bgr, thresh=.5, hier_thresh=.5, nms=.45, debug=False):
    custom_image = cv.cvtColor(custom_image_bgr, cv.COLOR_BGR2RGB)
    custom_image = cv.resize(custom_image, (lib.network_width(net), lib.network_height(net)),
                             interpolation=cv.INTER_LINEAR)

    im, arr = array_to_image(custom_image)  # you should comment line below: free_image(im)
    num = c_int(0)
    if debug: print("Assigned num")
    pnum = pointer(num)
    if debug: print("Assigned pnum")
    predict_image(net, im)
    letter_box = 0
    # predict_image_letterbox(net, im)
    # letter_box = 1
    if debug: print("did prediction")
    dets = get_network_boxes(net, custom_image_bgr.shape[1], custom_image_bgr.shape[0], thresh, hier_thresh, None, 0,
                             pnum, letter_box)  # OpenCV

    if debug: print("Got dets")
    num = pnum[0]
    if debug: print("got zeroth index of pnum")
    if nms:
        do_nms_sort(dets, num, meta.classes, nms)
    if debug: print("did sort")
    res = []
    if debug: print("about to range")
    for j in range(num):
        if debug: print("Ranging on " + str(j) + " of " + str(num))
        if debug: print("Classes: " + str(meta), meta.classes, meta.names)
        for i in range(meta.classes):
            if debug: print("Class-ranging on " + str(i) + " of " + str(meta.classes) + "= " + str(dets[j].prob[i]))
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                if altNames is None:
                    nameTag = meta.names[i]
                else:
                    nameTag = altNames[i]
                if debug:
                    print("Got bbox", b)
                    print(nameTag)
                    print(dets[j].prob[i])
                    print((b.x, b.y, b.w, b.h))
                res.append((nameTag, dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    if debug: print("did range")
    res = sorted(res, key=lambda x: -x[1])
    if debug: print("did sort")
    free_detections(dets, num)
    if debug: print("freed detections")
    return res


netMain = None
metaMain = None
altNames = None
change = ""

def performDetect(image, configPath="./cfg/yolov4.cfg", weightPath="yolov4.weights", metaPath="./cfg/coco.data",
                  thresh=0.25, hier_thresh=.5, nms=.45, debug=False, showImage=False):
    # Import the global variables. This lets us instance Darknet once, then just call performDetect() again without instancing again
    global metaMain, netMain, altNames, change  # pylint: disable=W0603
    assert 0 < thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if netMain is None or change != weightPath:
        netMain = load_net_custom(configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
        metaMain = load_meta(metaPath.encode("ascii"))
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    change = weightPath
    detections = detect_image(netMain, metaMain, image, thresh, hier_thresh, nms, debug)
    detections.sort(key=lambda xyli: xyli[2][0])
    if showImage:

        for detection in detections:
            bounds = detection[2]
            # x = shape[1]
            # xExtent = int(x * bounds[2] / 100)
            # y = shape[0]
            # yExtent = int(y * bounds[3] / 100)
            yExtent = int(bounds[3])
            xEntent = int(bounds[2])
            # Coordinates are around the center
            xCoord = int(bounds[0] - bounds[2] / 2)
            yCoord = int(bounds[1] - bounds[3] / 2)
            boundingBox = [
                [xCoord, yCoord],
                [xCoord, yCoord + yExtent],
                [xCoord + xEntent, yCoord + yExtent],
                [xCoord + xEntent, yCoord]
            ]

            cv.rectangle(image, (xCoord, yCoord), (xCoord + xEntent, yCoord + yExtent), (255, 255, 255), 0)
        cv.imshow("23", image)

    return detections


class Keyboard:
    def __init__(self, ser):
        self.keyvalue, self.status, self.wait, self.raseof = 0, 0, False, True
        self.ser = ser

    def __call__(self, keyvalue, es=40, ee=70, ss=40, se=70):
        s, e = self.snedpacket(1, keyvalue, ss, se, es, ee)
        print(f'(KeyBoard.Write : {keyvalue}, {s}, {e})')
        sleep(s / 1000)
        sleep(e / 1000)

    def snedpacket(self, status, keyvalue, ss, se, es=40, ee=70):
        if self.status == 2 and self.wait:
            self.ra()
            self.wait = False
        if type(keyvalue) == str:
            self.keyvalue = ord(keyvalue)
        else:
            self.keyvalue = keyvalue
        self.status = status
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(0,{status},{self.keyvalue},{s - 5},{e})'
        self.ser.write(packet.encode())
        return s, e

    def p(self, keyvalue, es=40, ee=70, wait=False):
        if self.keyvalue != keyvalue or self.status != 2:
            s, e = self.snedpacket(2, keyvalue, ss=es, se=ee)
            self.wait = wait
            print(f'(KeyBoard.Press : {keyvalue},{s})')
            sleep(s / 1000)
        else:
            e = random.randint(es, ee)
            sleep(e / 1000)

    def r(self, keyvalue, es=40, ee=70):
        s, e = self.snedpacket(3, keyvalue, ss=es, se=ee)
        print(f'(KeyBoard.release : {keyvalue},{s})')
        sleep(s / 1000)

    def ra(self, es=40, ee=70):
        e = random.randint(es, ee)
        self.status = 4
        packet = f'(0,{4},{self.keyvalue},{e - 5},{e})'
        self.ser.write(packet.encode())
        print(f'KeyBoard.ReleaseAll')
        sleep(e / 1000)

    def change(self, raseof):
        self.raseof = raseof


class Mouse:
    def __init__(self, x, y, ser):
        self.x = x + 2
        self.y = y
        self.ser = ser

    def __call__(self, x, y, ss=40, se=70):
        x1, y1 = win32api.GetCursorPos()
        print(f'Mouse.goto : {x},{y}')
        self.m((x + self.x) - x1, (y + self.y) - y1, ss, se)

    def m(self, x, y, ss=40, se=70):
        def pm(a):
            if a > 0:
                return 1
            elif a == 0:
                return 0
            else:
                return -1

        x1, x2 = divmod(x, 127 if x > 0 else -127)
        y1, y2 = divmod(y, 127 if y > 0 else -127)
        x1 *= pm(x)
        y1 *= pm(y)
        for i in range(max(abs(x1), abs(y1))):
            packet = f'(1,2,{127 * pm(x1)},{127 * pm(y1)},1)'
            self.ser.write(packet.encode())
            x1 -= pm(x1)
            y1 -= pm(y1)
            sleep(6 / 1000)
        s = random.randint(ss, se)
        packet = f'(1,2,{x2},{y2},{s - 5})'
        self.ser.write(packet.encode())
        sleep(s / 1000)

    def c(self, es=40, ee=70, ss=40, se=70):
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(1,1,0,{s - 5},{e})'
        self.ser.write(packet.encode())
        print(f'Mouse.click : {s} {e}')
        sleep(s / 1000)
        sleep(e / 1000)


class fi:
    def __init__(self, findimgname, sx, ex, sy, ey, pixtf=False):
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.pixli = []
        if not findimgname is None:
            self.find = cv.imread(f'dataimg\\{findimgname}.png')
            self.w, self.h = self.find.shape[1::-1]
            if pixtf:
                self.pixli = fi.pixex(self.find)
            self.find = cv.cvtColor(self.find, cv.COLOR_BGR2GRAY)

    def setmaskimg(self, maskimg):
        self.ms = maskimg

    def re(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sy:self.ey, self.sx:self.ex], cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        # cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def remask(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sy:self.ey, self.sx:self.ex], cv.COLOR_BGR2GRAY)
        # mask match only can TM_SQDIFF and TM_CCORR_NORMED
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED, mask=self.ms)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def piximg(self, creenimg):
        cutimgy = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def pixpix(self, creenimg):
        w, h = self.ex - self.sx, self.ey - self.sy
        creenimg = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        for i in range(w):
            for e in range(h):
                if creenimg[e, i] == 255:
                    return [True, i, e]
        return False

    @staticmethod
    def inRange(img, rgb):
        img1 = cv.inRange(img, np.array(rgb[0][0]), np.array(rgb[0][1]))
        for i in rgb[1:]:
            img1 = cv.bitwise_or(img1, cv.inRange(img, np.array(i[0]), np.array(i[1])))
        return img1

    @staticmethod
    def pixex(img):
        pixli = []
        w, h = img.shape[1::-1]
        for i in range(w):
            for e in range(h):
                if not pixli.count([list(img[e, i]), list(img[e, i])]):
                    pixli.append([list(img[e, i]), list(img[e, i])])
        return pixli


def creen(hwnd):
    le, to, ri, bo = win32gui.GetWindowRect(hwnd)
    w = ri - le
    h = bo - to

    hdc = win32gui.GetWindowDC(hwnd)

    uihdc = win32ui.CreateDCFromHandle(hdc)

    cdc = uihdc.CreateCompatibleDC()
    cbmp = win32ui.CreateBitmap()
    cbmp.CreateCompatibleBitmap(uihdc, w - 4, h)

    cdc.SelectObject(cbmp)
    cdc.BitBlt((0, 0), (w, h), uihdc, (2, 0), win32con.SRCCOPY)
    signedintsarray = cbmp.GetBitmapBits(True)
    img = np.frombuffer(signedintsarray, dtype='uint8')
    img.shape = (h, w - 4, 4)
    img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    win32gui.DeleteObject(cbmp.GetHandle())
    cdc.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img

