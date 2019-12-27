import serial
import random
from time import sleep

ser = serial.Serial(
    port='COM4',
    baudrate=9600, timeout=0
)

altk = 130
ctrlk = 128
leftk = 216
rightk = 215
upk = 218
downk = 217
swcont, wcont = 0, 0

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


def atkctrl():
    global swcont,wcont
    radm = random.randint(0, 20)
    if swcont >= 2:
        wcont += 1
        if radm >= 19:
            send(leftk, 20, 30, a=2)
            send(altk, e=41, f=70)
            send(altk, e=20, f=30)
            send(leftk, 41, 70, a=3)
            send('w', e=560, f=630)

        else:
            send(leftk, 20, 30, a=2)
            send(altk, e=41, f=70)
            send(altk, e=20, f=30)
            send(leftk, 41, 70, a=3)
            send(altk, e=41, f=70)
            send('w', e=560, f=630)

        if wcont >= 3:
            wcont = 0
            swcont = 0
    else:
        if radm >= 19:
            send(leftk, 20, 30, a=2)
            send(altk, e=41, f=70)
            send(altk, e=20, f=30)
            send(leftk, 41, 70, a=3)
            send(ctrlk, e=560, f=630)

        else:
            send(leftk, 20, 30, a=2)
            send(altk, e=41, f=70)
            send(altk, e=20, f=30)
            send(leftk, 41, 70, a=3)
            send(altk, e=41, f=70)
            send(ctrlk, e=560, f=630)


def atkdsa():
    global swcont
    swcont += 1
    send(96, e=900, f=930)
    send('d', e=40, f=60)
    send('d', e=600, f=620)
    send(rightk, 41, 70, a=2)
    send('s', e=40, f=60)
    send('s', e=250, f=280)
    send(rightk, 30, 50, a=3)
    send('a', e=40, f=60)
    send('a', e=400, f=500)

    send(altk, e=41, f=70)
    send(altk, e=41, f=70)
    send(ctrlk, e=560, f=630)

    send(altk, e=41, f=70)
    send(altk, e=41, f=70)
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
    send(downk, e=530, f=580)

    send(leftk, 41, 60, a=2)
    send('a', e=41, f=60)
    send(leftk, 170, 220, a=3)

    send('s', e=550, f=650)


while True:
    sleep(0.5)
    print(caller(get_square, 5))
