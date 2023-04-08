from prettytable import PrettyTable
import os
import numpy as np
from scipy.stats import kstest
import math
import matplotlib.pyplot as plt
fileDir ="combined112"
datafile = "getDataUpdated_1.out"
plotdir = "combined112Plots"
resultdir = plotdir + "/results/"
blocking = dict()
sgap = dict()
rgap = dict()
vgap = dict()
edgecalc = dict()
corecalc = dict()

plotting = False
plotAverages = False


block = dict()
gap = dict()
edges = dict()
core = dict()

headers = []
ITER = 2520


def max(a, b):
    if a >= b:
        return a
    else:
        return b

# def createMapIndex(key):
#     datamap[key] = ([],[],[],[],[])
#     i = 0
#     while i < 10:
#         datamap[key][0].append([])
#         datamap[key][1].append([])
#         datamap[key][2].append([])
#         datamap[key][3].append([])
#         i+=1

def open_file(name):
    # Use a breakpoint in the code line below to debug your script.
    file = open(fileDir + "/" + datafile, "r")
    # find latency
    latency = 0
    # possible tags:
    # COMBLO
    # COMGAP
    # EDGECA
    # CORECA
    global sgap
    global rgap
    global vgap
    global corecalc
    global edgecalc
    global blocking
    start = 0
    for nextline in file:
        s = nextline[0:6]
        # find start of datafiles.
        if s == "COMBLO":
            start = 1
            while True:
                nextline = file.readline().removesuffix("\n")
                if(nextline[0:6] == "COMGAP"):
                    break
                # Do what we need to do then break
                splitLine = nextline.split(",")
                width = int(splitLine[0])
                blocking[width] = []
                i = 1
                while i < len(splitLine):
                    try:
                        if (float(splitLine[i]) == 0):
                            i+=1
                            continue
                        if(float(splitLine[i] == 7.0)):
                            print("found")
                        blocking[width].append(float(splitLine[i]))

                    except ValueError as e:
                        print("Block splitline at " + str(i) + "got error " + str(e))

                    i+=1
        if (start == 1):
            while True:
                nextline = file.readline().removesuffix("\n")
                if(nextline[0:6] == "EDGECA"):
                    break
                # Do what we need to do then break
                splitLine = nextline.split(",")

                width = int(splitLine[0])
                try:
                    sgap[width]
                except KeyError:
                    sgap[width] = []
                    rgap[width] = []
                    vgap[width] = []
                i = 2
                while i < len(splitLine):
                    deciSplit = splitLine[i].split(";")
                    if len(deciSplit) != 3:
                        i+=1
                        continue
                    if float(deciSplit[0]) == 0:
                        i+=1
                        continue
                    if float(deciSplit[0]) == 0:
                        i+=1
                        continue
                    if float(deciSplit[0]) == 0:
                        i+=1
                        continue
                    sgap[width].append(float(deciSplit[0]))
                    rgap[width].append(float(deciSplit[1]))
                    vgap[width].append(float(deciSplit[2]))
                    i+=1

            # edgecalc
            while True:
                nextline = file.readline().removesuffix("\n")
                if (nextline[0:6] == "CORECA"):
                    break
                splitLine = nextline.split(",")



                width = int(splitLine[0]) + (int(splitLine[2])/10)
                try:
                    edgecalc[width]
                except KeyError:
                    edgecalc[width] = []
                i = 3
                while i < len(splitLine):
                    if (float(splitLine[i]) == 0):
                        i+=1
                        continue
                    edgecalc[width].append(float(splitLine[i]))
                    i+=1

            # corecalc
            indenter = 1;
            while True:
                nextline = file.readline().removesuffix("\n")
                if (nextline[0:4] == "TIME"):
                    break
                splitLine = nextline.split(",")

                tag = str(int(splitLine[1])) + "."+ str(int(splitLine[3]))
                key = int(splitLine[0])
                if key not in corecalc.keys():
                    corecalc[key] = dict()
                i = 4
                try:
                    var = len(corecalc[key][tag])
                except KeyError:
                    corecalc[key][tag] = []
                while i < len(splitLine):
                    corecalc[key][tag].append(float(splitLine[i]))
                    i += 1
            break

