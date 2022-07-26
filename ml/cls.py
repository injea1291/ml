import random
import cv2 as cv
import time
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
from ctypes import *
import os
import asyncio
import itertools
import winreg
import serial


class checkfps():
    def __init__(self):
        self.time = time.time()
        self.count = 0

    def print(self):
        try:
            self.count += 1
            print(self.count / (time.time() - self.time))
        except ZeroDivisionError:
            print("pass")
            pass


class hardhid:
    def __init__(self, ser):
        self.ser = ser


class Keyboard(hardhid):
    def __init__(self, ser):
        super().__init__(ser)
        self.keyvalue, self.status, self.wait = 0, 0, False

    def __call__(self, keyvalue, es=40, ee=70, ss=40, se=70):
        self.status = 1
        rd = random.randint(ss, se)
        ed = random.randint(es, ee)
        print(f'(KeyBoard.Write : {keyvalue},{rd},{ed})')
        self.ser(f"10{self.incoding(keyvalue)}")
        time.sleep(rd / 1000)
        self.ser(f"11{self.incoding(keyvalue)}")
        time.sleep(ed / 1000)

    def incoding(self, keyvalue):
        if type(keyvalue) is str:
            self.keyvalue = ord(keyvalue)
        else:
            self.keyvalue = keyvalue
        return self.keyvalue

    def p(self, keyvalue, s=40, e=70, wait=False):
        sd = random.randint(s, e)
        if self.keyvalue != keyvalue or self.status != 2:
            if self.wait:
                self.ra()
                self.wait = False
            self.status = 2
            self.wait = wait
            print(f'(KeyBoard.Press : {keyvalue},{sd})')
            self.ser(f"10{self.incoding(keyvalue)}")
        time.sleep(sd / 1000)

    def r(self, keyvalue, s=40, e=70):
        self.status = 3
        sd = random.randint(s, e)
        print(f'(KeyBoard.release : {keyvalue},{sd})')
        self.ser(f"11{self.incoding(keyvalue)}")
        time.sleep(sd / 1000)

    def ra(self, s=40, e=70):
        self.status = 4
        sd = random.randint(s, e)
        print(f'KeyBoard.ReleaseAll : {sd}')
        self.ser("12")
        time.sleep(sd / 1000)


class asyncKey(hardhid):
    def __init__(self, ser):
        super().__init__(ser)
        self.keyvalue, self.status, self.wait = 0, 0, False

    async def __call__(self, keyvalue, es=40, ee=70, ss=40, se=70):
        self.status = 1
        rd = random.randint(ss, se)
        ed = random.randint(es, ee)
        print(f'(KeyBoard.Write : {keyvalue},{rd},{ed})')
        self.ser(f"10{self.incoding(keyvalue)}")
        await asyncio.sleep(rd / 1000)
        self.ser(f"11{self.incoding(keyvalue)}")
        await asyncio.sleep(ed / 1000)

    def incoding(self, keyvalue):
        if type(keyvalue) is str:
            self.keyvalue = ord(keyvalue)
        else:
            self.keyvalue = keyvalue
        return self.keyvalue

    async def p(self, keyvalue, s=40, e=70, wait=False):
        sd = random.randint(s, e)

        if self.keyvalue != keyvalue or self.status != 2:
            print(sd)
            if self.wait:
                await self.ra()
                self.wait = False
            self.status = 2
            self.wait = wait
            print(f'(KeyBoard.Press : {keyvalue},{sd})')
            self.ser(f"10{self.incoding(keyvalue)}")
        await asyncio.sleep(sd / 1000)

    async def r(self, keyvalue, s=40, e=70):
        self.status = 3
        sd = random.randint(s, e)
        print(f'(KeyBoard.release : {keyvalue},{sd})')
        self.ser(f"11{self.incoding(keyvalue)}")
        await asyncio.sleep(sd / 1000)

    async def ra(self, s=40, e=70):
        self.status = 4
        sd = random.randint(s, e)
        print(f'KeyBoard.ReleaseAll : {sd}')
        self.ser("12")
        await asyncio.sleep(sd / 1000)


class BaseMouse(hardhid):
    @staticmethod
    def GetCursorPos():
        return win32api.GetCursorPos()


