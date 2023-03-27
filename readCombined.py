
import os
import numpy as np
import math
fileDir ="combined"
blocking = dict()
sgap = dict()
rgap = dict()
vgap = dict()
comgap = dict()
edgecalc = dict()
corecalc = dict()


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
    file = open(fileDir + "/test.txt", "r")
    # find latency
    latency = 0
    # possible tags:
    # COMBLO
    # COMGAP
    # EDGECA
    # CORECA
    for nextline in file:
        s = nextline[0:6]
        # find start of datafiles.
        if s == "COMBLO":
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
                    blocking[width].append(float(splitLine[i]))
                    i+=1
        while True:
            nextline = file.readline().removesuffix("\n")
            if(nextline[0:6] == "EDGECA"):
                break
            # Do what we need to do then break
            splitLine = nextline.split(",")

            width = int(splitLine[0])
            sgap[width] = []
            rgap[width] = []
            vgap[width] = []
            i = 2
            while i < len(splitLine):
                deciSplit = splitLine[i].split(";")
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
            edgecalc[width] = []
            i = 3
            while i < len(splitLine):
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



if __name__ == "__main__":
    open_file("")
    f = open("combinedBlock.txt", "w")
    f.write("BLOCKING: Size, Median, Average, Standard Deviation\n")
    for i in sorted(blocking.keys()):
        # Write for each and numpy median each border for each width.
        list = blocking[i]
        avg = np.average(list)
        med = np.median(list)
        std = np.std(list)
        f.write(str(i)+ "," + str(med) + "," + str(avg) +"," + str(std) + "\n")
    f.write("COMGAP: Size, SRV Median, SRV, Average, SRV Standard Deviation\n")

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
        f.write(str(math.floor(i))+ "," + str(smed)+";" + str(savg) +";" + str(sstd) + "," + str(rmed)+";" + str(ravg) +";" + str(rstd) +"," + str(vmed)+";" + str(vavg) +";" + str(vstd) +"\n")
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
        f.write(str(splitline[0]) + "," + str(halo) + ","+str(med) + "," + str(avg) +"," + str(std) + "\n")
    f.write("#####################################################\nCORECALC: SizeW, SizeH, Halo, Median, Average, Standard Deviation\n")
    for i in sorted(corecalc.keys()):
        # Write for each and numpy median each border for each width.
        for j in corecalc[i].keys():
            heightHalo = str(j).split(".")
            list = corecalc[i][j]
            avg = np.average(list)
            med = np.median(list)
            std = np.std(list)
            f.write(str(i) + "," +str(heightHalo[0]) + "," + str(heightHalo[1]) + ","+str(med) + "," + str(avg) +"," + str(std) + "\n")
    f.close()