def removeExtremes():
    for i in sorted(blocking.keys()):
        list = sorted(blocking[i])
        leng = len(list)
        leng = leng/100
        j = 0
        while j < leng:
            if j % 2 == 0:
                list.pop(0)
            else:
                list.pop()
            j += 1
        blocking[i] = list
    #rgap
    for i in sorted(rgap.keys()):
        list = sorted(rgap[i])
        leng = len(list)
        leng = leng/100
        j = 0
        while j < leng:
            if j % 2 == 0:
                list.pop(0)
            else:
                list.pop()
            j += 1
        rgap[i] = list
    #sgap
    for i in sorted(sgap.keys()):
        list = sorted(sgap[i])
        leng = len(list)
        leng = leng/100
        j = 0
        while j < leng:
            if j % 2 == 0:
                list.pop(0)
            else:
                list.pop()
            j += 1
        sgap[i] = list
    #vgap
    for i in sorted(vgap.keys()):
        list = sorted(vgap[i])
        leng = len(list)
        leng = leng/100
        j = 0
        while j < leng:
            if j % 2 == 0:
                list.pop(0)
            else:
                list.pop()
            j += 1
        vgap[i] = list

    # EdgeCalc
    #
    for i in sorted(edgecalc.keys()):

        list = sorted(edgecalc[i])
        leng = len(list)
        leng = leng / 100
        if leng < 1 :
            leng = 1.5
        j = 0
        while j < leng:
            if j % 2 == 0:
                list.pop(0)
            else:
                list.pop()
            j += 1
        edgecalc[i] = list
    for i in sorted(corecalc.keys()):
        for j in sorted(corecalc[i].keys()):
            list = sorted(corecalc[i][j])
            leng = len(list)
            leng = leng / 100
            if leng < 1 :
                leng = 1.5
            k = 0
            while k < leng:
                if k % 2 == 0:
                    list.pop(0)
                else:
                    list.pop()
                k += 1
            corecalc[i][j] = list