class Mouse(BaseMouse):
    def __init__(self, ser, x=0, y=0):
        super().__init__(ser)
        self.x = x
        self.y = y

    def __call__(self, x, y, s=40, e=70):
        def pm(a):
            if a > 0:
                return 1
            elif a == 0:
                return 0
            else:
                return -1

        nx, ny = win32api.GetCursorPos()
        x = (x + self.x) - nx
        y = (y + self.y) - ny
        x1, x2 = divmod(x, 127 if x > 0 else -127)
        y1, y2 = divmod(y, 127 if y > 0 else -127)
        x1 *= pm(x)
        y1 *= pm(y)
        print(f'Mouse.goto : {x},{y}')
        for i in range(max(abs(x1), abs(y1))):
            self.ser(f'20{127 * pm(x1)},{127 * pm(y1)}')
            x1 -= pm(x1)
            y1 -= pm(y1)
            time.sleep(6 / 1000)
        self.ser(f"20{x2},{y2}")
        sd = random.randint(s, e)
        time.sleep(sd / 1000)

    def c(self, es=40, ee=70, ss=40, se=70):
        sd = random.randint(ss, se)
        ed = random.randint(es, ee)
        print(f'Mouse.click : {sd} {ed}')
        self.ser('23')
        time.sleep(sd / 1000)
        self.ser('25')
        time.sleep(ed / 1000)

    def p(self, lr, s=40, e=70):
        if lr == 'l':
            packet = '23'
        elif lr == 'r':
            packet = '24'
        sd = random.randint(s, e)
        print(f'Mouse.prass : {sd}')
        self.ser(packet)
        time.sleep(sd / 1000)

    def r(self, lr, s=40, e=70):
        if lr == 'l':
            packet = '25'
        elif lr == 'r':
            packet = '26'
        sd = random.randint(s, e)
        print(f'Mouse.release : {sd}')
        self.ser(packet)
        time.sleep(sd / 1000)


class asyncMouse(BaseMouse):
    def __init__(self, ser, x=0, y=0):
        super().__init__(ser)
        self.x = x
        self.y = y

    async def __call__(self, x, y, s=40, e=70):
        def pm(a):
            if a > 0:
                return 1
            elif a == 0:
                return 0
            else:
                return -1

        nx, ny = win32api.GetCursorPos()

        x = (x + self.x) - nx
        y = (y + self.y) - ny
        print(x,self.x,nx)
        print(y,self.y,ny)
        x1, x2 = divmod(x, 127 if x > 0 else -127)
        y1, y2 = divmod(y, 127 if y > 0 else -127)
        x1 *= pm(x)
        y1 *= pm(y)
        print(f'Mouse.goto : {x},{y}')
        for i in range(max(abs(x1), abs(y1))):
            self.ser(f'20{127 * pm(x1)},{127 * pm(y1)}')
            x1 -= pm(x1)
            y1 -= pm(y1)
            await asyncio.sleep(6 / 1000)
        self.ser(f"20{x2},{y2}")
        sd = random.randint(s, e)
        await asyncio.sleep(sd / 1000)

    async def c(self, es=40, ee=70, ss=40, se=70):
        sd = random.randint(ss, se)
        ed = random.randint(es, ee)
        print(f'Mouse.click : {sd} {ed}')
        self.ser('23')
        await asyncio.sleep(sd / 1000)
        self.ser('25')
        await asyncio.sleep(ed / 1000)

    async def p(self, lr, s=40, e=70):
        if lr == 'l':
            packet = '23'
        elif lr == 'r':
            packet = '24'
        sd = random.randint(s, e)
        print(f'Mouse.prass : {sd}')
        self.ser(packet)
        await asyncio.sleep(sd / 1000)

    async def r(self, lr, s=40, e=70):
        if lr == 'l':
            packet = '25'
        elif lr == 'r':
            packet = '26'
        sd = random.randint(s, e)
        print(f'Mouse.release : {sd}')
        self.ser(packet)
        await asyncio.sleep(sd / 1000)


