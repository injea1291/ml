import winsound
import threading
import time

def asd():
    winsound.Beep(262, 1000)

t = threading.Thread(target=asd, daemon=True)
while True:
    print(1)
    if t.is_alive() == False:
        t = threading.Thread(target=asd, daemon=True)
        t.start()
