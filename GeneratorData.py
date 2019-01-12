from numpy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import Counter


def main():
    fileString = '/Users/sashacurcic/Documents/Sasha/MarkStuff/GeneratorData.txt'
    resistance = [x.split()[0] for x in open(fileString).readlines()]
    resistance = [float(i) for i in resistance]
    voltage = [x.split()[1] for x in open(fileString).readlines()]
    voltage = [float(i) for i in voltage]
    current = [x.split()[2] for x in open(fileString).readlines()]
    current = [float(i) for i in current]
    print resistance
    print voltage
    print current

    nDataPoints = Counter(resistance).values()
    resistanceValues = Counter(resistance).keys()
    nResistors = size(nDataPoints)
    print nResistors
    print
    for i in range(nResistors):
        for k in range(nResistors - i - 1):
            j = i + k + 1
            if(resistanceValues[i] > resistanceValues[j]):
                resistanceValues[i], resistanceValues[j] = resistanceValues[j], resistanceValues[i]
                nDataPoints[i], nDataPoints[j] = nDataPoints[j], nDataPoints[i]
    print
    print 'resistanceValues =', resistanceValues
    print 'nDataPoints =', nDataPoints
    listDimension = max(nDataPoints)
    print 'max =', listDimension
    voltageSets = [0 for x in range(nResistors)]
    percentSets = [0 for x in range(nResistors)]
    currentSets = [0 for x in range(nResistors)]
    upperIndex = 0
    for i in range(nResistors):
        lowerIndex = upperIndex
        upperIndex = upperIndex + nDataPoints[i]
        voltageSets[i] = [0 for x in range(nDataPoints[i])]
        percentSets[i] = [0 for x in range(nDataPoints[i])]
        currentSets[i] = [0 for x in range(nDataPoints[i])]
        if(lowerIndex == upperIndex - 1):
            voltageSets[i] = voltage[lowerIndex]
            currentSets[i] = current[lowerIndex]
            # percentSets[i] = percentError[lowerIndex]
        else:
            voltageSets[i] = voltage[lowerIndex:upperIndex]
            currentSets[i] = current[lowerIndex:upperIndex]
            # percentSets[i] = percentError[lowerIndex:upperIndex]
        theoreticalPowerSet = multiply(voltageSets[i], currentSets[i])
        actualPowerSet = multiply(voltageSets[i], voltageSets[i]) / resistanceValues[i]
        percentSets[i] = (100 * (theoreticalPowerSet - actualPowerSet)) / theoreticalPowerSet

    print 'voltageSets =', voltageSets
    print 'currentSets =', currentSets
    # percentError = [x.split() for x in percentSets]
    # print 'average =', percentError


    print 'RIGHT HERE:'
    print 5%3

    fig, ax = plt.subplots()
    for i in range(nResistors):
        k = i + 1
        if(k % 10 == 0):
            color = '#17becf'
        else:
            if(k % 9 == 0):
                color = '#bcbd22'
            else:
                if(k % 8 == 0):
                    color = '#7f7f7f'
                else:
                    if(k % 7 == 0):
                        color = '#e377c2'
                    else:
                        if(k % 6 == 0):
                            color = '#8c564b'
                        else:
                            if(k % 5 == 0):
                                color = '#9467bd'
                            else:
                                if(k % 4 == 0):
                                    color = '#d62728'
                                else:
                                    if(k % 3 == 0):
                                        color = '#2ca02c'
                                    else:
                                        if(k % 2 == 0):
                                            color = '#ff7f0e'
                                        else:
                                            color = '#1f77b4'
        if(nDataPoints[i] == 1):
            ax.scatter(voltageSets[i], percentSets[i], s = 3, color = color)
        else:
            ax.plot(voltageSets[i], percentSets[i], linewidth = 1.5, color = color)
        plt.title('Percent Error of Power Calculation with Increasing Voltage')
        plt.xlabel('Voltage')
        plt.ylabel('Percent Error')
        plt.grid(True)
        yticks = ticker.FormatStrFormatter('%.0f%%')
        ax.yaxis.set_major_formatter(yticks)
    plt.show()

main()