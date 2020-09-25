from threading import Thread, Lock
import winsound
from cls import *
import time


class findRhun(Exception):
    pass


class findBoss(Exception):
    pass


class stopmove(Exception):
    pass


class stoprunning(Exception):
    pass


class Keyboard1(Keyboard):
    def __getattribute__(self, item):
        if item == "raseof" or item == "change":
            return super().__getattribute__(item)
        if self.raseof:
            if rli['findBoss']:
                raise findBoss
            elif rli['findRhun']:
                raise findRhun
            elif rli['stopmove']:
                raise stopmove
        if rli['stoprunning']:
            raise stoprunning

        return super().__getattribute__(item)

    def change(self, raseof):
        self.raseof = raseof


ser = findarduino()
hwnd, left, top, right, bot = findmapl()
key = Keyboard1(ser)
mou = Mouse(left, top, ser)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esck, spacek, bsk, tabk, returnk = 130, 129, 128, 216, 215, 218, 217, 177, 32, 8, 179, 176
ma = [10, 248, 86, 158, 92, 54]  # [10, 212, 86, 171, 33, 69] 신전4, [10, 248, 86, 158, 92, 54] 폐쇄구역3
xy = [[], []]  # 0캐릭터위치, 1룬 위치
onfli = {'ai': True, 'sim': False}
rli = {'stoprunning': False, 'findBoss': False, 'stopmove': False, 'findRhun': False}
cren, lock, beep = [], Lock(), Thread(target=winsound.Beep, args=(300, 3000,))

