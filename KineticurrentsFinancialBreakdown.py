import numpy as numpy
from scipy import *
from numpy import *
import matplotlib
import sys as sys

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def main():
    lifespan = 30
    contractSpan = asarray([lifespan]) # Don't touch this if you want same answer as what we discussed.
    LCOEMin = 0.03
    discountRate = 0.03
    inflationRate = 0.04
    maintIncreaseRate = 0.01
    productionCost = 20000
    profitCost = 20000
    installationCost = 10000
    annualEnergy = 15 * 50 * 7 * 24
    maintMargin = 0.4

    if (type(lifespan) is not int):
        sys.exit('lifespan must be an integer!')
    if(lifespan <= 0):
        sys.exit('lifespan must be greater than 0!')

    if (((type(contractSpan) is not ndarray) and (type(contractSpan) is not numpy.ma.core.MaskedArray))):
        sys.exit('contractSpan must be an array!')

    if ((type(LCOEMin) is not float) and (type(LCOEMin) is not int)):
        sys.exit('LCOEMin must be a numerical value!')
    if(LCOEMin <= 0):
        sys.exit('LCOEMin must be greater than 0!')

    if ((type(discountRate) is not float) and (type(discountRate) is not int)):
        sys.exit('discountRate must be a numerical value!')
    if(discountRate < 0):
        sys.exit('discountRate must be greater than or equal to 0!')

    if ((type(inflationRate) is not float) and (type(inflationRate) is not int)):
        sys.exit('inflationRate must be a numerical value!')

    if (sum(contractSpan) != lifespan):
        sys.exit('contractSpan must yield integer number of periods in lifespan!')

    investment = productionCost + profitCost + installationCost
    maintMarginScalingFactor = 1 + maintMargin
    ratio = 1 + discountRate
    segments = shape(contractSpan)[0]
    increaseRate = inflationRate + maintIncreaseRate
    numer = (annualEnergy * LCOEMin * ratio * ((ratio ** lifespan) - 1)) - (investment * (ratio ** lifespan) * (ratio - 1)) # (ratio - exp(increaseRate)) * ((annualEnergy * LCOEMin * ratio * ((ratio ** lifespan) - 1)) - (investment * (ratio ** lifespan) * (ratio - 1)))
    denom = ratio * ((ratio ** lifespan) - 1) # ratio * (exp(increaseRate) - 1) * (ratio - 1) * ((ratio ** lifespan) - exp(lifespan * increaseRate))
    maintRateUtil = numer / denom

    if (maintRateUtil <= 0):
        sys.exit('The conditions you entered are not mathematically viable.')


    maintRateUtilArray = zeros(segments, float)
    contractTime = zeros(segments, float)
    for i in range(segments):
        if (i == 0):
            maintRateUtilArray[i] = maintRateUtil
        else:
            maintRateUtilArray[i] = maintRateUtilArray[i - 1] * exp(inflationRate * contractSpan[i - 1])
        contractTime[i] = sum(contractSpan[0:i + 1])
    price = (increaseRate * maintRateUtil * lifespan) / (maintMarginScalingFactor * (exp(increaseRate * lifespan) - 1))

    scalingString = asarray(round(maintRateUtil, 2), str)
    timePoints = linspace(1, lifespan, num = lifespan)
    timeSpace = linspace(0, lifespan, num = (10 * lifespan) + 1)
    maintArray = ones(lifespan, float)
    maintArrayLarge = ones((10 *lifespan) + 1, float)
    intercept = ones((10 * lifespan) + 1, float)
    oldIndex = 0
    oldSpot = 0
    newIntercept = 0
    oldIntercept = 0
    for i in range(segments):
        index = asscalar(where(timePoints == contractTime[i])[0])
        spot = asscalar(where(timeSpace == contractTime[i])[0])
        maintArray[oldIndex:index + 1] =  asscalar(maintRateUtilArray[i]) * maintArray[oldIndex:index + 1]
        maintArrayLarge[oldSpot:spot + 1] = asscalar(maintRateUtilArray[i]) * maintArrayLarge[oldSpot:spot + 1]
        if (i == 0):
            intercept[oldSpot:spot + 1] = 0 * intercept[oldSpot:spot + 1] + newIntercept
        else:
            newIntercept = (contractTime[i - 1] * (maintRateUtilArray[i - 1] - maintRateUtilArray[i])) + oldIntercept
            intercept[oldSpot:spot + 1] = newIntercept * intercept[oldSpot:spot + 1]
            oldIntercept = newIntercept
        oldIndex = index + 1
        oldSpot = spot + 1
    annualMaintUs = (price / increaseRate) * (1 - exp(-increaseRate)) * exp(increaseRate * timePoints)
    annualMaintUtil = maintArray * ones(lifespan, dtype)
    if (annualMaintUs[lifespan - 1] >= annualMaintUtil[lifespan - 1]):
        annualMaintUpperLim = 1.05 * annualMaintUs[lifespan - 1]
    else:
        annualMaintUpperLim = 1.05 * annualMaintUtil[lifespan - 1]
    maintExpUs = (price / increaseRate) * (exp(increaseRate * timeSpace) - 1)

    LCOENumerUtil = annualMaintUtil / (ratio ** timePoints)
    LCOENumerUtil[0] = LCOENumerUtil[0] + (investment / ratio)
    LCOEDenomUtil = annualEnergy / (ratio ** timePoints)
    LCOETimeUtil = zeros(lifespan, float)

    # I'm pretty confused about how to calculate our LCOE. We and utilities can't both get the subsidy rate. So I
    # omitted it from
    LCOENumerUs = 1 * annualMaintUs # If I don't include that 1, Python reads the = as ser rather than estar
    LCOENumerUs[0] = LCOENumerUs[0] + productionCost
    LCOEDenomUs = annualEnergy * ones(lifespan, float)
    LCOETimeUs = zeros(lifespan, float)
    for i in range(lifespan):
        if (i == 0):
            LCOETimeUtil[i] = LCOENumerUtil[i] / LCOEDenomUtil[i]
            LCOETimeUs[i] = LCOENumerUs[i] / LCOEDenomUs[i]
        else:
            LCOETimeUtil[i] = sum(LCOENumerUtil[0:i + 1]) / sum(LCOEDenomUtil[0:i + 1])
            LCOETimeUs[i] = sum(LCOENumerUs[0:i + 1]) / sum(LCOEDenomUs[0:i + 1])

    LCOEUpperLim = 1.05 * LCOETimeUtil[0]
    maintExpUtil = (maintArrayLarge * timeSpace) + intercept
    maintExpUpperLim = 1.1 * maintExpUtil[10 * lifespan]
    newMaintProfit = (maintExpUtil[10 * lifespan] - maintExpUs[10 * lifespan]) / maintExpUs[10 * lifespan]
    totalProfit = (newMaintProfit * maintExpUs[10 * lifespan]) + profitCost
    print 'Our Total Maintenance Costs (These values should match.): $%f, $%f' % (round(sum(annualMaintUs), 2), round(maintExpUs[10 * lifespan], 2))
    print 'Utilities\' Total Maintenance Costs (These values should match.): $%f, $%f' % (round(sum(annualMaintUtil), 2), round(maintExpUtil[10 * lifespan], 2))
    print 'New Profit Margin on Maintenance: %f' % (100 * newMaintProfit)
    print 'Total Profit: $%f' % round(totalProfit, 2)
    print LCOETimeUtil[lifespan - 1]

    plt.figure('AnnualMaintenanceCost')
    plt.bar(timePoints, annualMaintUtil, zorder = 2, color = colorDefault(2), alpha = 0.95)
    plt.bar(timePoints, annualMaintUs, zorder = 3, color = colorDefault(0), alpha = 0.65)
    plt.text(lifespan / 6, 0.8 * annualMaintUpperLim, r'$M_{t} = \$%s [e^{0.05 t} - e^{0.05 (t - 1)}]$' % scalingString)
    plt.grid(True, which = 'both', zorder = 1)
    plt.title('Annual Maintenance Cost')
    plt.xlabel('Time [yr]')
    plt.ylabel('Cost [$]')
    plt.xlim(0, lifespan + 1)
    plt.ylim(0, annualMaintUpperLim)
    plt.figure('MaintenanceExpenditureByYear')
    plt.plot(timeSpace, maintExpUtil, color = colorDefault(2), zorder = 2)
    plt.plot(timeSpace, maintExpUs, color = colorDefault(0), zorder = 3)
    plt.scatter(timeSpace[10 * lifespan], maintExpUtil[10 * lifespan], color = colorDefault(1), zorder = 3, s = 25)
    plt.scatter(timeSpace[10 * lifespan], maintExpUs[10 * lifespan], color = colorDefault(3), zorder = 4, s = 25)
    plt.text(lifespan / 6, 0.66 * maintExpUpperLim, r'$T(t) = \$%s (e^{0.05 t} - 1)$' % scalingString)
    proportion = (((0.94 * maintExpUpperLim) - maintExpUtil[10 * lifespan]) + maintExpUs[10 * lifespan]) / maintExpUpperLim
    if (proportion > 0.79):
        proportion = ((maintExpUs[10 * lifespan] - ((0.94 * maintExpUpperLim) - maintExpUtil[10 * lifespan])) / maintExpUpperLim) - 0.01
    line1 = 0.94 * maintExpUpperLim
    line2 = 0.89 * maintExpUpperLim
    line3 = 0.84 * maintExpUpperLim
    line4 = proportion * maintExpUpperLim
    line5 = (proportion - 0.05) * maintExpUpperLim
    plt.text(0.75 * lifespan, line1, 'Total Maintenance')
    plt.text(0.75 * lifespan, line2, 'Budget for')
    plt.text(0.75 * lifespan, line3, 'Utilities')
    plt.text(0.75 * lifespan, line4, 'Total Maintenance')
    plt.text(0.75 * lifespan, line5, 'Budget for Us')
    plt.grid(True, which = 'both', zorder = 1)
    plt.title('Maintenance Expenditure by Year')
    plt.xlabel('Time [yr]')
    plt.ylabel('Expenditure [$]')
    plt.xlim(0, 1.03 * lifespan)
    plt.ylim(0, maintExpUpperLim)
    plt.figure('LCOEByYear')
    plt.plot(timePoints, LCOETimeUtil, color = colorDefault(2), zorder = 1)
    plt.plot(timePoints, LCOETimeUs, color = colorDefault(0), zorder = 2)
    plt.grid(True, which = 'both', zorder = 1)
    plt.title('LCOE by Year')
    plt.xlabel('Time [yr]')
    plt.ylabel(r'$\mathrm{LCOE} \: \: [\$/\mathrm{kW} \bullet \mathrm{hr}]$')
    plt.xlim(0, lifespan + 1)
    plt.ylim(0, LCOEUpperLim)
    plt.show()


def colorDefault(k):
    if (k == 0):
        color = '#1f77b4'  # blue
    else:
        if (k % 9 == 0):
            color = '#17becf'  # cyan
        else:
            if (k % 8 == 0):
                color = '#bcbd22'  # sickly greenish tan
            else:
                if (k % 7 == 0):
                    color = '#7f7f7f'  # grey
                else:
                    if (k % 6 == 0):
                        color = '#e377c2'  # pink
                    else:
                        if (k % 5 == 0):
                            color = '#8c564b'  # brown
                        else:
                            if (k % 4 == 0):
                                color = '#9467bd'  # purple
                            else:
                                if (k % 3 == 0):
                                    color = '#d62728'  # red
                                else:
                                    if (k % 2 == 0):
                                        color = '#2ca02c'  # green
                                    else:
                                        color = '#ff7f0e'  # orange
    return color

main()
