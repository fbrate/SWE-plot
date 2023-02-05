

# NOTE: WIDTH HEIGHT per PROCESSOR
WIDTH = 100
HEIGHT = 100
ITERATIONS = 2520 # NEEDS TO be a LCM of all the border thicknesses
LATENCY = 1 # in seconds?
BANDWIDTH = 3000 # in megabytes per sec?
bytes_per_point = 8
point_multiplier = 1 # used to multiply by for example by 3 since we always are dealing with 3 grids.

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
            extra_points += WIDTH * (K - j) * 2
            j+=1
    return (calculated_points + extra_points) * point_multiplier

def originalCom(calc):
    i = 0
    total_latency = 0
    total_com_time = 0
    # for each border exchange
    while i < ITERATIONS:
        total_calc[i]
        if i %
        calculated_points += WIDTH * HEIGHT
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
    calc.append(borderCalc(2))
    calc.append(borderCalc(3))
    calc.append(borderCalc(4))
    calc.append(borderCalc(5))
    calc.append(borderCalc(6))
    calc.append(borderCalc(7))
    calc.append(borderCalc(8))
    calc.append(borderCalc(9))
    calc.append(borderCalc(10))
    i = 2;
    for x in calc:
        print("Points for border thicknes " + str(i) + ": " + str(x) + ". Percentage inc: " + str(x/ogCalc * 100) + "%")
        i+=1

    print("""\n###########################################################################
##                         COMMUNICATION COSTS                           ##
###########################################################################""")
    originalCom(calc)
