import cv2.cv2 as cv
import glob
from time import sleep
class rect:
    def __init__(self, sx, sy, ex, ey):
        self.color = (0, 0, 0)
        self.label = 'lie'
        self.sx, self.sy = sx, sy
        self.ex, self.ey = ex, ey
        if self.sx > self.ex and self.sy > self.ey:
            self.lux, self.luy, self.rdx, self.rdy = self.ex, self.ey, self.sx, self.sy

        elif self.sx > self.ex and self.sy < self.ey:
            self.lux, self.luy, self.rdx, self.rdy = self.ex, self.sy, self.sx, self.ey

        elif self.sx < self.ex and self.sy > self.ey:
            self.lux, self.luy, self.rdx, self.rdy = self.sx, self.ey, self.ex, self.sy

        else:
            self.lux, self.luy, self.rdx, self.rdy = self.sx, self.sy, self.ex, self.ey
        self.make()
        self.mr(img1)

        self.lurddot = [False, False, False, False]  # left up right down true/false

    def make(self):
        self.w, self.h = self.rdx - self.lux, self.rdy - self.luy

        self.wcenter = self.w / 2
        self.hcenter = self.h / 2

        self.middotx, self.middoty = (self.lux + self.rdx) / 2, (self.luy + self.rdy) / 2

        self.leftx, self.lefty = self.middotx - self.wcenter, self.middoty
        self.upx, self.upy = self.middotx, self.middoty - self.hcenter
        self.rightx, self.righty = self.middotx + self.wcenter, self.middoty
        self.downx, self.downy = self.middotx, self.middoty + self.hcenter
        self.leftx, self.lefty, self.upx, self.upy, self.rightx, self.righty, self.downx, self.downy = \
            round(self.leftx), round(self.lefty), round(self.upx), round(self.upy), round(self.rightx), round(
                self.righty), round(self.downx), round(self.downy)

        self.lurdx = [self.leftx, self.upx, self.rightx, self.downx]
        self.lurdy = [self.lefty, self.upy, self.righty, self.downy]

    def mr(self, im, a=False):
        if a:
            cv.putText(im, self.label, (self.lux, self.rdy), cv.FONT_HERSHEY_SIMPLEX, 2, color=[225, 225, 225])
        cv.rectangle(im, (self.lux, self.luy), (self.rdx, self.rdy), self.color, 0)

        for i in range(4):
            cv.rectangle(im, (self.lurdx[i] - sm, self.lurdy[i] - sm),
                         (self.lurdx[i] + sm, self.lurdy[i] + sm), self.color, 0)



def rfi():
    dr = glob.glob(f"labels\\{labelimg}\\*.txt")
    if dr.count(f"labels\\{labelimg}\\{str(di[dcount])}.txt"):
        f = open(f"labels\\{labelimg}\\{str(di[dcount])}.txt", 'r')
        print(str(di[dcount]), end=" ")
        lines = f.readlines()
        for g, line in enumerate(lines):
            linel = line.split()
            linel[1:] = list(map(int, linel[1:]))
            print(f"{linel[0]}", end=" ")
            rectli.append(rect(linel[1], linel[2], linel[3], linel[4]))
            rectli[g].label = linel[0]
        if len(lines):
            print()
        f.close()


def wfi():
    f = open(f"labels\\{labelimg}\\{str(di[dcount])}.txt", 'w')
    for i in rectli:
        lix, liy = [i.lux, i.rdx], [i.luy, i.rdy]
        lix.sort()
        liy.sort()
        data = f"{i.label} {lix[0]} {liy[0]} {lix[1]} {liy[1]}\n"
        f.write(data)
    f.close()


def drawrect(event, x, y, flags, param):
    global sx, sy, draw, img1, rectli, start

    img1 = img.copy()

    if start:
        img1 = img.copy()
        for i1 in rectli:
            i1.mr(img1)
        if event == cv.EVENT_LBUTTONDOWN:
            draw = True
            sx, sy = x, y
        elif event == cv.EVENT_MOUSEMOVE and draw:
            cv.rectangle(img1, (sx, sy), (x, y), (0, 0, 0), 0)
        elif event == cv.EVENT_LBUTTONUP and draw:
            draw = False
            rectli.append(rect(sx, sy, x, y))
            start = False

    else:
        if event == cv.EVENT_LBUTTONDOWN:
            for i in rectli:
                for a in range(4):
                    if i.lurdx[a] - sm < x < i.lurdx[a] + sm and i.lurdy[a] - sm < y < i.lurdy[a] + sm:
                        i.lurddot[a] = True
                    else:
                        i.lurddot[a] = False

        elif event == cv.EVENT_MOUSEMOVE:
            for i in rectli:
                if i.lurddot[0]:
                    i.lux = x
                    i.make()
                elif i.lurddot[1]:
                    i.luy = y
                    i.make()
                elif i.lurddot[2]:
                    i.rdx = x
                    i.make()
                elif i.lurddot[3]:
                    i.rdy = y
                    i.make()

        elif event == cv.EVENT_LBUTTONUP:
            for i in rectli:
                for a in range(4):
                    i.lurddot[a] = False


draw, start, rectli, di, dcount = False, False, [], [], 0
labelimg, sm, zoom = "lie", 3, 0

d = glob.glob(f"images\\{labelimg}\\*.jpg")

for i in d:
    i = i.split('\\')[2]
    i = i[:-4]
    di.append(int(i))
di.sort()

img = cv.imread(f"images\\{labelimg}\\{str(di[dcount])}.jpg")
for i in range(zoom):
    img = cv.pyrUp(img)

img1 = img.copy()
cv.namedWindow('image1')
cv.setMouseCallback('image1', drawrect)


rfi()

while (1):
    for i in rectli:
        i.mr(img1, a=True)
    cv.imshow('image1', img1)
    k = cv.waitKey(10) & 0xFF
    if k == 27:  # esc
        wfi()
        break
    elif k == 119:  # w
        start = True

    elif k == 100:  # d
        wfi()
        rectli = []
        dcount += 1

        if len(di) <= dcount:
            dcount = 0
        rfi()
        img = cv.imread(f"images\\{labelimg}\\{str(di[dcount])}.jpg")
        for i in range(zoom):
            img = cv.pyrUp(img)
        img1 = img.copy()

    elif k == 97:  # a
        wfi()
        rectli = []
        dcount -= 1
        if dcount < 0:
            dcount = len(di) - 1
        rfi()
        img = cv.imread(f"images\\{labelimg}\\{str(di[dcount])}.jpg")
        for i in range(zoom):
            img = cv.pyrUp(img)
        img1 = img.copy()

    elif k == 115:  # s
        for i in rectli:
            i.color = (255, 0, 0)
            img1 = img.copy()
            for i1 in rectli:
                i1.mr(img1)
            i.color = (0, 0, 0)
            cv.imshow('image1', img1)
            k = cv.waitKeyEx(0)
            if k == 2621440:  # down arrow
                i.label = "down"
            elif k == 2424832:  # left arrow
                i.label = "left"
            elif k == 2555904:  # right arrow
                i.label = "right"
            elif k == 2490368:  # up arrow
                i.label = "up"
            else:
                i.label = 'lie'

cv.destroyAllWindows()
