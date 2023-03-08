
import os
import numpy as np
fileDir ="swe_gap"

def open_file(name,s_gaps, r_gaps ):
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
            nextLine = file.readline() # ignore first line

            i = 1
            while i < processes:
                nextLine = file.readline() # ignore first line.
                splitLine = nextLine.split(",")

                sndgap = float(splitLine[3])
                rcvgap = float(splitLine[4].removesuffix("\n"))
                s_gaps[borders-1].append((sndgap))
                r_gaps[borders-1].append((rcvgap))
                i+=1
            file.close()
            return


if __name__ == "__main__":
    stensil_pr_second = 100344885.21751237
    s_gaps = []
    r_gaps = []
    i = 0
    while i < 10:
        s_gaps.append([])
        r_gaps.append([])
        i+=1
    for file in os.listdir(fileDir):
        open_file(file, s_gaps, r_gaps)

    print("Medians:\n b, send_gap, rcv_gap")
    i=0
    while i < 10:
        communications = 2520/(i+1)
        snd = np.median(s_gaps[i]) * 6
        rcv = np.median(r_gaps[i]) * 6
        snd_pr = snd / communications
        rcv_pr = rcv / communications
        tot = snd_pr + rcv_pr
        stensils = tot * stensil_pr_second
        print("b" + str(i+1) + " " + str(snd_pr) + " " + str(rcv_pr) + " " + str(tot) + " " + str(stensils))
        i+=1
    # values = np.sort(values)
    # values.pop(0)
    # values.pop(len(values)-1)
    # median = np.median(values)
    # deviation = np.std(values)
    # print("Median:       " + str(median))
    # print("Median - std: "+ str(median-deviation))
    # print("Median + std: "+ str(median+ deviation))
    # print("std:           " + str(deviation))