class fi:
    def __init__(self, findimgname, sx, ex, sy, ey, pixelsearch=False):
        self.sx, self.ex, self.sy, self.ey = sx, ex, sy, ey
        self.pixli = []
        self.mask = None

        if self.mask:
            self.method = cv.TM_CCORR_NORMED
        else:
            self.method = cv.TM_CCOEFF_NORMED

        if findimgname is not None:
            self.find = cv.imread(f'data\\dataimg\\{findimgname}.png')
            self.h, self.w = self.find.shape[:2]
            if pixelsearch:
                self.pixli = fi.pixex(self.find)
            self.find = cv.cvtColor(self.find, cv.COLOR_BGR2GRAY)

    def setmask(self, maskimg):
        self.mask = maskimg

    def match(self, creenimg):
        cutimgy = cv.cvtColor(creenimg[self.sy:self.ey, self.sx:self.ex], cv.COLOR_BGR2GRAY)
        # mask match only can TM_SQDIFF and TM_CCORR_NORMED
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCOEFF_NORMED, mask=self.mask)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)
        # cv.rectangle(cutimgy, maxloc, (maxloc[0] + self.w, maxloc[1] + self.h), (255, 255, 255), 1)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def pixelmatch(self, creenimg):
        cutimgy = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        res = cv.matchTemplate(cutimgy, self.find, cv.TM_CCORR_NORMED)

        minval, maxval, minloc, maxloc = cv.minMaxLoc(res)

        return [maxval, [maxloc[0] + self.w / 2, maxloc[1] + self.h / 2], list(maxloc)]

    def pixpix(self, creenimg):
        w, h = self.ex - self.sx, self.ey - self.sy

        creenimg = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        for e in range(h):
            for i in range(w):
                if creenimg[e, i] == 255:
                    return i, e
        return False

    def pixpix2(self, creenimg):
        creenimg = self.inRange(creenimg[self.sy:self.ey, self.sx:self.ex], self.pixli)
        b = np.where(creenimg == 254)
        return np.c_[b[0], b[1]]

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


def getimgfromhwnd(hwnd=None):
    if hwnd is None:
        hwnd = win32gui.GetDesktopWindow()

    sx, sy, ex, ey = win32gui.GetWindowRect(hwnd)
    w = ex - sx
    h = ey - sy
    w -= 4
    h -= 2
    hdc = win32gui.GetWindowDC(hwnd)
    #win32api hwnd to pywin32 hwnd
    uihdc = win32ui.CreateDCFromHandle(hdc)

    cdc = uihdc.CreateCompatibleDC()
    cbmp = win32ui.CreateBitmap()
    cbmp.CreateCompatibleBitmap(uihdc, w, h)

    cdc.SelectObject(cbmp)
    cdc.BitBlt((0, 0), (w, h), uihdc, (2, 0), win32con.SRCCOPY)
    signedintsarray = cbmp.GetBitmapBits(True)
    img = np.frombuffer(signedintsarray, dtype='uint8')
    img.shape = (h, w, 4)
    img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    win32gui.DeleteObject(cbmp.GetHandle())
    cdc.DeleteDC()
    uihdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    return img


def getmaplhwnd():
    hwnd = win32gui.FindWindow(None, 'MapleStory')
    sx, sy, ex, ey = win32gui.GetWindowRect(hwnd)
    if ex - sx < 900:
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return hwnd


class arduino:
    def __init__(self, baud=9600, port=None, timeout=2):
        if not port:
            sr = arduino.find_port(baud, timeout)
            if not sr:
                raise ValueError("Could not find port.")
        else:
            sr = serial.Serial(port, baud, timeout=timeout)

        self.sr = sr

    def __call__(self, cmd):
        cmd += "$!"

        self.sr.write(cmd.encode())

    @staticmethod
    def find_port(baud, timeout):
        # This function must have an Arduino code that receives '00$!' and sends 'version'.

        def enumerate_serial_ports():
            path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            except WindowsError:
                raise Exception

            for i in itertools.count():
                try:
                    val = winreg.EnumValue(key, i)
                    yield (str(val[1]))  # , str(val[0]))
                except EnvironmentError:
                    break

        ports = enumerate_serial_ports()

        for p in ports:
            try:
                sr = serial.Serial(p, baud, timeout=timeout)
            except (serial.serialutil.SerialException, OSError) as e:
                continue

            try:
                packet = '00$!'
                sr.flush()
                sr.write(packet.encode())
            except Exception:
                return None

            version = sr.readline()
            version = version.decode()[:len(version) - 2]
            if version != 'version':
                sr.close()
                continue
            if sr:
                return sr
        return None

    @staticmethod
    def findarduino_devcon():
        # This function need devcon.exe
        import subprocess
        asd = os.getcwd().replace("\\", "/")
        a = subprocess.check_output(f"{asd}/devcon find @*USB*", shell=True, stderr=subprocess.STDOUT)
        try:
            ser = serial.Serial(
                port=f"{a[a.find('Arduino'):].split()[1][4:-1]}",
                baudrate=9600, timeout=0
            )
        except:
            ser = serial.Serial(
                port=f"{a[a.find('Bossa'):].split()[2][5:-1]}",
                baudrate=9600, timeout=0
            )

        return ser
