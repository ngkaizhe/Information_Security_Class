from time import time

startTimes = []
endTimes = []
SecondElapsedRecords = []
first = [0]


def start():
    start_time = time()
    startTimes.append(start_time)
    first[0] = startTimes[0]


def end(text=""):
    end_time = time()
    seconds_elapsed = end_time - startTimes.pop()
    SecondElapsedRecords.append(f"{text} part Second Used = {seconds_elapsed}\n")


def writeRecords(new=True):
    if new:
        f1 = open("log.txt", "w+")
    else:
        f1 = open("log.txt", "a+")

    f1.write("=================\n"
             "==================\n\n")
    for i in SecondElapsedRecords:
        f1.write(i)

    SecondElapsedRecords.clear()
    f1.write("\n\n=================\n"
             "==================\n")
    f1.close()
