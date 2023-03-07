
from matplotlib import pyplot as plt
import numpy as np

dir = "hockneyData/"
fileDir = "1v2hockney_with_couples_0_1.out"
graphName = "Neighbour Cores"
def readFile(file):
    file = open(file, "r")
    # find latency
    latency = 0
    for line in file:
        s = line[0:3]
        if s == "RUN":

            # Do what we need to do then break
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            cores = (splitLine[0], splitLine[1])
            print("Latency from %d to %d is %d:", splitLine[0], splitLine[1], splitLine[2])
            latency = float(splitLine[2])
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            print("Latency from %d to %d is %d:", splitLine[0], splitLine[1], splitLine[2])
            latency = (float(latency) + float(splitLine[2]))/2
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
            dataSize = int(header[2][:-2])
            # if dataSize > 15:
            #     continue

            dataSizes.append(int(header[2][:-2]))
            tests.append(int(header[3][:-1]))
            oneWays.append(float(file.readline().split(",")[2][:-1]))
            secondWays.append(float(file.readline().split(",")[2][:-1]))
    file.close()
    return cores, dataSizes, tests, oneWays, secondWays, latency


def plot(plt, cores, dataSizes, tests, oneWays, secondWays, col, style):
    plt.title("Bandwidth between cores")
    label = cores[0] + " <-> " + cores[1]
    combined = []
    i = 0
    while i < len(oneWays):
        combined.append((oneWays[i] + secondWays[i]) / 2)
        i= i + 1
    plt.plot(dataSizes, combined, label=label, color=col, linestyle=style)

    plt.xlabel("Data Sizes (kB)")
    plt.ylabel("Bandwidth (mB/s)")
    plt.legend()

    plt.tight_layout()
    return plt


def latenciesPlot(latencies):
    i = 0
    langs = []
    vals = []
    col = []
    while i < len(latencies):
       core1 = int(latencies[i][0][0])
       core2 = int(latencies[i][0][1])
       lat = float(latencies[i][1])
       lbl = str(core1) + " <-> " + str(core2)
       langs.append(lbl)
       vals.append(lat)
       opa = 1.0
       i += 1
    plt.figure(figsize=(15,5))
    plt.title("Latency between cores")
    plt.bar(langs, vals)
    plt.xlabel("Communicating cores")
    #plt.show()
    plt.savefig("plots/hockney/latency")

if __name__ == "__main__":
    latencies = []
    cores, dataSizes, tests, oneWays, secondWays, lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plt.figure(figsize=(10,10))
    #plt.ylim(0,23000)
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "green", "dotted")
    fileDir = "1v2hockney_with_couples_1_2.out"
    cores, dataSizes, tests, oneWays, secondWays, lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "orange", "dotted")
    fileDir = "1v2hockney_with_couples_0_12.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)

    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "red", "dashed")
    fileDir = "1v2hockney_with_couples_1_13.out"
    cores, dataSizes, tests, oneWays, secondWays, lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "purple", "dashed")
    fileDir = "1v2hockney_with_couples_12_13.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "blue", "dotted")
    fileDir = "1v2hockney_with_couples_13_14.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "magenta", "dotted")

    fileDir = "1v2hockney_with_couples_0_2.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "slategrey", "dashed")


    fileDir = "1v2hockney_with_couples_0_22.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "pink", "dashed")


    fileDir = "1v2hockney_with_couples_0_23.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "violet", "dotted")


    fileDir = "1v2hockney_with_couples_12_14.out"
    cores, dataSizes, tests, oneWays, secondWays,lat = readFile(dir + fileDir)
    latencies.append((cores, lat))
    plot(plt, cores, dataSizes, tests, oneWays, secondWays, "lime", "dashed")



    print("nice!")
    plt.savefig("plots/hockney/all")
    #plt.show()

    #latenciesPlot(latencies)
