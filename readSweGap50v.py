
import os
import numpy as np
fileDir ="50v"
datamap = dict()
headers = []
ITER = 2520

def createMapIndex(key):
    datamap[key] = ([],[],[],[],[])
    i = 0
    while i < 10:
        datamap[key][0].append([])
        datamap[key][1].append([])
        datamap[key][2].append([])
        datamap[key][3].append([])
        i+=1

def open_file(name):
    # Use a breakpoint in the code line below to debug your script.
    file = open(fileDir + "/" + name, "r")
    for line in file:
        if line == "RUN\n":
            # Do what we need to do then break
            nextLine = file.readline() # ignore header
            # retrieve borders.
            splitLine = nextLine.split(",")
            borders = int(splitLine[4].removesuffix("b\n"))
            processes = int(splitLine[1].removesuffix("p"))
            width = int(splitLine[2].removesuffix("W"))
            headers.append(width)
            height = splitLine[3].removesuffix("H")
            nextLine = file.readline() # ignore first line
            s_gaps = []
            r_gaps = []
            c_gaps = []
            run_gaps = []
            i = 1
            while i < processes-1:
                nextLine = file.readline() # ignore first line.
                splitLine = nextLine.split(",")

                sndgap = float(splitLine[3])
                rcvgap = float(splitLine[4].removesuffix("\n"))
                cvgap = float(splitLine[2])
                run = float(splitLine[1])
                s_gaps.append(sndgap)
                r_gaps.append(rcvgap)
                c_gaps.append(cvgap)
                run_gaps.append(run)
                i+=1
            file.close()
            try:
                datamap[width]
            except KeyError:
                createMapIndex(width)
            #now we are sure that we can add.
            list = datamap[width]
            list[0][borders-1].append(np.median(s_gaps))
            list[1][borders-1].append(np.median(r_gaps))
            list[2][borders-1].append(np.median(c_gaps))
            list[3][borders-1].append(np.median(run_gaps))
            # snd = np.median(s_gaps[i]) * 6
            # rcv = np.median(r_gaps[i]) * 6
            # com = np.median(c_gaps[i]) / (i+1)
            return width, height


if __name__ == "__main__":

    stensil_pr_second = 100344885.21751237
    for file in os.listdir(fileDir):
        print(file)
        width, height = open_file(file)

        i=0
        # print("RUN," + width + "," + height)
        # while i < 10:
        #     communications = 2520/(i+1)
        #     snd_pr = snd / communications
        #     rcv_pr = rcv / communications
        #     tot = snd_pr + rcv_pr + com
        #     print("b" + str(i+1) + " " + str(snd_pr) + " " + str(rcv_pr) + " " + str(com) + " " + str(tot))
        #     i+=1
    f = open("outputGap50v.txt", "w")
    f.write("All data are per superstep\n#Border Thickness, Send Gap, Recv Gap, Com validation gap, total, runtime\n")
    f.close()
    for i in sorted(datamap.keys()):
        f = open("outputGap50v.txt", "a")
        # Write for each and numpy median each border for each width.
        list = datamap[i]
        j = 0
        f.write("DATA," + str(i) + "\n")
        while j < 10:
            sgap = np.median(list[0][j]) * 6 * (j+1)
            rgap = np.median(list[1][j]) * 6 * (j+1)
            cgap = np.median(list[2][j])

            # make them all so that they are for each superstep
            # they are currently for entire run.
            sgap = sgap / (ITER/(j+1))
            rgap = rgap / (ITER/(j+1))
            cgap = cgap / (ITER/(j+1))




            tot = sgap + rgap + cgap
            run = np.median(list[3][j])
            f.write("b" + str(j) + "," + str(sgap) + "," + str(rgap) + "," + str(cgap) + "," + str(tot) + "," + str(run)+"\n")

            j+=1


    # values = np.sort(values)
    # values.pop(0)
    # values.pop(len(values)-1)
    # median = np.median(values)
    # deviation = np.std(values)
    # print("Median:       " + str(median))
    # print("Median - std: "+ str(median-deviation))
    # print("Median + std: "+ str(median+ deviation))
    # print("std:           " + str(deviation))
