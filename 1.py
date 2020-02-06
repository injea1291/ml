import os, sys, time


class MyError(Exception):
    pass


class MyError2(Exception):
    pass


def asdf(asd):
    if asd == 1:
        raise MyError
    elif asd == 2:
        raise MyError2
    print(asd)


try:
    asdf(1)
except MyError:
    print('MyError발생')
except MyError2:
    print('MyError2발생')
