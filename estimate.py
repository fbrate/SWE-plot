

# calculate for 1 superstep and multiply with the total number of iterations?


# NOTE: WIDTH HEIGHT per PROCESSOR
WIDTH = 100
HEIGHT = 100
ITERATIONS = 12 # NEEDS TO be a LCM of all the border thicknesses
BANDWIDTH = 3000 # in megabytes per sec?
bytes_per_point = 8
point_multiplier = 1 # used to multiply by for example by 3 since we always are dealing with 3 grids.
stansils_send = 4000/3
borders = 4


def originalCalc():
    calculated_points = 0
    i = 0
    while i < ITERATIONS:
        calculated_points += WIDTH * HEIGHT
        i+=1
    return calculated_points * point_multiplier

def borderCalc(K):
    calculated_points = 0
    extra_points = 0
    i = 0
    while i < ITERATIONS:
        calculated_points += WIDTH * HEIGHT * K
        i += K
        j = 1
        while j < K:
            # one extra row to calculate in top, and botom.
            extra_points += WIDTH * (K - j) * 2
            j+=1
    return (calculated_points + extra_points) * point_multiplier

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

if __name__ == "__main__":

    print("""###########################################################################
##                          CALCULATION COSTS                            ##
###########################################################################""")
    ogCalc = originalCalc();
    calc = []
    calc.append(ogCalc)
    print("Original points to calculate: " + str(calc[0]))
    i = 2
    while i <= borders:
        calc.append(borderCalc(i))
        i+=1
    i = 0;
    while i < borders:
        communications = int(ITERATIONS/(i+1))
        print("b" + str(i+1) + " " + str(calc[i]) + " " + str(calc[i]/ogCalc * 100) + "%" + " " + str(communications))
        i+=1

    originalCom(calc)
