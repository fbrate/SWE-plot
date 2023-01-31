# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import statistics
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
import seaborn as sb

offset = 0
max = 0
boarder_start = 0
fileDir = "4k_80k"
width = 8000
height = 4000
processes = 12
w_proc = width//processes
h_proc = height//processes
plotDir = fileDir
plotTitle = str(width) + "W " + str(height) + "H " + str(processes) + "P - " + str(w_proc) + "w x " +str(h_proc) + "h per process"
fileNameApp = "mean"


def removeExtremeValuesRunTime(list):
    list.remove(list[0])
    list.remove(list[0])
    leng = len(list)
    list.remove(list[leng - 1])
    list.remove(list[leng - 2])
    return list


def removeExtremeValuesComTime(list):
    list.remove(list[0])
    list.remove(list[1])
    leng = len(list)
    list.remove(list[leng - 1])
    list.remove(list[leng - 2])
    return list


def readAverage(file, linesToRead):
    global offset
    global boarder_start
    global max
    comTimeList = []
    runTimeList = []
    scrap = file.readline()  # skip first
    for x in range(int(linesToRead) - 2):
        vals = file.readline().split(",")
        vals[2] = vals[2].removesuffix("\n")
        comTime = float(vals[2])
        runTime = float(vals[1]) - comTime
        comTimeList.append(comTime)
        runTimeList.append(runTime)
    comTimeList.sort()
    runTimeList.sort()
    com = removeExtremeValuesComTime(comTimeList)
    run = removeExtremeValuesRunTime(runTimeList)
    medianCom = np.median(com)
    medianRun = np.median(run)
    return np.median(run), np.median(com)


def open_file(name, dataList):
    global offset
    global boarder_start
    global max
    # Use a breakpoint in the code line below to debug your script.
    file = open(fileDir + "/" + name, "r")
    for line in file:
        if line == "RUN\n":
            # Do what we need to do then break
            nextLine = file.readline()
            splitLine = nextLine.split(",")
            run, com = readAverage(file, splitLine[1].removesuffix("p"))
            boarder = int(splitLine[4].removesuffix("b\n"))
            inp = boarder - offset + 1
            dataList[inp][0].append(run)
            dataList[inp][1].append(com)
            # dataList[inp][0]
            file.close()
            break


