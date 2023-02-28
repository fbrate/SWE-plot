
from matplotlib import pyplot as plt
import numpy as np

fileDir = "hockneyData/test.txt"
graphName = "Neighbour Cores"
def readFile(file):
    file = open(file, "r")
    # find latency

    for line in file:
        s = line[0:3]
        if s == "RUN":

            # Do what we need to do then break
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            cores = (splitLine[0], splitLine[1])
            print("Latency from %d to %d is %d:", splitLine[0], splitLine[1], splitLine[2])
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            print("Latency from %d to %d is %d:", splitLine[0], splitLine[1], splitLine[2])
            break
    # now next lines should be 3x iterations over bandwidth data.
    dataSizes =[]
    tests = []
    oneWays = []
    secondWays = []
    for line in file:
        s = line[0:3]
        if s == "RUN":
            header = line.split(",")
            dataSizes.append(int(header[2][:-2]))
            tests.append(int(header[3][:-1]))
            oneWays.append(float(file.readline().split(",")[2][:-1]))
            secondWays.append(float(file.readline().split(",")[2][:-1]))
    file.close()
    return cores, dataSizes, tests, oneWays, secondWays


def plot(cores, dataSizes, tests, oneWays, secondWays):
    plt.figure(figsize=(5,5))
    plt.title("Core " + cores[0] + " to core " + cores[1] + " bandwidth")
    plt.plot(dataSizes, oneWays, label="Core 0 to 1", color="green")
    plt.plot(dataSizes, secondWays, label="Core 0 to 1", color="red")

    plt.xlabel("Data Sizes (kB)")
    plt.ylabel("Bandwidth (mB/s)")

    plt.tight_layout()
    plt.show()
    #plt.savefig("plots/hockney/" + cores[0] + "_" + cores[1])

if __name__ == "__main__":
    cores, dataSizes, tests, oneWays, secondWays = readFile(fileDir)
    plot(cores, dataSizes, tests, oneWays, secondWays)
    print("nice!")