def readDataFiles():
    open_file("")
    removeExtremes()
    global blocking
    global edgecalc
    global corecalc
    global sgap, vgap, rgap
    f = open(resultdir+ "combinedBlock.txt", "w")
    tbl = open(resultdir+ "tableBlock.txt", "w")
    t = PrettyTable(["Size", "Median", "Average", "Standard Deviation", "%"])
    f.write("BLOCKING: Size, Median, Average, Standard Deviation\n")
    comNormal = 0
    comTotal = 0
    for i in sorted(blocking.keys()):

        # Write for each and numpy median each border for each width.
        list = blocking[i]
        avg = np.average(list)
        med = np.median(list)
        std = np.std(list)

        perc = std / avg * 100
        block[i] = (med, avg, std, perc)
        f.write(str(i)+ "," + str(med) + "," + str(avg) +"," + str(std) + "," + str(round(perc,1)) +"%\n")
        t.add_row([i, med, avg, std, round(perc,1)])
        sor = sorted(blocking[i])
        normaly = kstest(list, 'norm')
        if (normaly[1] > 0.05):
            comNormal+=1
        comTotal +=1
        if plotting:
            plotList = sorted(list)
            title = "Block" + str(i)
            print("Plot " + title)
            plt.plot(plotList, label=title)
            plt.savefig(plotdir + "/block/block" + str(i))
            plt.close()
    tbl.write(str(t))
    tbl.close()
    t = PrettyTable(["Size","Send Median", "Recv Median", "Verify Median" ,"Send Average", " Recv Average", "Verify Average", "Send Std", "Recv Std", "Verify Std"])
    f.write("COMGAP: Size, SRV Median, SRV, Average, SRV Standard Deviation\n")
    print("BLOCKINGCOM normals:"+ str(comNormal))

    tbl = open(resultdir+ "tableGap.txt", "w")
    sTotal = 0
    rTotal  = 0
    vTotal = 0
    sNormal = 0
    rNormal = 0
    vNormal = 0
    for i in sorted(sgap.keys()):
        savg = np.average(sgap[i])
        ravg = np.average(rgap[i])
        vavg = np.average(vgap[i])

        smed = np.median(sgap[i])
        rmed = np.median(rgap[i])
        vmed = np.median(vgap[i])

        sstd = np.std(sgap[i])
        rstd = np.std(rgap[i])
        vstd = np.std(vgap[i])

        vperc = vstd/vavg * 100
        sperc = sstd/ravg * 100
        rperc = rstd/ravg * 100
        sNor = kstest(sgap[i], 'norm')
        rNor = kstest(rgap[i], 'norm')
        vNor = kstest(vgap[i], 'norm')
        if (sNor[1] > 0.05):
            sNormal+=1
        if (rNor[1] > 0.05):
            rNormal+=1
        if (vNor[1] > 0.05):
            vNormal+=1



        if plotting:
            plotList = sorted(rgap[i])
            title = "rgap" + str(i)
            print("Plot " + title)
            plt.plot(plotList, label=title)
            plt.savefig(plotdir + "/gap/rgap" + str(i))
            plt.close()
            plotList = sorted(sgap[i])
            title = "sgap" + str(i)
            print("Plot " + title)
            plt.plot(plotList, label=title)
            plt.savefig(plotdir + "/gap/sgap" + str(i))
            plt.close()
            plotList = sorted(vgap[i])
            title = "vgap" + str(i)
            print("Plot " + title)
            plt.plot(plotList, label=title)
            plt.savefig(plotdir + "/gap/vgap" + str(i))
            plt.close()

        vTotal+=1
        rTotal+=1
        sTotal+=1


        gap[i] = ((smed, savg, sstd, sperc),(rmed,ravg,rstd,rperc),(vmed,vavg,vstd,vperc))

        f.write(str(math.floor(i))+ "," + str(smed)+";" + str(savg) +";" + str(sstd) + "," + str(rmed)+";" + str(ravg) +";" + str(rstd) +"," + str(vmed)+";" + str(vavg) +";" + str(vstd) +"\n")
        t.add_row([str(math.floor(i)), med, rmed, vmed, savg, ravg, vavg, sstd, rstd, vstd])
    # print("SGAP :" +str(sNormal) + "/" + str(sTotal))
    # print("RGAP :" +str(rNormal) + "/" + str(rTotal))
    # print("VGAP :" +str(rNormal) + "/" + str(vTotal))
    tbl.write(str(t))
    tbl.close()
    tbl = open(resultdir+ "tableEdge.txt", "w")
    t = PrettyTable(["Size", "HALO" ,"Median", "Average", "Standard Deviation", "%"])
    f.write("EDGECALC: Size, Halo, Median, Average, Standard Deviation\n")
    for i in sorted(edgecalc.keys()):
        # Write for each and numpy median each border for each width.
        list = edgecalc[i]
        splitline = str(i).split(".")
        halo = 11
        if int(splitline[0]) % 10 == 1:
            halo = 10
            splitline[0] = int(splitline[0]) - 1
        else:
            halo = splitline[1]
        avg = np.average(list)
        med = np.median(list)
        std = np.std(list)
        perc = std / avg * 100
        edges[i] = (med,avg,std,perc)
        sor = sorted(edgecalc[i])

        if plotting:
            plotList = sorted(list)
            title = "edge" + str(i)
            print("Plot " + title)
            plt.plot(plotList, label=title)
            plt.savefig(plotdir + "/edge/edge" + str(i) +".png")
            plt.close()

        f.write(str(splitline[0]) + "," + str(halo) + ","+str(med) + "," + str(avg) +"," + str(std) + "," + str(round(perc,1)) +"%\n")
        t.add_row([str(splitline[0]), halo, med, avg, std, round(perc,1)])
    f.write("#####################################################\nCORECALC: SizeW, SizeH, Halo, Median, Average, Standard Deviation, std % of avg\n")
    tbl.write(str(t))
    tbl.close()
    tbl = open(resultdir+ "tableCore.txt", "w")
    t = PrettyTable(["Size W", "Size H", "Halo","Median", "Average", "Standard Deviation", "%"])
    global corecalc
    for i in sorted(corecalc.keys()):
        # Write for each and numpy median each border for each width.
        core[i] = dict()
        for j in corecalc[i].keys():
            heightHalo = str(j).split(".")
            list = corecalc[i][j]
            avg = np.average(list)
            med = np.median(list)
            std = np.std(list)
            perc = std/avg * 100
            core[i][j]= (med,avg,std,perc)
            f.write(str(i) + "," +str(heightHalo[0]) + "," + str(heightHalo[1]) + ","+str(med) + "," + str(avg) +"," + str(std) + "," + str(round(perc,1)) +"%\n")
            t.add_row([str(i), str(heightHalo[0]), str(heightHalo[1]), med, avg, std, round(perc,1)])
            if plotting:
                plotList = sorted(corecalc[i][j])
                title = "core" + str(i) + "_" + str(j) + ".png"
                print("Plot " + title)
                plt.plot(plotList, label=title)
                plt.savefig(plotdir + "/core/" + title)
                plt.close()
            # corecalc[i][j] = sorted(corecalc[i][j])
    f.close()

    tbl.write(str(t))
    tbl.close()
    # corecalc = None
    # edgecalc = None
    # blocking = None
    # sgap = None
    # vgap = None
    # rgap = None


