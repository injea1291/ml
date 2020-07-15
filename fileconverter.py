import glob
import cv2.cv2 as cv
import os

arrows = ["right", "left", "up", "down"]
lies = ["star", "lie"]
sum = ["right", "left", "up", "down","star", "lie"]
def yolotomy(lis, ih, iw, zoom):
    xmin = max(float(lis[0]) - float(lis[2]) / 2, 0)
    xmax = min(float(lis[0]) + float(lis[2]) / 2, 1)
    ymin = max(float(lis[1]) - float(lis[3]) / 2, 0)
    ymax = min(float(lis[1]) + float(lis[3]) / 2, 1)

    xmin = int(iw * xmin)
    xmax = int(iw * xmax)
    ymin = int(ih * ymin)
    ymax = int(ih * ymax)
    lis = xmin, ymin, xmax, ymax
    lis = list(map(lambda a: int(a * zoom), lis))
    return lis


def mytoyolo(lis, ih, iw):
    xcen = float((lis[0] + lis[2])) / 2 / iw
    ycen = float((lis[1] + lis[3])) / 2 / ih

    w = float((lis[2] - lis[0])) / iw
    h = float((lis[3] - lis[1])) / ih

    lis = f"{xcen:0.6f}", f"{ycen:0.6f}", f"{w:0.6f}", f"{h:0.6f}"

    return lis


def globli(a, a1, tj):
    di, d = [], glob.glob(f"{a}\\{a1}\\*.{tj}")
    for i in d:
        i = i[len(a) + 2 + len(a1):]
        i = i[:-4]
        di.append(int(i))
    di.sort()
    return di

def renamefile1(a, a1, a2, count):
    dri = globli(a, a1, a2)
    for c, i in enumerate(dri):
        c = c + count
        print(i, c)
        os.rename(f'{a}\\{a1}\\{str(i)}.{a2}', f'{a}\\{a1}\\{c}.txt')


# renamefile1('labels', 'arrow', 'txt', 50000)


def a2(name):
    dri = globli("images", name, "png")
    f = open(f"data\\{name}.txt", 'w')
    for i in dri:
        f.write(f"{os.getcwd()}/images/result/{i}.png\n")
    f.close()

# a2('sum')

def label(labelimg, zoom, labellist):
    dri = globli('labels', labelimg, "txt")
    for i in dri:
        f = open(f"labels\\{labelimg}\\{str(i)}.txt", 'r')
        f1 = open(f"labels\\result\\{str(i)}.txt", 'w')
        img = cv.imread(f"images\\{labelimg}\\{str(i)}.png")
        ih, iw = img.shape[:2]
        lines = f.readlines()
        for line in lines:
            linel = line.split()
            linel[1:] = list(map(float, linel[1:]))
            linel[1:] = list(map(lambda a: int(a / zoom), linel[1:]))
            linel[1:] = mytoyolo(linel[1:], ih, iw)
            linel[0] = labellist.index(linel[0])
            data = f"{linel[0]} {linel[1]} {linel[2]} {linel[3]} {linel[4]}\n"
            f1.write(data)
        f.close()
        f1.close()


# label('arrow', 4, sum)

def label1(labelimg, zoom, labellist):
    dri = globli("labels", labelimg, "txt")
    for i in dri:
        f = open(f"labels\\{labelimg}\\{str(i)}.txt", 'r')
        f1 = open(f"labels\\result\\{str(i)}.txt", 'w')
        img = cv.imread(f"images\\{labelimg}\\{str(i)}.jpg")
        ih, iw = img.shape[:2]
        lines = f.readlines()
        for line in lines:
            linel = line.split()
            linel[1:] = list(map(float, linel[1:]))
            linel[1:] = yolotomy(linel[1:], ih, iw, zoom)
            linel[0] = labellist[int(linel[0])]
            data = f"{linel[0]} {linel[1]} {linel[2]} {linel[3]} {linel[4]}\n"
            f1.write(data)
        f.close()
        f1.close()

# label1('output', 1, lies)

def makex4(dir, dir1):
    dri = globli(dir, "jpg")
    for i in dri:
        img = cv.imread(f"{dir}\\{str(i)}.jpg")
        img = cv.pyrUp(img)
        img = cv.pyrUp(img)
        cv.imwrite(f"{dir1}\\{str(i)}.jpg", img)


def retinanet():
    f1 = open("C:\\Users\\kay\\PycharmProjects\\retinanet\\keras_retinanet\\bin\\arowa.txt", 'w')
    labelo = "label\\circle"
    imglo = "image\\arrow"
    dri = globli(labelo, "txt")
    for i in dri:
        f = open(f"{labelo}\\{str(i)}.txt", 'r')
        lines = f.readlines()
        for line in lines:
            linel = line.split()
            linel[1:] = list(map(int, linel[1:]))
            linel[1:] = list(map(lambda a: int(a / 4), linel[1:]))
            data = f"arrow/{str(i)}.jpg,{linel[1]},{linel[2]},{linel[3]},{linel[4]},{linel[0]}\n"
            f1.write(data)
        f.close()
    f1.close()


def arrowcut():
    labelo = "labels\\arrow"
    imglo = "images\\arrow"
    dri = globli(labelo, "txt")
    for i in dri:
        a = 0
        f = open(f"{labelo}\\{str(i)}.txt", 'r')
        img = cv.imread(f"{imglo}\\{str(i)}.jpg")
        lines = f.readlines()
        for line in lines:
            linel = line.split()
            linel[1:] = list(map(int, linel[1:]))
            linel[1:] = list(map(lambda a: int(a / 4), linel[1:]))
            imgq = img[linel[2]:linel[4], linel[1]:linel[3]]
            imgq = cv.cvtColor(imgq, cv.COLOR_BGR2GRAY)
            cv.imwrite(f"images\\cutarrowg\\{linel[0]}\\{str(i)}{a}.jpg", imgq)
            a += 1
        f.close()
