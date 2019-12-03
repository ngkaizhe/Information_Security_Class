from time import time

startTimes = []
SecondElapsedRecords = []


def start():
    start_time = time()
    startTimes.append(start_time)


def end(text=""):
    end_time = time()
    seconds_elapsed = end_time - startTimes.pop()
    SecondElapsedRecords.append(f"{text} part Second Used = {seconds_elapsed}\n")


def writeRecords():
    f1 = open("log.txt", "w+")
    f1.write("=================\n"
             "==================\n\n")
    for i in SecondElapsedRecords:
        f1.write(i)

    f1.write("\n\n=================\n"
             "==================\n")
