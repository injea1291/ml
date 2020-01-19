import asyncio
import datetime
import random


def coro():
    while True:
        hello = yield 15
        yield hello


c = coro()


