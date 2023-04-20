
import os
import numpy as np
from matplotlib import pyplot as plt

fileDir ="timing/singleTimer150_1700_112"
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
HALOS = 10
allPerc = []

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

def addlabels(x,y,loc):
    for i in range(len(x)):
        val = str(round(y[i], 2)) + "%"
        plt.text(i+1, loc, val, ha = 'center')

if __name__ == "__main__":

    createMapIndex()
    for file in os.listdir(fileDir):
        open_file(file)

    avgs = []
    standards = []
    median = []
    i = 0
    x_axis = []
    while i < HALOS:
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

    #plt.bar(x_axis, avgs, yerr=standards, capsize=6, color="lightsteelblue", alpha=0.8)
    perc = []
    i = 1
    og = avgs[0]
    x_axis = []
    perc.append(100)
    x_axis.append("1\n100%")
    while i < HALOS:
        per = avgs[i]/og * 100
        perc.append(per)
        x_axis.append(str(i) + "\n" +str(round(per,2)) + "%")
        i+=1

    # i = 0
    # while i < 10:
    #     x_axis.append(i + 1)
    #     i += 1

    # Creating axes instance
    # ax = fig.add_axes([0, 0, 1, 1])

    # Creating plot
    # bp = ax.boxplot(datamap)
    bp = ax.boxplot(datamap, labels=x_axis)
    plt.savefig(plotDir + "Box_"+ str(WIDTH) + "W_"+ str(h_per) +"H_" + str(PROCESES) + "P.png")
    plt.close()
    title = str(WIDTH) + "W_"+ str(h_per) +"H_" + str(PROCESES)+ "P"
    allPerc.append((title,perc))
