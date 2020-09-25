from threading import Thread, Lock
import winsound
from cls import *
import time
import asyncio

class findRhun(Exception):
    pass


class findBoss(Exception):
    pass


class stopmove(Exception):
    pass


class stoprunning(Exception):
    pass


class asyncKey:

    def __init__(self, ser):
        self.keyvalue, self.status, self.wait, self.raseof = 0, 0, False, True
        self.ser = ser

    async def __call__(self, keyvalue, es=40, ee=70, ss=40, se=70):
        s, e = self.sendpacket(1, keyvalue, ss, se, es, ee)
        print(f'(KeyBoard.Write : {keyvalue}, {s}, {e})')
        await asyncio.sleep(s / 1000)
        await asyncio.sleep(e / 1000)

    def sendpacket(self, status, keyvalue, ss, se, es=40, ee=70):
        if self.status == 2 and self.wait:
            self.ra()
            self.wait = False
        if type(keyvalue) is str:
            self.keyvalue = ord(keyvalue)
        else:
            self.keyvalue = keyvalue
        self.status = status
        s = random.randint(ss, se)
        e = random.randint(es, ee)
        packet = f'(0,{status},{self.keyvalue},{s - 5},{e})'
        self.ser.write(packet.encode())
        return s, e

    async def p(self, keyvalue, ss=40, se=70, wait=False):
        if self.keyvalue != keyvalue or self.status != 2:
            s, e = self.sendpacket(2, keyvalue, ss=ss, se=se)
            self.wait = wait
            print(f'(KeyBoard.Press : {keyvalue},{s})')
            await asyncio.sleep(s / 1000)
        else:
            s = random.randint(ss, se)
            await asyncio.sleep(s / 1000)

    async def r(self, keyvalue, es=40, ee=70):
        s, e = self.sendpacket(3, keyvalue, ss=es, se=ee)
        print(f'(KeyBoard.release : {keyvalue},{s})')
        await asyncio.sleep(s / 1000)

    async def ra(self, es=40, ee=70):
        e = random.randint(es, ee)
        self.status = 4
        packet = f'(0,{4},{self.keyvalue},{e - 5},{e})'
        self.ser.write(packet.encode())
        print(f'KeyBoard.ReleaseAll')
        await asyncio.sleep(e / 1000)

ser = findarduino()
hwnd, left, top, right, bot = findmapl()
key = asyncKey(ser)
mou = Mouse(left, top, ser)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esck, spacek, bsk, tabk, returnk = 130, 129, 128, 216, 215, 218, 217, 177, 32, 8, 179, 176
ma = [10, 248, 86, 158, 92, 54]  # [10, 212, 86, 171, 33, 69] 신전4, [10, 248, 86, 158, 92, 54] 폐쇄구역3
xy = [[], []]  # 0캐릭터위치, 1룬 위치
onfli = {'ai': True, 'sim': False}
cren, lock, beep = [], Lock(), Thread(target=winsound.Beep, args=(300, 3000,))