fili = [fi("i", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi("y", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi("r", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi(None, 1345, 1346, 744, 745),
        fi("lie", 1000, 1366, 298, 578, True),
        fi("b", 580, 650, 63, 83)]

fili[2].pixli += fi.pixex(cv.imread('data\\dataimg\\g.png'))
fili[3].pixli.append([[185, 169, 152], [185, 169, 152]])
fili[4].setmaskimg(cv.imread('data\\dataimg\\liem.png'))


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
            key.ra()
            break


def scmc():
    global xy, beep, cren, onfli, rli, stkeyt
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

                cv.imwrite(f'data\\lastimg\\{a}.png', lieimg)
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


def stkey():
    global xy, beep, cren, onfli, rli
    fstart = True
    swcont = 0

    def cadensin():
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
            if onfli['sim']:
                key(194, 1000, 1100)
                key(213, 750, 800)
                onfli['sim'] = False
            elif xy[0][0] >= 31 + 33:
                atkctrl()
            elif xy[0][0] >= 10 + 33:
                key.p(leftk, 5, 5)
            else:
                if wcont >= 1:
                    swcont = 0
                key.r(leftk, 5, 5)
                break

    def zero():
        def dob(keyV, d1, d2):
            key(keyV, 41, 70)
            key(keyV, 41, 70)
            key(keyV, d1, d2)

        for i in [leftk, rightk]:
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
            dob(i, 200, 250)
            key('s', 40, 70)
            radm = random.randint(0, 4)
            if radm == 0:
                key(ctrlk, 40, 70)
                key(ctrlk, 41, 70)
            else:
                key(ctrlk, 41, 70)
            key.p(upk, 20, 40)
            key.p(downk)
            key(altk)
            if random.randint(0, 2) == 1:
                key(altk, 41, 70)
            key.r(upk, 20, 40)
            key.r(downk, 1000, 1100)

            key.p(i, 1200, 1300)
            key.r(i)

    def cadenmo():

        while True:
            if xy[0][0] < 90:
                if xy[0][1] >= 25:
                    goto(ma[4], ma[5])
                    continue
                if xy[0][0] >= 19:
                    key.p(leftk, wait=True)
                elif xy[0][0] <= 17:
                    key.p(rightk, wait=True)

                if rli['stoprunning']:
                    raise stoprunning
                elif rli['findBoss']:
                    raise findBoss
                elif rli['findRhun']:
                    raise findRhun
                elif rli['stopmove']:
                    raise stopmove

                s = random.randint(40, 70)
                e = random.randint(60, 90)
                packet = f'(0,1,218,{s - 5},{e})'
                ser.write(packet.encode())
                print(f'(KeyBoard.Write : 218, {s}, {e})')
                sleep(s / 1000)
                sleep(e / 1000)
            else:
                break
        key.ra()
        key(rightk, 250, 280)
        key(altk, 200, 240)
        key('c', 90, 140)
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

        if random.randint(0, 1):
            key('a', 110, 150)
        else:
            key('a')
            key('a', 70, 110)

        if random.randint(0, 1):
            key('s', 400, 451)
        else:
            key('s')
            key('s', 400, 451)

        radm = random.randint(0, 3)
        if not radm == 0:
            key(altk)
        key.p(upk)
        if radm:
            key('e')
            key('e')
        else:
            key('e')
            key('e')
            key('e')

        key.r(upk, 500, 551)
        key.p(upk, 30, 50)
        key.p(downk, 100, 140)
        key(altk)
        key(altk)
        key(altk)
        key.r(upk, 30, 50)
        key.r(downk, 300, 400)
        bat = 0
        while True:
            if onfli['sim']:
                key('4', 1000, 1100)
                key('3', 750, 800)
                onfli['sim'] = False
            elif xy[0][0] >= 74:
                if (random.randint(0, 2) == False or bat) and bat < 3:
                    bat += 1
                    key.p(leftk, 20, 40)
                    key(altk, 70, 100)
                    key(altk, 40, 70)
                    key(altk, 40, 70)
                    key.r(leftk, 20, 40)
                    key('w', 550, 590)
                else:
                    key.p(leftk, 20, 40)
                    key(altk, 70, 100)
                    key(altk, 30, 50)
                    key.r(leftk, 20, 40)
                    key(altk, 40, 70)

                    key(ctrlk, 550, 590)
            elif xy[0][0] >= 58:
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
        if random.randint(0, 1):
            key('a')
            key('a', 300, 351)
        else:
            key('a')
            key('a')
            key('a', 300, 351)
        key.p(rightk)
        key('f', 40, 70, 80, 110)
        key.r(rightk)

    while True:
        try:
            try:
                key.change(True)
                onfli['ai'] = True
                cadenmo()

            except findRhun:
                onfli['ai'] = False
                key.change(False)
                rli['findRhun'] = False
                print("Raise findRhun")

                time.sleep(1)
                goto(xy[1][0], xy[1][1])
                key(32, 500, 550)
                labelli = performDetect(cren[150:314, 450:900], thresh=.5, configPath="./cfg/yolov46.cfg",
                                        weightPath="backup\\yolov4-6cls_last.weights", metaPath="./data/sum.data")
                print(labelli)
                if len(labelli) == 4:
                    for i in labelli:
                        if i[0] == 'star' or i[0] == 'lie':
                            break
                        sleep(0.5)
                        key(eval(i[0] + 'k'))

            except findBoss:
                onfli['ai'] = False
                key.change(False)
                rli['findBoss'] = False
                print("Raise findBoss")
                key.ra()

                if fstart:
                    key(esck)
                    key(176)
                    key(rightk, 200, 300)
                    key(176, 100, 150)
                    key(176, 5000, 5100)
                findplayer = True
                cheak = fi(None, 806, 807, 756, 757)
                cheak.pixli.append([[255, 255, 255], [255, 255, 255]])
                while True:
                    if cheak.pixpix(cren):
                        stime = time.time()
                        while time.time() - stime < 4:
                            player = fili[1].piximg(cren)
                            if player[0] > 0.99:
                                key(esck)
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

                fstart = True

            except stopmove:
                key.change(False)
                rli['stopmove'] = False
                print("Raise stopmove")
                key.ra()

                mou(481, 490)
                mou.c()
                key.p(leftk)
                key(altk)
                key(altk)
                key.ra()
                key.p(rightk)
                key(altk)
                key(altk)
                key.ra()
                goto(ma[4], ma[5])

        except stoprunning:
            key.change(False)
            rli['stoprunning'] = False
            key.ra()
            print("Raise stoprunning")
            break


def main():
    beep.start()