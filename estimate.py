

# calculate for 1 superstep and multiply with the total number of iterations?

from prettytable import PrettyTable

# NOTE: WIDTH HEIGHT per PROCESSOR
# 83 W and 333 HEIGHT should be ok.
WIDTH = 50
HEIGHT = 166
h = {50, 100, 150, 166 ,200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000}
#h = {166}

ITERATIONS = 2520 # NEEDS TO be a LCM of all the border thicknesses
BANDWIDTH = 3000 # in megabytes per sec?
bytes_per_point = 8
point_multiplier = 3 # used to multiply by for example by 3 since we always are dealing with 3 grids.
stansils_send = 4000/3
borders = 10


def originalCalc():
    calculated_points = 0
    i = 0
    while i < ITERATIONS:
        calculated_points += (WIDTH) * (HEIGHT)
        i+=1
    return calculated_points * point_multiplier

def borderCalc(K):
    calculated_points = 0
    extra_points = 0
    extra_per_pr_super = 0
    i = 0
    calculated_points += WIDTH * HEIGHT * K
    i += K
    j = 1
    while j < K:
        # one extra row to calculate in top, and boto
        extra_points += WIDTH * (K - j) * 2
        j+=1
    extra_per_pr_super = extra_points
    total_super = ITERATIONS/K
    extra_points = extra_points * total_super
    return extra_points * point_multiplier, extra_per_pr_super * point_multiplier, total_super

def originalCom(calc):
    i = 0
    total_latency = 0
    total_com_time = 0
    # for each border exchange
    while i < ITERATIONS:
        # total_calc[i]
        # if i %
        # calculated_points += WIDTH * HEIGHT
        i+=1
    return

datamap = dict()
def readGaps():
    name = "outputGap.txt"
    file = open(name, "r")
    for line in file:
        s = line[0:4]
        if s == "DATA":
            splitpline = line.split(",")
            width = splitpline[1].removesuffix("\n")
            datamap[width] = ([],[],[],[],[])
            sendG = datamap[width][0]
            recG = datamap[width][1]
            cGap = datamap[width][2]
            total = datamap[width][3]
            run = datamap[width][4]
            i = 0
            while i < 10:
                nextline = file.readline()
                splitpline = nextline.split(",")
                sendG.append(float(splitpline[1]))
                recG.append(float(splitpline[2]))
                cGap.append(float(splitpline[3]))
                total.append(float(splitpline[4]))
                run.append(float(splitpline[5].removesuffix("\n")))
                i+=1


def createWriteTable(list):
    ogCalc = float(originalCalc())
    special = False
    info = PrettyTable(['Stencil calc speed / second', 'Grid Width', 'Grid Height', 'Stencils / point'])
    calcSpeed = 100344885.21751237
    calcSpeed = 90000000
    calcSpeed = 74064281
    base_runtime = ogCalc / calcSpeed
    info.add_row([calcSpeed, WIDTH, HEIGHT, 3])
    sgap = list[0]
    rgap = list[1]
    cgap = list[2]
    tgap = list[3]
    rntime = list[4]
    # print(info)
    gap_time = tgap[0] * float(ITERATIONS)
    ogRuntime = base_runtime + gap_time

    t = PrettyTable(['Border Thickness', 'Stencils', 'Extra Stencils / Sstep', 'Ssteps', 'S gap / Sstep', 'R gap / Sstep', "C gap / Sstep", "T gap / Sstep",
                     'Extra stencils  * Calc speed / Sstep','T gap * Supersteps', 'Runtime', '% increase',
                     '% more stencil points', "Physical runtime for 166h"])
    # tK = PrettyTable(['Border Thickness', 'Stencil Points', 'Extra Points / Sstep', 'Ssteps', 'Communications' 'Gap time each Sstep', 'Comm gap * Supersteps', 'Extra points  * Calc speed', 'Runtime', '% increase'])
    t.add_row(["1", ogCalc, None, float(ITERATIONS), sgap[0],rgap[0],cgap[0],tgap[0], None , gap_time, ogRuntime,
               None, round(float(0), 3), rntime[0]])

    i = 2
    percentages = []
    while i <= borders:

        total_extra, extra_pr_super, total_super = borderCalc(i)
        # add stencils + extra border stencils.
        total = total_extra + ogCalc
        # add number of superstaps with total gap for each Sstep.
        # calculate time to calculate extra stencils. * total supersteps.

        # Recheck that data comes is as per superstep for its border thickness.
        # make sure we times it against the correct to get total value.




        extra_points_over_calc_speed = ( total_extra / calcSpeed)
        gap_time = total_super * tgap[i-1]
        runtime = base_runtime + gap_time + extra_points_over_calc_speed
        perc = runtime / ogRuntime * 100
        percentages.append(perc)
        ratio = total_extra / ogCalc * 100
        t.add_row([str(i), total, extra_pr_super, total_super, sgap[i-1],rgap[i-1],cgap[i-1],tgap[i-1], extra_points_over_calc_speed, gap_time,
                   runtime, round(perc, 2), round(ratio, 3), rntime[i-1]])
        # tK.add_row(["b" + str(i), total, pr_super, total_super, gapList[i-1], comm_gap_times_superstep_cartesian, extra_points_over_calc_speed, runtime, round(perc,2)])
        # print("b" + str(i) + " " + str(total) +  " " + str(pr_super) + " " + str(total_super))
        i += 1
    if percentages[0] < 100 and percentages[1] < 100:
        special = True
    return info, t, special

if __name__ == "__main__":

    s = open("estimation/special.txt", "w")
    s.close()
    readGaps()
    for i in sorted(datamap.keys()):
        f = open("estimation/" + i + ".txt", "w")
        WIDTH = int(i)
        for he in sorted(h):
            HEIGHT = he
            info, t, special = createWriteTable(datamap[i])
            f.write(str(info))
            f.write(str(t) + "\n\n")
            if special:
                s = open("estimation/special.txt", "a")
                s.write(str(info))
                s.write(str(t))
                s.close()
            # if(i == "500"):
            # print(info)
            # print(t)
        # break


    # print(tK)

