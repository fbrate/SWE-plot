
from matplotlib import pyplot as plt
import numpy as np
import os

dir = "oneRank"
def readFile(file, l500, l1000, l2000, all):
    file = open(file, "r")
    # find latency
    latency = 0
    for line in file:
        if line == "RUN\n":
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            type = splitLine[2]
            if type == "500W":
                nextLine= file.readline()
                splitLine = nextLine.split(",")
                l500.append(float(splitLine[3].removesuffix("\n")))
                all.append(float(splitLine[3].removesuffix("\n")))

            elif type == "1000W":
                nextLine= file.readline()
                splitLine = nextLine.split(",")
                l1000.append(float(splitLine[3].removesuffix("\n")))
                all.append(float(splitLine[3].removesuffix("\n")))
            elif type == "2000W":
                nextLine= file.readline()
                splitLine = nextLine.split(",")
                l2000.append(float(splitLine[3].removesuffix("\n")))
                all.append(float(splitLine[3].removesuffix("\n")))
            else:
                print("Unkown type: " + type)





if __name__ == "__main__":
    l500 = []
    l1000 = []
    l2000 = []
    all = []
    for file in os.listdir(dir):
        print(file)
        readFile(dir+ "/" + file, l500, l1000, l2000, all)


    print("RUN 500:")
    print("Average: "+ str(np.average(l500) * 3))
    print("Median : "+ str(np.median(l500) * 3))
    print("Max    : "+ str(np.max(l500) * 3))
    print("Min    : "+ str(np.min(l500) * 3))
    print("\nRUN 1000:")
    print("Average: "+ str(np.average(l1000) * 3))
    print("Median : "+ str(np.median(l1000)*3))
    print("Max    : "+ str(np.max(l1000)*3))
    print("Min    : "+ str(np.min(l1000)*3))
    print("\nRUN 2000:")
    print("Average: "+ str(np.average(l2000)*3))
    print("Median : "+ str(np.median(l2000)*3))
    print("Max    : "+ str(np.max(l2000)*3))
    print("Min    : "+ str(np.min(l2000)*3))
    print("\nRUN ALL:")
    print("Average: " + str(np.average(all) * 3))
    print("Median : " + str(np.median(all) * 3))
    print("Max    : " + str(np.max(all) * 3))
    print("Min    : " + str(np.min(all) * 3))
