
import os
import numpy as np
from matplotlib import pyplot as plt

fileDir ="timing/singleTimer150_850_224"
datamap = []
WIDTH = -99
HEIGHT = -99
BORDERS = -99
PROCESES = -99
maxList = dict()
avgList = dict()
headers = []
ITER = 2520
plotDir = "timing/plots/"

def createMapIndex():
    i = 0
    while i < 10:
        datamap.append([])
        i+=1

def open_file(name):
    # Use a breakpoint in the code line below to debug your script.
    file = open(fileDir + "/" + name, "r")
    for line in file:
        if line == "RUN\n":
            global BORDER, PROCESES, WIDTH, HEIGHT
            # Do what we need to do then break
            nextLine = file.readline() # ignore header
            # retrieve borders.
            splitLine = nextLine.split(",")
            borders = int(splitLine[4].removesuffix("b\n"))
            BORDERS = borders
            processes = int(splitLine[1].removesuffix("p"))
            PROCESES = processes
            width = int(splitLine[2].removesuffix("W"))
            WIDTH = width
            headers.append(width)
            height = splitLine[3].removesuffix("H")
            HEIGHT = height
            nextLine = file.readline() # ignore first line
            s_gaps = []
            r_gaps = []
            c_gaps = []
            run_gaps = []
            i = 0
            global avgList
            global maxList
            try:
                z = avgList[name]
            except KeyError:
                avgList[name] = []
                maxList[name] = []
                while i < 10:
                    avgList[name].append(-0.9)
                    maxList[name].append(-0.9)
                    i+=1

            i = 1
            list = []
            while i < processes-1:
                nextLine = file.readline() # ignore first line.
                splitLine = nextLine.split(",")

                run = float(splitLine[1])
                datamap[BORDERS-1].append(float(splitLine[1]))
                list.append(float(splitLine[1]))
                run_gaps.append(run)
                i+=1
            i = 0
            avg = np.average(list)
            m = np.max(list)
            avgList[name][BORDERS-1] = avg
            maxList[name][BORDERS-1] = m
            while i < 10:
                datamap[i] = sorted(datamap[i])
                i += 1
            continue

def plotAvgList():
    i = 0
    x_axis = []
    while i < 10:
        x_axis.append(i + 1)
        i+=1
    h_per = int(int(HEIGHT)/int(PROCESES))
    plotTitle = "Runtime for various border exchange widths - " + str(WIDTH) + "W, " + str(h_per) + "H, " + str(PROCESES) + "P "
    fix, ax = plt.subplots(figsize=(15, 5))
    ax.set_xlabel("Border Exchange Thickness")
    ax.set_ylabel("Runime (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle)
    for key in avgList.keys():
        list = avgList[key]
        plt.plot(x_axis, list)


    plt.savefig(plotDir + "Individual_"+ str(WIDTH) + "W_"+ str(h_per) +"H_" + str(PROCESES) + "P.png")
    return

def plotMaxList():
    i = 0
    x_axis = []
    while i < 10:
        x_axis.append(i + 1)
        i+=1
    h_per = int(int(HEIGHT)/int(PROCESES))
    plotTitle = "Runtime for various border exchange widths - " + str(WIDTH) + "W, " + str(h_per) + "H, " + str(PROCESES) + "P "
    fix, ax = plt.subplots(figsize=(15, 5))
    ax.set_xlabel("Border Exchange Thickness")
    ax.set_ylabel("Runime (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle)
    for key in maxList.keys():
        list = maxList[key]
        plt.plot(x_axis, list)


    plt.savefig(plotDir + "IndividualMax_"+ str(WIDTH) + "W_"+ str(h_per) +"H_" + str(PROCESES) + "P.png")
    return

if __name__ == "__main__":
    createMapIndex()
    for file in os.listdir(fileDir):
        open_file(file)

    avgs = []
    standards = []
    median = []
    i = 0
    x_axis = []
    while i < 10:
        x_axis.append(i+1)
        avgs.append(np.average(datamap[i]))
        median.append(np.median(datamap[i]))
        standards.append(np.std(datamap[i]))
        i+=1

    #print(datamap)
    h_per = int(int(HEIGHT)/int(PROCESES))
    plotTitle = "Runtime for various border exchange widths - " + str(WIDTH) + "W, " + str(h_per) + "H, " + str(PROCESES) + "P "
    fix, ax = plt.subplots(figsize=(15, 5))
    ax.set_xlabel("Border Exchange Thickness")
    ax.set_ylabel("Runime (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle)

    plt.bar(x_axis, avgs, yerr=standards, capsize=6, color="lightsteelblue", alpha=0.8)
    plt.savefig(plotDir + "Bar_"+ str(WIDTH) + "W_"+ str(h_per) +"H_" + str(PROCESES) + "P")
    # print("RUN," + width + "," + height)
        # while i < 10:
        #     communications = 2520/(i+1)
        #     snd_pr = snd / communications
        #     rcv_pr = rcv / communications
        #     tot = snd_pr + rcv_pr + com
        #     print("b" + str(i+1) + " " + str(snd_pr) + " " + str(rcv_pr) + " " + str(com) + " " + str(tot))
        #     i+=1
    plotAvgList()
    plotMaxList()
