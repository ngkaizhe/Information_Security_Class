from time import time

startTimes = []


def start():
    start_time = time()
    startTimes.append(start_time)


def end(text=""):
    end_time = time()
    seconds_elapsed = end_time - startTimes.pop()
    print(f"{text} part Second Used = {seconds_elapsed}")
