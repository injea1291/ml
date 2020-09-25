import winsound
from cls import *
import time
import functools

ser = findarduino()
hwnd, left, top, right, bot = findmapl()
key = asyncKey(ser)
mou = asyncMouse(left, top, ser)

altk, shiftk, ctrlk, leftk, rightk, upk, downk, esck, spacek, bsk, tabk, returnk = 130, 129, 128, 216, 215, 218, 217, 177, 32, 8, 179, 176
ma = [10, 248, 86, 158, 92, 54]  # [10, 212, 86, 171, 33, 69] 신전4, [10, 248, 86, 158, 92, 54] 폐쇄구역3
xy = [[], []]  # 0캐릭터위치, 1룬 위치
onfli = {'ai': True, 'sim': False, 'sub': 0}
loop = asyncio.get_event_loop()
fili = [fi("i", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi("y", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi("r", ma[0], ma[1], ma[2], ma[3], pixtf=True),
        fi(None, 1345, 1346, 744, 745),
        fi("lie", 1000, 1366, 298, 578, True),
        fi("b", 580, 650, 63, 83)]

fili[2].pixli += fi.pixex(cv.imread('data\\dataimg\\g.png'))
fili[3].pixli.append([[185, 169, 152], [185, 169, 152]])
fili[4].setmaskimg(cv.imread('data\\dataimg\\liem.png'))


async def goto(x, y, z=3):
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


async def scmc():
    global xy, cren, mainkey
    stimety, stime = [True, True], [0, 0]

    resul = list(range(len(fili)))

    mainkey = asyncio.create_task(cadenmo())
    asyncio.create_task(stkey())
    onf = True
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_F1):
            if onf:
                onf = False
                print(onf)
                mainkey.cancel()
                try:
                    await mainkey
                except asyncio.CancelledError:
                    print("cancel mainkey")
                onfli['ai'] = False
            else:
                onf = True
                print(onf)
                mainkey = asyncio.create_task(cadenmo())
                onfli['ai'] = True

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
                    loop.run_in_executor(None, winsound.Beep, 300, 3000)
                    onfli['sub'] = 3
            else:
                stimety[1] = True

            if resul[0][0] > 0.99:
                xy[0] = resul[0][1]

            if resul[3]:
                onfli['sim'] = True

            if resul[2][0] > 0.99:
                xy[1] = resul[2][1]
                onfli['sub'] = 1

            if resul[1][0] > 0.99:
                if stimety[0]:
                    stime[0] = time.time()
                    stimety[0] = False
                elif time.time() - stime[0] > 5:
                    print('사람')
                    loop.run_in_executor(None, winsound.Beep, 300, 3000)
            else:
                stimety[0] = True

            if resul[4][0] > 0.99:
                loop.run_in_executor(None, winsound.Beep, 300, 3000)

            if resul[5][0] > 0.6:
                loop.run_in_executor(None, winsound.Beep, 300, 3000)
                onfli['sub'] = 2

            await asyncio.sleep(0.001)


async def useai():
    stime = time.time()
    a = 1
    loop = asyncio.get_event_loop()
    while True:
        if onfli['ai']:
            if time.time() - stime > 5:
                lieimg = cren.copy()
                print('start gpu')

                lieli = await loop.run_in_executor(None, functools.partial(performDetect,
                            cv.imread("data\\set\\images\\arrow\\60010.png"), thresh=.5, configPath="./cfg/yolov46.cfg",
                            weightPath="backup\\yolov4-6cls_last.weights", metaPath="./data/sum.data"))

                cv.imwrite(f'lastimg\\{a}.png', lieimg)
                a += 1
                if a == 30:
                    a = 1
                print(lieli)
                for i in lieli:
                    if i[0] == 'star' or i[0] == 'lie':
                        loop.run_in_executor(None, winsound.Beep, 300, 3000)
                stime = time.time()
                print('end gpu')
        else:
            stime = time.time()


async def cadenmo():
    while True:
        while True:
            if xy[0][0] < 90:

                if xy[0][1] >= 25:
                    await goto(ma[4], ma[5])
                    continue
                if xy[0][0] >= 19:
                    await key.p(leftk, wait=True)
                elif xy[0][0] <= 17:
                    await key.p(rightk, wait=True)

                s = random.randint(40, 70)
                e = random.randint(60, 90)
                packet = f'(0,1,218,{s - 5},{e})'
                ser.write(packet.encode())
                print(f'(KeyBoard.Write : 218, {s}, {e})')
                await asyncio.sleep(s / 1000)
                await asyncio.sleep(e / 1000)
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


async def stkey():
    global onfli,mainkey
    while True:
        if onfli['sub']:
            mainkey.cancel()
            try:
                await mainkey
            except asyncio.CancelledError:
                print("cancel mainkey")
            if onfli['sub'] == 1:
                onfli['ai'] = False
                print("findRhun")
                await goto(xy[1][0], xy[1][1])
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
            elif onfli['sub'] == 2:
                onfli['ai'] = False
                print("chagech")
                await key.ra()
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

                await goto(ma[4], ma[5])
            elif onfli['sub'] == 3:
                print("stopmove")
                await key.ra()

                await mou(481, 490)
                await mou.c()
                await key.p(leftk)
                await key(altk)
                await key(altk)
                await key.ra()
                await key.p(rightk)
                await key(altk)
                await key(altk)
                await key.ra()
                await goto(ma[4], ma[5])
            onfli['sub'] = 0
            mainkey = asyncio.create_task(cadenmo())
        await asyncio.sleep(0.001)


asyncio.run(scmc())