def findValidGapCore():
    iterations = 2520
    # compare gaps added
    # gaps need to be multiplied by each direciton sent. 2 for horizontal.
    # same goes for edge.
    special = PrettyTable(
        ["HALO", "Width", "Height", "Gap/Sstep", "CCalc/Sstep", "EdgeCalc/Sstep", "Ssteps", "Block time",
         "Core Time > Block Time", "(ECalc + CCalc + Gap) * Ssteps", "%", "OG run"])
    for w in sorted(core.keys()):
        halo =1
        key = str(100) + "." + str(halo)
        key = float(key)
        gapsTuple = gap[w]
        blockTuple = block[w]
        coreTuple = core[w]
        # blockTuple = block[w]
        # gets each of the average valus and adds them
        gapsAvg = gapsTuple[0][1] + gapsTuple[1][1] + gapsTuple[2][1]
        # this one also adds the std deviation for eachgapsTuple[0][1] + gapsTuple[1][1] + gapsTuple[2][1]
        # gapsAvgPlus = gapsTuple[0][1] + gapsTuple[1][1] + gapsTuple[2][1] + gapsTuple[0][2] + gapsTuple[1][2] + gapsTuple[2][2]
        gapsAvg *= 2 # multiply by two since we send in two directions.
        # gapsAvgPlus *= 2 # multiply by two since we send in two directions.
        supersteps = 2520
        t = PrettyTable(["HALO", "Width", "Height", "Gap/Sstep", "CCalc/Sstep", "EdgeCalc/Sstep"
                            , "Ssteps", "Block time", "Core Time > Block Time","(ECalc + CCalc + Gap) * Ssteps", "%", "OG run"])
        # tK = PrettyTable(['Border Thickness', 'Stencil Points', 'Extra Points / Sstep', 'Ssteps', 'Communications' 'Gap time each Sstep', 'Comm gap * Supersteps', 'Extra points  * Calc speed', 'Runtime', '% increase'])



        # if average % with std is greater than say 10%.
        # Use median instead. Maybe append 50% of std?
        timeOG = 0
        #print("Calculating for width: " + str(w) + "\n --", end = "")
        for h in coreTuple.keys():
            #print(", " +str(h), end="")
            splitH = h.split(".")
            halo = int(splitH[1])
            supersteps = 2520 * (1/halo)
            coreSpeed = coreTuple[h][1]
            edgeAvg = edges[float(h)][1]
            blockTime = blockTuple[1]
            # total time
            time = edgeAvg + gapsAvg + coreSpeed
            time *= supersteps
            coreOverBlock = False
            if coreSpeed > blockTime:
                coreOverBlock = True
            perc = 100
            if splitH[1] == '1':
                timeOG = time
            else:
                perc = time/timeOG * 100

            # write to width file under subfolder
            t.add_row([splitH[1], w, splitH[0], gapsAvg, coreSpeed, edgeAvg, supersteps, blockTime, coreOverBlock, time, perc, timeOG])

            # append to a special file under each subfolder.
            if (perc < 100 and coreOverBlock is True):
                special.add_row([splitH[1], w, splitH[0], gapsAvg, coreSpeed, edgeAvg, supersteps, blockTime, coreOverBlock, time,
                           perc, timeOG])

        # print(t)
        s = open(resultdir  + str(w) + ".txt", "w")
        s.write(str(t))
        s.close()

    # end for each width
    if special:
        s = open(resultdir + "special.txt", "w")
        s.write(str(special))
        s.close()
        print()

    # print(special)
    # FLOW:
    # get gap for a size. time with 2.
    # get blocking for that size. Time it with 2 or 3?
    # find coreCalc which is longer than the block.

    # estimate time with EdgeCalc, GAP and Corecalc.
    # compare to halo 1 and percentage bases output. Store good cases in own file.


    # add the edgecalc at last.

    # baseline = 2520 * gap halo 1
    # baseline += core(halo1) + (edge * 2)


