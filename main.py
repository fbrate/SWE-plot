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

offset =0
max = 0
boarder_start = 0
fileDir = "8k_72"
fileNameApp = "mean"

def removeExtremeValuesRunTime(list):
    list.remove(list[0])
    list.remove(list[0])
    leng = len(list)
    list.remove(list[leng-1])
    list.remove(list[leng - 2])
    return list

def removeExtremeValuesComTime(list):
    list.remove(list[0])
    list.remove(list[1])
    leng = len(list)
    list.remove(list[leng-1])
    list.remove(list[leng-2])
    return list


def readAverage(file, linesToRead):
    global offset
    global boarder_start
    global max
    comTimeList = []
    runTimeList = []
    scrap = file.readline() # skip first
    for x in range(int(linesToRead)-2):
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
    file = open(fileDir+"/"+name, "r")
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
    stdCom =[]
    avgCom = []
    avgComp = []
    i = 0
    while i < max:
        labels.append(i + offset-1)
        barComp.append(np.mean(list[i][0]))
        barCom.append(np.mean(list[i][1]))
        stdComp.append(np.std(list[i][0]))
        stdCom.append(np.std(list[i][1]))
        # avgComp.append(np.median(list[i][0]))
        # avgCom.append(np.median(list[i][1]))
        i+=1
    # plot computation
    fix, ax = plt.subplots()
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Runtime (s)")
    ax.yaxis.grid(True)
    plt.title(name + " computation")
    plt.tight_layout()
    plt.bar(labels, barComp, yerr=stdComp, align='center', alpha=0.8, ecolor='black', capsize=6, color="blue")
    plt.savefig("plots/"+name+"_computation_" +fileNameApp)
    #plt.show()

    # plot communication
    fix, ax = plt.subplots()
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Communication Wait (s)")
    plt.title(name + " communication")
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.bar(labels, barCom, yerr=stdCom, align='center', alpha=0.8, ecolor='black', capsize=6, color="green")
    plt.savefig("plots/"+name+"_communication_" +fileNameApp)
    #plt.show()

    # combined plot

    fig, ax = plt.subplots()
    ax.bar(labels, barComp,
           label='Computation', color='blue', alpha=0.8)
    ax.bar(labels, barCom,  bottom=barComp,label='Communication', color="red")
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    ax.set_xlabel("Boarders")
    ax.set_ylabel("Runtime (s)")
    ax.yaxis.grid(True)
    ax.legend(bbox_to_anchor=(0.5, -0.05))


    plt.tight_layout()
    plt.savefig("plots/"+name+"_combined_" +fileNameApp)
    return barComp, barCom, stdComp, stdCom
    #plt.show()


#def plotB
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
if __name__ == '__main__':
    barComp, barCom, stdComp, stdCom = getPlots()
    fileDir += "_b"
    barCompBlock, barComBlock, stdCompBlock, stdComBlock = getPlots()
    print("hei")

    # plot combined overlap from blocking and nonblocking:
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