def plot_comp_time(list, name):
    labels = []
    barComp = []
    stdComp = []
    barCom = []
    stdCom = []
    avgCom = []
    avgComp = []
    i = 0
    while i < max:
        labels.append(i + offset - 1)
        barComp.append(np.mean(list[i][0]))
        barCom.append(np.mean(list[i][1]))
        stdComp.append(np.std(list[i][0]))
        stdCom.append(np.std(list[i][1]))
        # avgComp.append(np.median(list[i][0]))
        # avgCom.append(np.median(list[i][1]))
        i += 1
    # plot computation
    fix, ax = plt.subplots()
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Time (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Compute time")
    plt.tight_layout()
    plt.bar(labels, barComp, yerr=stdComp, align='center', alpha=0.8, ecolor='black', capsize=6, color="blue")
    plt.savefig("plots/" + plotDir + "/" + fileDir + "_computation")
    # plt.show()

    # plot communication
    fix, ax = plt.subplots()
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Idle time (s)")
    plt.title(plotTitle + " - Idle time")
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.bar(labels, barCom, yerr=stdCom, align='center', alpha=0.8, ecolor='black', capsize=6, color="green")
    plt.savefig("plots/" + plotDir + "/" + fileDir + "_idle")
    # plt.show()

    # combined plot

    fig, ax = plt.subplots()
    plt.title(plotTitle + " - Total Runtime")
    ax.bar(labels, barComp,
           label='Compute Time', color='blue', alpha=0.8)
    ax.bar(labels, barCom, bottom=barComp, label='Idle Time', color="red")
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Time (s)")
    ax.yaxis.grid(True)
    ax.legend(bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    plt.savefig("plots/" + plotDir + "/" + fileDir + "_combined")
    return barComp, barCom, stdComp, stdCom
    # plt.show()


# def plotB
def getPlots():
    global offset
    global boarder_start
    global max
    global fileDir
    i = 0
    lowest_boarder = 1000
    highest_boarder = 0
    for file in os.listdir(fileDir):
        boarders = file[-7:]
        boarders = boarders.strip(".out")
        index = boarders.find('_')
        boarders = boarders[index + 1:]
        if int(boarders) > highest_boarder:
            highest_boarder = int(boarders)
        if lowest_boarder > int(boarders):
            lowest_boarder = int(boarders)
    boarder_start = lowest_boarder
    offset = lowest_boarder + 1
    max = highest_boarder - lowest_boarder + 1
    dataListAverage = []
    dataListMedian = []
    for x in range(max):
        dataListAverage.append([])
        dataListAverage[x].append([])
        dataListAverage[x].append([])
    for file in os.listdir(fileDir):
        open_file(file, dataListAverage)
    for x in range(max):
        temp = dataListAverage[x][0]
        temp.sort()
        # temp.remove(temp[0])
        # temp.remove(temp[0])
        # leng = len(temp)
        # temp.remove(temp[leng-1])
        # temp.remove(temp[leng-2])
        dataListAverage[x][0] = temp

        temp = dataListAverage[x][1]
        temp.sort()
        # temp.remove(temp[0])
        # temp.remove(temp[0])
        # leng = len(temp)
        # temp.remove(temp[leng-1])
        # temp.remove(temp[leng-2])
        dataListAverage[x][1] = temp
        # remove top 2 and bot 2 for every
        # maybe top 3 and bot 3? Then need atlast 40 runs.

        barComp, barCom, stdComp, stdCom = plot_comp_time(dataListAverage.copy(), fileDir)
        return barComp, barCom, stdComp, stdCom


# Press the green button in the gutter to run the script.
def overlapPlot(barCom, barComBlock):
    global offset
    global boarder_start
    global max
    global fileDir
    global fileDir
    global plotTitle
    idle_removed = []
    overlap = []
    labels = []
    i = 0
    while i < max:
        labels.append(i + offset - 1)
        idle_removed.append(barComBlock[i] - barCom[i])

        avgComp = (barComp[i] + barCompBlock[i]) / 2

        total = avgComp + barComBlock[i]
        time_used = barComp[i] + barCom[i]
        overlap_gained = total - time_used
        overlap.append(overlap_gained)

        i += 1
    fix, ax = plt.subplots()
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Idle time removed (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Idle time removed")
    plt.tight_layout()
    plt.bar(labels, idle_removed, align='center', alpha=0.8, ecolor='black', capsize=6, color="blue")
    plt.savefig("plots/" + plotDir + "/" + fileDir + "_idleTime")

    # overlap:
    fix, ax = plt.subplots()
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Overlap (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Overlap")
    plt.tight_layout()
    plt.bar(labels, overlap, align='center', alpha=0.8, ecolor='black', capsize=6, color="blue")
    plt.savefig("plots/" + plotDir + "/" + fileDir + "_overlap")


def triplePlotGreen(com1, comp1, com2, comp2, com3, comp3, com1er, comp1er, com2er, comp2er, com3er, comp3er,
                    bcom1, bcomp1, bcom2, bcomp2, bcom3, bcomp3, bcom1er, bcomp1er, bcom2er, bcomp2er, bcom3er,
                    bcomp3er):
    name = "4k"
    plotTitle = "4000W, 4000H, 2520 iterations"
    labels = []
    total1 = []
    total2 = []
    total3 = []
    total1B = []
    total2B = []
    total3B = []
    overlap1 = []
    overlap2 = []
    overlap3 = []
    i = 0
    while i < max:
        print(i)
        labels.append(i + offset - 1)
        total1.append(com1[i] + comp1[i])
        total2.append(com2[i] + comp2[i])
        total3.append(com3[i] + comp3[i])
        total1B.append(bcom1[i] + bcomp1[i])
        total2B.append(bcom2[i] + bcomp2[i])
        total3B.append(bcom3[i] + bcomp3[i])
        overlap1.append(total1B[i] - total1[i])
        overlap2.append(total2B[i] - total2[i])
        overlap3.append(total3B[i] - total3[i])
        i += 1

    ind = np.arange(10)
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Idle Time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Waiting for communication")

    plt.bar(ind + 0 + 1, com1, width=0.3, yerr=com1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="springgreen", label='24 processes')
    plt.bar(ind + width + 1, com2, width=0.3, yerr=com2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, com3, width=0.3, yerr=com3er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_idle_wait_combined")
    # plt.show()

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Computation Time")

    plt.bar(ind + 0 + 1, comp1, width=0.3, yerr=comp1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="springgreen", label='24 processes')
    plt.bar(ind + width + 1, comp2, width=0.3, yerr=comp2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, comp3, width=0.3, yerr=comp3er, align='center', capsize=4, alpha=0.9,
            ecolor='black', color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_compute_combined")

    # combined

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Total Time")

    plt.bar(ind + 0 + 1, total1, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black', color="springgreen",
            label='24 processes')
    plt.bar(ind + width + 1, total2, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, total3, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_total")
    # plt.savefig("plots/"+name+"_combined")

    ##########
    # BLOCKING PLOTS:

    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Idle Time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Waiting for communication (Blocking)")

    plt.bar(ind + 0 + 1, bcom1, width=0.3, yerr=bcom1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="springgreen", label='24 processes')
    plt.bar(ind + width + 1, bcom2, width=0.3, yerr=bcom2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, bcom3, width=0.3, yerr=bcom3er, align='center', capsize=4, alpha=0.9,
            ecolor='black', color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_idle_wait_combined_blocking")
    # plt.show()

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Computation Time (Blocking)")

    plt.bar(ind + 0 + 1, bcomp1, width=0.3, yerr=bcomp1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="springgreen", label='24 processes')
    plt.bar(ind + width + 1, bcomp2, width=0.3, yerr=bcomp2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, bcomp3, width=0.3, yerr=bcomp3er, align='center', capsize=4, alpha=0.9,
            ecolor='black', color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_compute_combined_blocking")

    # combined

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Total Time (Blocking)")

    plt.bar(ind + 0 + 1, total1B, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black', color="springgreen",
            label='24 processes')
    plt.bar(ind + width + 1, total2B, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, total3B, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_total_blocking")
    # plt.savefig("plots/"+name+"_combined")

    # overlap combined:
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Overlap (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Overlap")

    plt.bar(ind + 0 + 1, overlap1, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black', color="springgreen",
            label='24 processes')
    plt.bar(ind + width + 1, overlap2, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="mediumseagreen", label='48 processes')
    plt.bar(ind + width + width + 1, overlap3, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="seagreen", label='72 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_overlap_combined")


def triplePlot(com1, comp1, com2, comp2, com3, comp3, com1er, comp1er, com2er, comp2er, com3er, comp3er,
               bcom1, bcomp1, bcom2, bcomp2, bcom3, bcomp3, bcom1er, bcomp1er, bcom2er, bcomp2er, bcom3er, bcomp3er):
    name = "8k"
    plotTitle = "8000W, 8000H, 2520 iterations"
    labels = []
    total1 = []
    total2 = []
    total3 = []
    total1B = []
    total2B = []
    total3B = []
    overlap1 = []
    overlap2 = []
    overlap3 = []
    i = 0
    while i < max:
        print(i)
        labels.append(i + offset - 1)
        total1.append(com1[i] + comp1[i])
        total2.append(com2[i] + comp2[i])
        total3.append(com3[i] + comp3[i])
        total1B.append(bcom1[i] + bcomp1[i])
        total2B.append(bcom2[i] + bcomp2[i])
        total3B.append(bcom3[i] + bcomp3[i])
        overlap1.append(total1B[i] - total1[i])
        overlap2.append(total2B[i] - total2[i])
        overlap3.append(total3B[i] - total3[i])
        i += 1

    ind = np.arange(10)
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Idle Time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Waiting for communication")

    plt.bar(ind + 0 + 1, com1, width=0.3, yerr=com1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, com2, width=0.3, yerr=com2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, com3, width=0.3, yerr=com3er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_idle_wait_combined")
    # plt.show()

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Computation Time")

    plt.bar(ind + 0 + 1, comp1, width=0.3, yerr=comp1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, comp2, width=0.3, yerr=comp2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, comp3, width=0.3, yerr=comp3er, align='center', capsize=4, alpha=0.9,
            ecolor='black', color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_compute_combined")

    # combined

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Total Time")

    plt.bar(ind + 0 + 1, total1, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, total2, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, total3, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_total")
    # plt.savefig("plots/"+name+"_combined")

    ##########
    # BLOCKING PLOTS:

    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Idle Time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Waiting for communication (Blocking)")

    plt.bar(ind + 0 + 1, bcom1, width=0.3, yerr=bcom1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, bcom2, width=0.3, yerr=bcom2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, bcom3, width=0.3, yerr=bcom3er, align='center', capsize=4, alpha=0.9,
            ecolor='black', color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_idle_wait_combined_blocking")
    # plt.show()

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Computation Time (Blocking)")

    plt.bar(ind + 0 + 1, bcomp1, width=0.3, yerr=bcomp1er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, bcomp2, width=0.3, yerr=bcomp2er, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, bcomp3, width=0.3, yerr=bcomp3er, align='center', capsize=4, alpha=0.9,
            ecolor='black', color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_compute_combined_blocking")

    # combined

    # compute
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Compute time (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Total Time (Blocking)")

    plt.bar(ind + 0 + 1, total1B, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, total2B, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, total3B, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_total_blocking")
    # plt.savefig("plots/"+name+"_combined")

    # overlap combined:
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Overlap (s)")
    width = 0.3
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Overlap")

    plt.bar(ind + 0 + 1, overlap1, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='72 processes')
    plt.bar(ind + width + 1, overlap2, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="cornflowerblue", label='96 processes')
    plt.bar(ind + width + width + 1, overlap3, width=0.3, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="royalblue", label='120 processes')
    plt.legend(loc='best')
    plt.savefig("plots/ok/" + name + "_overlap_combined")


def plotOverlap(com, comp, bCom, bComp):
    # overlap combined:
    labels = []
    overlap = []
    i = 0
    while i < max:
        overlap.append((bCom[i] + bComp[i]) - (com[i] + comp[i]))
        labels.append(i + offset - 1)
        i+=1
    fix, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlabel("Border Thickness (rows)")
    ax.set_ylabel("Overlap (s)")
    ax.yaxis.grid(True)
    plt.title(plotTitle + " - Overlap combined" + str())

    plt.bar(labels, overlap, width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
            color="lightsteelblue", label='12 processes')
    plt.legend(loc='best')
    plt.savefig("plots/" + plotDir + "/" + plotDir + "_overlap_combined")

if __name__ == '__main__':
    try:
        os.mkdir("plots/"+fileDir)
    except FileExistsError as exc:
        pass
    # plot overlap
    barComp, barCom, stdComp, stdCom = getPlots()
    # plot blocking
    fileDir += "_b"
    barCompBlock, barComBlock, stdCompBlock, stdComBlock = getPlots()

    #plot combined in overlap style:
    plotOverlap(barCom, barComp, barComBlock, barCompBlock)


    exit(0)
    # overlapPlot(barCom, barComBlock)
    fileDir = "8k_96"
    barComp_2, barCom_2, stdComp_2, stdCom_2 = getPlots()
    fileDir += "_b"
    barCompBlock_2, barComBlock_2, stdCompBlock_2, stdComBlock_2 = getPlots()

    fileDir = "8k_120"
    barComp_3, barCom_3, stdComp_3, stdCom_3 = getPlots()
    fileDir += "_b"
    barCompBlock_3, barComBlock_3, stdCompBlock_3, stdComBlock_3 = getPlots()
    triplePlot(barCom, barComp, barCom_2, barComp_2, barCom_3, barComp_3,
               stdCom, stdComp, stdCom_2, stdComp_2, stdCom_3, stdComp_3,
               barComBlock, barCompBlock, barComBlock_2, barCompBlock_2, barComBlock_3, barCompBlock_3,
               stdComBlock, stdCompBlock, stdComBlock_2, stdCompBlock_2, stdComBlock_3, stdCompBlock_3)
    fileDir = "4k_24"
    barComp, barCom, stdComp, stdCom = getPlots()
    fileDir += "_b"
    barCompBlock, barComBlock, stdCompBlock, stdComBlock = getPlots()
    # overlapPlot(barCom, barComBlock)
    fileDir = "4k_48"
    barComp_2, barCom_2, stdComp_2, stdCom_2 = getPlots()
    fileDir += "_b"
    barCompBlock_2, barComBlock_2, stdCompBlock_2, stdComBlock_2 = getPlots()

    fileDir = "4k_72"
    barComp_3, barCom_3, stdComp_3, stdCom_3 = getPlots()
    fileDir += "_b"
    barCompBlock_3, barComBlock_3, stdCompBlock_3, stdComBlock_3 = getPlots()
    triplePlotGreen(barCom, barComp, barCom_2, barComp_2, barCom_3, barComp_3,
                    stdCom, stdComp, stdCom_2, stdComp_2, stdCom_3, stdComp_3,
                    barComBlock, barCompBlock, barComBlock_2, barCompBlock_2, barComBlock_3, barCompBlock_3,
                    stdComBlock, stdCompBlock, stdComBlock_2, stdCompBlock_2, stdComBlock_3, stdCompBlock_3)

    # plot combined overlap from blocking and nonblocking:
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