def plotAverages():
    if plotAverages:
        # Block

        list = block
        x_axis = []
        averageValues = []
        copy = sorted(blocking[200], reverse=True)
        for i in list.keys():
            x_axis.append(int(i))
            averageValues.append(float(list[i][1]))

        fix, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel("Stencil points per communication")
        ax.set_ylabel("Time (s)")
        ax.yaxis.grid(True)
        plt.title("")

        plt.bar(x_axis, averageValues, width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
                color="lightsteelblue")
        plt.savefig(plotdir + "/avg/block")


        # Gap

        list = sgap
        x_axis = []
        averageValues = []
        for i in list.keys():
            x_axis.append(int(i))
            averageValues.append(float(np.average(list[i])))

        fix, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel("Stencil points per communication")
        ax.set_ylabel("Time (s)")
        ax.yaxis.grid(True)
        plt.title("")

        plt.bar(x_axis, averageValues, width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
                color="lightsteelblue")
        plt.savefig(plotdir + "/avg/sgap")
        list = rgap
        x_axis = []
        averageValues = []
        for i in list.keys():
            x_axis.append(int(i))
            averageValues.append(float(np.average(list[i])))

        fix, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel("Stencil points per communication")
        ax.set_ylabel("Time (s)")
        ax.yaxis.grid(True)
        plt.title("")

        plt.bar(x_axis, averageValues, width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
                color="lightsteelblue")
        plt.savefig(plotdir + "/avg/rgap")
        list = vgap
        x_axis = []
        averageValues = []
        copy = sorted(blocking[200], reverse=True)
        for i in list.keys():
            x_axis.append(int(i))
            averageValues.append(float(np.average(list[i])))

        fix, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel("Stencil points per communication")
        ax.set_ylabel("Time (s)")
        ax.yaxis.grid(True)
        plt.title("")

        plt.bar(x_axis, averageValues, width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
                color="lightsteelblue")
        plt.savefig(plotdir + "/avg/vgap")
        # Edge
        values = dict()
        i = 0
        for i in edges.keys():
            split = str(i).split(".")
            width = int(split[0])
            halo = int(split[1])
            if(halo == 0):
                width -= 1
                halo = 10
            try:
                k = values[width]
            except KeyError:
                values[width] = []
            values[width].append(edges[i][1])
        labels = [1,2,3,4,5,6,7,8,9,10]
        for i in values:
            fix, ax = plt.subplots(figsize=(10, 5))
            ax.set_xlabel("HALOS")
            ax.set_ylabel("Time Calculation")
            ax.yaxis.grid(True)
            plt.title("")

            plt.bar(labels, values[i], width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
                    color="lightsteelblue", label="1")
            plt.savefig(plotdir + "/avg/edge/edge" + str(i) +".png")
            plt.close()
        # Core
        # DO THIS BUT FOR every j in coreedges.
        for j in corecalc.keys():
            values = dict()
            i = 0
            for i in corecalc[j].keys():
                split = str(i).split(".")
                width = int(split[0])
                halo = int(split[1])
                if(halo == 0):
                    width -= 1
                    halo = 10
                try:
                    k = values[width]
                except KeyError:
                    values[width] = []
                values[width].append(core[j][i][1])
            labels = [1,2,3,4,5,6,7,8,9,10]
            for i in values:
                try:
                    os.makedirs(plotdir+"/avg/core/" + str(j))
                except FileExistsError:
                    pass
                fix, ax = plt.subplots(figsize=(10, 5))
                ax.set_xlabel("HALOS")
                ax.set_ylabel("Time Calculation")
                ax.yaxis.grid(True)
                plt.title("")

                plt.bar(labels, values[i], width=1.0, align='center', capsize=4, alpha=0.9, ecolor='black',
                        color="lightsteelblue", label="1")
                plt.savefig(plotdir + "/avg/core/" + str(j) + "/" + str(i)+ ".png")
                plt.close()

def createEnvironment():
    try:
        os.makedirs(plotdir)
    except FileExistsError:
        print("Plotdir exists.")
    try:
        os.makedirs(plotdir + "/avg")
        os.makedirs(plotdir + "/block")
        os.makedirs(plotdir + "/core")
        os.makedirs(plotdir + "/edge")
        os.makedirs(plotdir + "/gap")
        os.makedirs(plotdir + "/avg/edge")
        os.makedirs(plotdir + "/avg/core")
        os.makedirs(resultdir)
    except FileExistsError:
        print("Subplotdirs exists.")


if __name__ == "__main__":
    createEnvironment()
    readDataFiles()
    plotAverages()
    #findValidGapCore()
    # I think we need to plot the gaps, blocks, edgeCalc and corecalc.
