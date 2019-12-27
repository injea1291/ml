from threading import Thread
from time import sleep
from time import time

def print_hello():
    while True:
        print("{} - Hello world!".format(int(time())))
        sleep(3)
def read_and_process_input():
    while True:
        n = int(input())
        for i in range(n):
            sleep(1)
            print(i)
def main():
    t = Thread(target=print_hello)
    t.daemon = True
    t.start() # Main thread will read and process input
    read_and_process_input()
if __name__ == '__main__':
    main()

