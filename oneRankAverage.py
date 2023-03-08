
import os
import numpy as np
fileDir ="oneRankData"

def open_file(name):
    # Use a breakpoint in the code line below to debug your script.
    file = open(fileDir + "/" + name, "r")
    for line in file:
        if line == "RUN\n":
            # Do what we need to do then break
            nextLine = file.readline()
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            splitLine[3] = splitLine[3][1:]
            # dataList[inp][0]
            file.close()
            return float(splitLine[3])


if __name__ == "__main__":
    values = []
    for file in os.listdir(fileDir):
        values.append(open_file(file))
    values = np.sort(values)
    values.pop(0)
    values.pop(len(values)-1)
    median = np.median(values)
    deviation = np.std(values)
    print("Median:       " + str(median))
    print("Median - std: "+ str(median-deviation))
    print("Median + std: "+ str(median+ deviation))
    print("std:           " + str(deviation))