fili = [fi("i", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi("y", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi("r", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi(None, 1345, 1346, 744, 745),
        fi("lie", 1000, 1366, 298, 578, True),
        fi("b", 580, 650, 63, 83)]

fili[2].pixli += fi.pixex(cv.imread('dataimg\\g.png'))
fili[3].pixli.append([[185, 169, 152], [185, 169, 152]])
fili[4].setmaskimg(cv.imread('dataimg\\liem.png'))


def goto(x, y, z=3):
    await key.ra()
    while True:
        if xy[0][0] - x >= 40:
            await key.p(leftk)
            await key(altk)
            await key(altk)
            await key.ra()
        elif x - xy[0][0] >= 40:
            await key.p(rightk)
            await key(altk)
            await key(altk)
            await key.ra()
        elif xy[0][0] - x >= z:
            await key.p(leftk, wait=True)
        elif x - xy[0][0] >= z:
            await key.p(rightk, wait=True)
        elif xy[0][1] > y + 7:
            await key(altk, 100, 130)
            await key(96, 3000, 3100)
        elif xy[0][1] < y - 7:
            await key.p(upk, 20, 40)
            await key.p(downk)
            await key(altk)
            await key.r(upk, 20, 40)
            await key.r(downk, 1000, 1100)
        else:
            await key.ra()
            break


def scmc():
    global xy, beep, cren, onfli, stkeyt
    stimety, stime = [True, True], [0, 0]
    resul = list(range(len(fili)))
    onf = True
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_F1):
            if onf:
                rli['stoprunning'] = True
                onfli['ai'] = False
                onf = False
                print(onf)
                sleep(1)
            else:
                onf = True
                stkeyt = Thread(target=stkey)
                stkeyt.start()
                print(onf)
                sleep(1)
        if onf:
            cren = creen(hwnd)
            resul[0] = fili[0].piximg(cren)
            resul[1] = fili[1].piximg(cren)
            resul[2] = fili[2].piximg(cren)
            resul[3] = fili[3].pixpix(cren)

            for e, i in enumerate(fili[4:]):
                resul[e + 4] = i.re(cren)

            if xy[0] == resul[0][1]:
                if stimety[1]:
                    stime[1] = time.time()
                    stimety[1] = False
                elif time.time() - stime[1] > 10:
                    if not beep.is_alive():
                        beep = Thread(target=winsound.Beep, args=(300, 3000,))
                        beep.start()
                    rli['stopmove'] = True
            else:
                stimety[1] = True

            if resul[0][0] > 0.99:
                xy[0] = resul[0][1]
            lock.acquire()

            if resul[3]:
                onfli['sim'] = True


            if resul[2][0] > 0.99:
                xy[1] = resul[2][1]
                rli['findRhun'] = True

            if resul[1][0] > 0.99:
                if stimety[0]:
                    stime[0] = time.time()
                    stimety[0] = False
                elif time.time() - stime[0] > 5 and not beep.is_alive():
                    print('사람')
                    beep = Thread(target=winsound.Beep, args=(300, 3000,))
                    beep.start()
            else:
                stimety[0] = True

            if resul[4][0] > 0.99 and not beep.is_alive():
                beep = Thread(target=winsound.Beep, args=(300, 3000,))
                beep.start()

            if resul[5][0] > 0.6 and not beep.is_alive():
                beep = Thread(target=winsound.Beep, args=(300, 3000,))
                beep.start()
                rli['findBoss'] = True
            lock.release()

def useai():
    global beep
    stime = time.time()
    a = 1
    while True:
        time.sleep(1)
        if onfli['ai']:
            if time.time() - stime > 5:
                lieimg = cren.copy()
                print('start gpu')
                lieli = performDetect(lieimg, thresh=.5, configPath="./cfg/yolov46.cfg",
                                      weightPath="backup\\yolov4-6cls_last.weights", metaPath="./data/sum.data")

                cv.imwrite(f'lastimg\\{a}.png', lieimg)
                a += 1
                if a == 30:
                    a = 1
                print(lieli)
                for i in lieli:
                    if i[0] == 'star' or i[0] == 'lie':
                        if not beep.is_alive():
                            beep = Thread(target=winsound.Beep, args=(300, 3000,))
                            beep.start()
                stime = time.time()
                print('end gpu')
        else:
            stime = time.time()


def cadenmo():
    while True:
        if xy[0][0] < 90:
            if xy[0][1] >= 25:
                goto(ma[4], ma[5])
                continue
            if xy[0][0] >= 19:
                await key.p(leftk, wait=True)
            elif xy[0][0] <= 17:
                await key.p(rightk, wait=True)

            s = random.randint(40, 70)
            e = random.randint(60, 90)
            packet = f'(0,1,218,{s - 5},{e})'
            ser.write(packet.encode())
            print(f'(await KeyBoard.Write : 218, {s}, {e})')
            sleep(s / 1000)
            sleep(e / 1000)
        else:
            break

    await key.ra()
    await key(rightk, 250, 280)
    await key(altk, 200, 240)
    await key('c', 90, 140)
    await key.p(rightk, 20, 40)
    await key.p(upk, 20, 40)
    await key.p('x', 400, 501)
    await key.r(rightk)
    await key.r(upk)
    await key.r('x')
    await key('x')
    await key('x', 300, 350)
    await key(ctrlk, 400, 450)
    await key(shiftk)
    await key(shiftk, 300, 351)
    radm = random.randint(0, 1)
    if radm == 0:
        await key.p(upk, 30, 50)
        await key.p(downk, 100, 140)
        await key(altk, 80, 120)
        await key(altk, 80, 120)
        await key(altk, 500, 550)
        await key(altk)
        await key(altk)
        await key(altk)
        await key.r(upk, 30, 50)
        await key.r(downk)

    else:
        await key.p(upk, 30, 50)
        await key.p(downk, 100, 140)
        await key(altk, 80, 120, 1000, 1050)
        await key.r(upk, 30, 50)
        await key.r(downk)

    if random.randint(0, 1):
        await key('a', 110, 150)
    else:
        await key('a')
        await key('a', 70, 110)

    if random.randint(0, 1):
        await key('s', 400, 451)
    else:
        await key('s')
        await key('s', 400, 451)

    radm = random.randint(0, 3)
    if not radm == 0:
        await key(altk)
    await key.p(upk)
    if radm:
        await key('e')
        await key('e')
    else:
        await key('e')
        await key('e')
        await key('e')

    await key.r(upk, 500, 551)
    await key.p(upk, 30, 50)
    await key.p(downk, 100, 140)
    await key(altk)
    await key(altk)
    await key(altk)
    await key.r(upk, 30, 50)
    await key.r(downk, 300, 400)
    bat = 0
    while True:
        if onfli['sim']:
            await key('4', 1000, 1100)
            await key('3', 750, 800)
            onfli['sim'] = False
        elif xy[0][0] >= 74:
            if (random.randint(0, 2) == False or bat) and bat < 3:
                bat += 1
                await key.p(leftk, 20, 40)
                await key(altk, 70, 100)
                await key(altk, 40, 70)
                await key(altk, 40, 70)
                await key.r(leftk, 20, 40)
                await key('w', 550, 590)
            else:
                await key.p(leftk, 20, 40)
                await key(altk, 70, 100)
                await key(altk, 30, 50)
                await key.r(leftk, 20, 40)
                await key(altk, 40, 70)

                await key(ctrlk, 550, 590)
        elif xy[0][0] >= 58:
            await key.p(leftk)
        else:
            await key.ra()
            break

    await key(altk)
    await key.p(leftk, 20, 40)
    await key.p(upk, 20, 40)
    await key.p('x')
    await key.r(leftk)
    await key.r(upk, 400, 501)
    await key.r('x')
    await key('x')
    await key('x', 300, 351)
    if random.randint(0, 1):
        await key('a')
        await key('a', 300, 351)
    else:
        await key('a')
        await key('a')
        await key('a', 300, 351)
    await key.p(rightk)
    await key('f', 40, 70, 80, 110)
    await key.r(rightk)

def stkey():
    global xy, beep, cren, onfli
    fstart = True

    while True:
        try:
            try:
                onfli['ai'] = True
                cadenmo()

            except findRhun:
                onfli['ai'] = False
                rli['findRhun'] = False
                print("Raise findRhun")

                time.sleep(1)
                goto(xy[1][0], xy[1][1])
                await key(32, 500, 550)
                labelli = performDetect(cren[150:314, 450:900], thresh=.5, configPath="./cfg/yolov46.cfg",
                                        weightPath="backup\\yolov4-6cls_last.weights", metaPath="./data/sum.data")
                print(labelli)
                if len(labelli) == 4:
                    for i in labelli:
                        if i[0] == 'star' or i[0] == 'lie':
                            break
                        sleep(0.5)
                        await key(eval(i[0] + 'k'))

            except findBoss:
                onfli['ai'] = False
                rli['findBoss'] = False
                print("Raise findBoss")
                await key.ra()

                if fstart:
                    await key(esck)
                    await key(176)
                    await key(rightk, 200, 300)
                    await key(176, 100, 150)
                    await key(176, 5000, 5100)
                findplayer = True
                cheak = fi(None, 806, 807, 756, 757)
                cheak.pixli.append([[255, 255, 255], [255, 255, 255]])
                while True:
                    if cheak.pixpix(cren):
                        stime = time.time()
                        while time.time() - stime < 4:
                            player = fili[1].piximg(cren)
                            if player[0] > 0.99:
                                await key(esck)
                                await key(176)
                                await key(rightk, 200, 300)
                                await key(176, 100, 150)
                                await key(176, 2000, 2100)
                                findplayer = True
                                break
                            else:
                                findplayer = False

                        if not findplayer:
                            break

                goto(ma[4], ma[5])

                fstart = True

            except stopmove:
                rli['stopmove'] = False
                print("Raise stopmove")
                await key.ra()

                mou(481, 490)
                mou.c()
                await key.p(leftk)
                await key(altk)
                await key(altk)
                await key.ra()
                await key.p(rightk)
                await key(altk)
                await key(altk)
                await key.ra()
                goto(ma[4], ma[5])

        except stoprunning:
            rli['stoprunning'] = False
            await key.ra()
            print("Raise stoprunning")
            break


async def main():

