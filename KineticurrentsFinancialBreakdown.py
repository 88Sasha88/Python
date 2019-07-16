import numpy as numpy
from scipy import *
from numpy import *
import matplotlib
import sys as sys

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

runDiagnostic = 'No'
damageRateOverride = 'No'
defaultDamageRate = 0.01

def main():
    LCOE = 0.06
    discountRate = 0.03
    energykW = 15
    numberOfUnits = 1
    lifespan = 30
    contractSpan = 5
    inflationRate = 0.04
    productionCost = 20000
    profitCost = 20000
    baseInstalCost = 8000
    unitInstalCost = 2000
    daysActive = 50 * 7
    maintMargin = 0.4
    
    if ((type(LCOE) is not float) and (type(LCOE) is not int)):
        sys.exit('LCOE must be a numerical value!')
    if(LCOE <= 0):
        sys.exit('LCOE must be greater than 0!')

    if ((type(discountRate) is not float) and (type(discountRate) is not int)):
        sys.exit('discountRate must be a numerical value!')
    if(discountRate <= 0):
        sys.exit('discountRate must be greater than 0!')
    
    if ((type(energykW) is not float) and (type(energykW) is not int)):
        sys.exit('discountRate must be a numerical value!')
    if(energykW <= 0):
        sys.exit('energykW must be greater than 0!')
    
    if (type(numberOfUnits) is not int):
        sys.exit('numberOfUnits must be an integer!')
    if(numberOfUnits <= 0):
        sys.exit('numberOfUnits must be greater than 0!')

    if (type(lifespan) is not int):
        sys.exit('lifespan must be an integer!')
    if(lifespan <= 0):
        sys.exit('lifespan must be greater than 0!')

    if (type(contractSpan) is not int):
        sys.exit('contractSpan must be an integer!')
    if ((lifespan % contractSpan) != 0):
        sys.exit('contractSpan must be a factor of lifespan!')

    if ((type(inflationRate) is not float) and (type(inflationRate) is not int)):
        sys.exit('inflationRate must be a numerical value!')
    
    if ((type(productionCost) is not float) and (type(productionCost) is not int)):
        sys.exit('productionCost must be a numerical value!')
    if(productionCost < 0):
        sys.exit('produtionCost must be greater than or equal to 0!')
    
    if ((type(profitCost) is not float) and (type(profitCost) is not int)):
        sys.exit('profitCost must be a numerical value!')
    if(profitCost < 0):
        sys.exit('profitCost must be greater than or equal to 0!')
        
    if ((type(baseInstalCost) is not float) and (type(baseInstalCost) is not int)):
        sys.exit('baseInstalCost must be a numerical value!')
    if(baseInstalCost < 0):
        sys.exit('baseInstalCost must be greater than or equal to 0!')
    
    if ((type(unitInstalCost) is not float) and (type(unitInstalCost) is not int)):
        sys.exit('unitInstalCost must be a numerical value!')
    if(unitInstalCost < 0):
        sys.exit('unitInstalCost must be greater than or equal to 0!')
    
    if ((type(daysActive) is not float) and (type(daysActive) is not int)):
        sys.exit('daysActive must be a numerical value!')
    if(daysActive <= 0):
        sys.exit('daysActive must be greater than 0!')

    if ((type(maintMargin) is not float) and (type(maintMargin) is not int)):
        sys.exit('maintMargin must be a numerical value!')
    if(maintMargin < 0):
        sys.exit('maintMargin must be greater than or equal to 0!')

    diagnostic = runDiagnostic.lower()
    damageOverride = damageRateOverride.lower()
    percentString = '%'
    annualEnergy = numberOfUnits * energykW * daysActive * 24
    instalCost = (unitInstalCost * numberOfUnits) + baseInstalCost
    investment = productionCost + profitCost + instalCost
    maintMarginScalingFactor = 1 + maintMargin
    segments = lifespan / contractSpan
    ratio = 1 + discountRate

    numer = ((ratio ** contractSpan) - exp(contractSpan * inflationRate)) * ((annualEnergy * LCOE * ratio * ((ratio ** lifespan) - 1)) - (investment * (ratio ** lifespan) * (ratio - 1)))
    denom = ratio * ((ratio ** contractSpan) - 1) * ((ratio ** lifespan) - exp(lifespan * inflationRate))
    maintNaughtUtil = numer / denom
    initialMaintString = asarray(round(maintNaughtUtil, 2), str)
    if (diagnostic == 'yes'):
        print 'Initial Maintenance Cost to Utilities: $%s' % initialMaintString
    if (maintNaughtUtil <= 0):
        sys.exit('The conditions you entered allow for less than no maintenance over time.')


    maintRateUtilArray = zeros(segments, float)
    for i in range(segments):
        if (i == 0):
            maintRateUtilArray[i] = maintNaughtUtil
        else:
            maintRateUtilArray[i] = maintRateUtilArray[i - 1] * exp(inflationRate * contractSpan)
    contractTime = contractSpan * linspace(1, segments, num = segments)
    if (diagnostic == 'yes'):
        print 'Times of Contract Expiration:'
        print contractTime

    checkPoints = 100000
    lowerCheckPoint = exp(inflationRate)
    upperCheckPoint = exp(inflationRate + 1)
    for i in range(4):
        damageRange = linspace(lowerCheckPoint, upperCheckPoint, num = checkPoints + 1)
        topPart = maintMarginScalingFactor * exp(inflationRate * lifespan) * (1 - exp(inflationRate * contractSpan)) * ((damageRange ** lifespan) - 1) * damageRange
        bottomPart = contractSpan * exp(inflationRate * contractSpan) * (1 - exp(inflationRate * lifespan)) * (damageRange - 1)
        xN1 = topPart / bottomPart
        xN2 = (damageRange ** lifespan)
        difference = abs(xN1 - xN2)
        smallest = min(difference[0:checkPoints + 1])
        smallestPlace = where(difference == smallest)[0][0]
        correctValue = damageRange[smallestPlace]
        if (diagnostic == 'yes'):
            print
            print 'Iteration:', i
            print 'Lowest Value:', correctValue, smallest, 'location:', smallestPlace
            print 'Range:', damageRange[0], 'to', damageRange[checkPoints]
            print 'Working Value:', log(correctValue) - inflationRate
        if (smallestPlace == 0):
            lowerCheckPoint = damageRange[smallestPlace]
            if (diagnostic == 'yes'):
                print 'Place 1:', smallestPlace
        else:
            lowerCheckPoint = damageRange[smallestPlace - 1]
            if (diagnostic == 'yes'):
                print 'Place 1:', smallestPlace - 1
        if (smallestPlace == checkPoints):
            upperCheckPoint = damageRange[smallestPlace]
            if (diagnostic == 'yes'):
                print 'Place 2:', smallestPlace
        else:
            upperCheckPoint = damageRange[smallestPlace + 1]
            if (diagnostic == 'yes'):
                print 'Place 2:', smallestPlace + 1
    print
    damageRate = log(correctValue) - inflationRate
    if (diagnostic == 'yes'):
        print 'Damage Rate Before Default Override/Precaution: %s%s' % (asarray(100 * damageRate, str), percentString)
    if ((damageRate < (10 ** -12)) and (damageOverride != 'yes')):
        damageRate = defaultDamageRate
        damageString = asarray(100 * damageRate, str)
        print
        print 'WARNING: The parameters you set entail that you will be losing money during the last few years of your'
        print 'final contracting period. While your total profit margin will remain the same as what you set, there'
        print 'will be a period during which the cost of servicing overtakes the amount Utilities is paying for'
        print 'for maintenance. Because of this, the program was unable to solve for a \"budgeted\" rate of damage which'
        print 'would prevent this from happening, and so a default value of %s%s has been set for your damage rate.' % (damageString, percentString)
        print
    if (damageOverride == 'yes'):
        damageRate = defaultDamageRate
    damageString = asarray(100 * damageRate, str)
    print 'Damage Rate: %s%s' % (damageString, percentString)
    increaseRate = inflationRate + damageRate

    price = (maintNaughtUtil * contractSpan * increaseRate * (1 - exp(lifespan * inflationRate))) / (maintMarginScalingFactor * (1 - exp(contractSpan * inflationRate)) * (exp(increaseRate * lifespan) - 1))
    priceString = asarray(round(price, 2), str)
    print 'Price: $%s' % priceString

    timePoints = linspace(1, lifespan, num = lifespan)
    timeSpace = linspace(0, lifespan, num = (10 * lifespan) + 1)
    maintArrayLarge = ones((10 *lifespan) + 1, float)
    intercept = ones((10 * lifespan) + 1, float)
    oldSpot = 0
    newIntercept = 0
    oldIntercept = 0
    for i in range(segments):
        spot = asscalar(where(timeSpace == contractTime[i])[0])
        maintArrayLarge[oldSpot:spot + 1] = asscalar(maintRateUtilArray[i]) * maintArrayLarge[oldSpot:spot + 1]
        if (i == 0):
            intercept[oldSpot:spot + 1] = 0 * intercept[oldSpot:spot + 1] + newIntercept
        else:
            newIntercept = (contractTime[i - 1] * (maintRateUtilArray[i - 1] - maintRateUtilArray[i])) + oldIntercept
            intercept[oldSpot:spot + 1] = newIntercept * intercept[oldSpot:spot + 1]
            oldIntercept = newIntercept
        oldSpot = spot + 1
    annualMaintUs = (price / increaseRate) * (1 - exp(-increaseRate)) * exp(increaseRate * timePoints)
    annualMaintUtil = maintNaughtUtil * exp(contractSpan * inflationRate * floor((timePoints - 1) / contractSpan))
    if (annualMaintUs[lifespan - 1] >= annualMaintUtil[lifespan - 1]):
        annualMaintUpperLim = 1.05 * annualMaintUs[lifespan - 1]
    else:
        annualMaintUpperLim = 1.05 * annualMaintUtil[lifespan - 1]
    maintExpUs = (price / increaseRate) * (exp(increaseRate * timeSpace) - 1)


    LCOENumer = annualMaintUtil / (ratio ** timePoints)
    LCOENumer[0] = LCOENumer[0] + (investment / ratio)
    LCOEDenom = annualEnergy / (ratio ** timePoints)
    LCOETime = zeros(lifespan, float)

    for i in range(lifespan):
        if (i == 0):
            LCOETime[i] = LCOENumer[i] / LCOEDenom[i]
        else:
            LCOETime[i] = sum(LCOENumer[0:i + 1]) / sum(LCOEDenom[0:i + 1])

    LCOEUpperLim = 1.05 * LCOETime[0]
    maintExpUtil = (maintArrayLarge * timeSpace) + intercept
    maintExpUpperLim = 1.1 * maintExpUtil[10 * lifespan]
    newMaintProfit = (maintExpUtil[10 * lifespan] - maintExpUs[10 * lifespan]) / maintExpUs[10 * lifespan]
    totalProfit = (newMaintProfit * maintExpUs[10 * lifespan]) + profitCost
    maintBudgUsString1 = asarray(round(maintExpUs[10 * lifespan], 2), str)
    maintBudgUsString2 = asarray(round(sum(annualMaintUs), 2), str)
    maintBudgUtilString1 = asarray(round(maintExpUtil[10 * lifespan], 2), str)
    maintBudgUtilString2 = asarray(round(sum(annualMaintUtil), 2), str)
    marginString1 = asarray(100 * maintMargin, str)
    marginString2  = asarray(100 * newMaintProfit, str)
    finalYearUs = asarray(annualMaintUs[lifespan - 1])
    finalYearUtil = asarray(annualMaintUtil[lifespan - 1], str)
    profitString = asarray(round(totalProfit, 2), str)
    if (diagnostic == 'yes'):
        print 'Final Year Respective Maintenance Costs for Us and Utilities (If damage rate precaution/override not triggered, then these values should match.): $%s, $%s' % (finalYearUs, finalYearUtil)
        print 'Our Total Maintenance Costs (These values should match.): $%s, $%s' % (maintBudgUsString1, maintBudgUsString2)
        print 'Utilities\' Total Maintenance Costs (These values should match.): $%s, $%s' % (maintBudgUtilString1, maintBudgUtilString2)
        print 'Profit Margin on Maintenance (These values should match.): %s%s, %s%s' % (marginString1, percentString, marginString2, percentString)
        print 'LCOE (These values should match.): $%f, $%f' % (LCOE, LCOETime[lifespan - 1])
    else:
        print 'Our Total Maintenance Costs: $%s' % maintBudgUsString1
        print 'Utilities\' Total Maintenance Costs: $%s' % maintBudgUtilString1
    print 'Total Profit: $%s' % profitString


    plt.figure('AnnualMaintenanceCost')
    plt.bar(timePoints, annualMaintUtil, zorder = 2, color = colorDefault(2), alpha = 0.95)
    plt.bar(timePoints, annualMaintUs, zorder = 3, color = colorDefault(0), alpha = 0.65)
    # plt.text(lifespan / 8, 0.8 * annualMaintUpperLim, r'$M_{t} = \$%s [e^{0.05 t} - e^{0.05 (t - 1)}]$' % initialMaintString)
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
    # plt.text(lifespan / 6, 0.66 * maintExpUpperLim, r'$T(t) = \$%s (e^{0.05 t} - 1)$' % initialMaintString)
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
    plt.plot(timePoints, LCOETime, color = colorDefault(2), zorder = 2)
    plt.grid(True, which = 'both', zorder = 1)
    plt.title('LCOE by Year')
    plt.xlabel('Time [yr]')
    plt.ylabel(r'$\mathrm{LCOE} \: \: [\$/\mathrm{kW} \bullet \mathrm{hr}]$')
    plt.xlim(0, lifespan + 1)
    plt.ylim(0, LCOEUpperLim)
    if (diagnostic == 'yes'):
        plt.figure()
        # plt.plot(damageRange, xN1)
        # plt.plot(damageRange, xN2)
        plt.plot(damageRange, difference)
        plt.xlim(damageRange[0], damageRange[checkPoints])
        plt.title(r'$\mathrm{Optimization} \: \: \mathrm{of} \: \: e^{R}$')
        plt.ylabel(r'$|\frac{a}{b} - e^{NR}|$')
        plt.xlabel(r'$e^{R}$')
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
