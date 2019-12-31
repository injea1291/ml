def stkey():
    def atkctrl():
        nonlocal swcont, wcont
        print(swcont,wcont)

    swcont = 0
    atkctrl()
    while True:
        swcont += 1
        wcont = 0
stkey()