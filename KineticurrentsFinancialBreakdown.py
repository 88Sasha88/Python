import numpy as numpy
from scipy import *
from numpy import *
import matplotlib
import sys as sys

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

runDiagnostic = 'No'
damageRateOverride = 'No'

def main():
    LCOE = 0.03
    discountRate = 0.03
    efficiencyLossRate = 0.01
    defaultDamageRate = 0.01
    inflationRate = 0.04
    lifespan = 30
    contractSpan = 3
    daysActive = 50 * 7
    numberOfUnits = 1
    productionCost = 20000
    baseInstalCost = 8000
    unitInstalCost = 2000
    power = 30
    saleMargin = 0.5
    maintMargin = 0.4
    
    if ((type(LCOE) is not float) and (type(LCOE) is not int)):
        sys.exit('LCOE must be a numerical value!')
    if(LCOE <= 0):
        sys.exit('LCOE must be greater than 0!')

    if ((type(discountRate) is not float) and (type(discountRate) is not int)):
        sys.exit('discountRate must be a numerical value!')
    if(discountRate <= 0):
        sys.exit('discountRate must be greater than 0!')

    if ((type(efficiencyLossRate) is not float) and (type(efficiencyLossRate) is not int)):
        sys.exit('efficiencyLossRate must be a numerical value!')
    if(discountRate <= 0):
        sys.exit('efficiencyLossRate must be greater than 0!')

    if ((type(inflationRate) is not float) and (type(inflationRate) is not int)):
        sys.exit('inflationRate must be a numerical value!')

    if ((type(defaultDamageRate) is not float) and (type(defaultDamageRate) is not int)):
        sys.exit('defaultDamageRate must be a numerical value!')
    if(defaultDamageRate <= 0):
        sys.exit('defaultDamageRate must be greater than 0!')

    if (type(lifespan) is not int):
        sys.exit('lifespan must be an integer!')
    if(lifespan <= 0):
        sys.exit('lifespan must be greater than 0!')

    if (type(contractSpan) is not int):
        sys.exit('contractSpan must be an integer!')
    if ((lifespan % contractSpan) != 0):
        sys.exit('contractSpan must be a factor of lifespan!')

    if ((type(daysActive) is not float) and (type(daysActive) is not int)):
        sys.exit('daysActive must be a numerical value!')
    if(daysActive <= 0):
        sys.exit('daysActive must be greater than 0!')

    if (type(numberOfUnits) is not int):
        sys.exit('numberOfUnits must be an integer!')
    if(numberOfUnits <= 0):
        sys.exit('numberOfUnits must be greater than 0!')

    if ((type(productionCost) is not float) and (type(productionCost) is not int)):
        sys.exit('productionCost must be a numerical value!')
    if(productionCost < 0):
        sys.exit('produtionCost must be greater than or equal to 0!')

    if ((type(baseInstalCost) is not float) and (type(baseInstalCost) is not int)):
        sys.exit('baseInstalCost must be a numerical value!')
    if (baseInstalCost < 0):
        sys.exit('baseInstalCost must be greater than or equal to 0!')

    if ((type(unitInstalCost) is not float) and (type(unitInstalCost) is not int)):
        sys.exit('unitInstalCost must be a numerical value!')
    if (unitInstalCost < 0):
        sys.exit('unitInstalCost must be greater than or equal to 0!')
    
    if ((type(power) is not float) and (type(power) is not int)):
        sys.exit('power must be a numerical value!')
    if(power <= 0):
        sys.exit('power must be greater than 0!')

    if ((type(saleMargin) is not float) and (type(saleMargin) is not int)):
        sys.exit('saleMargin must be a numerical value!')
    if(maintMargin < 0):
        sys.exit('saleMargin must be greater than or equal to 0!')

    if ((type(maintMargin) is not float) and (type(maintMargin) is not int)):
        sys.exit('maintMargin must be a numerical value!')
    if(maintMargin < 0):
        sys.exit('maintMargin must be greater than or equal to 0!')

    diagnostic = runDiagnostic.lower()
    damageOverride = damageRateOverride.lower()
    percentString = '%'
    annualEnergy = numberOfUnits * power * daysActive * 24
    instalCost = (unitInstalCost * numberOfUnits) + baseInstalCost
    saleMarginScalingFactor = 1 / (1 - saleMargin)
    saleCost = saleMarginScalingFactor * productionCost * numberOfUnits
    investment = productionCost + saleCost + instalCost
    maintMarginScalingFactor = 1 / (1 - maintMargin)
    segments = lifespan / contractSpan
    ratio = 1 + discountRate

    numer = (ratio - 1) * ((ratio ** contractSpan) - exp(inflationRate * contractSpan)) * ((annualEnergy * LCOE * ratio * (((ratio ** lifespan) * exp(efficiencyLossRate * lifespan)) - 1)) - (investment * (ratio ** lifespan) * exp(efficiencyLossRate * lifespan) * ((ratio * exp(efficiencyLossRate)) - 1)))
    denom = ratio * exp(efficiencyLossRate * lifespan) * ((ratio * exp(efficiencyLossRate)) - 1) * ((ratio ** contractSpan) - 1) * ((ratio ** lifespan) - exp(inflationRate * lifespan))

    maintNaughtUtil = numer / denom
    initialMaintString = asarray(round(maintNaughtUtil, 2), str)
    if (diagnostic == 'yes'):
        print 'Initial Maintenance Cost to Utilities: $%s' % initialMaintString
    if (maintNaughtUtil <= 0):
        sys.exit('The conditions you entered allow for less than no maintenance over time.')

    checkPoints = 100000
    lowerCheckPoint = exp(inflationRate)
    upperCheckPoint = exp(inflationRate + 1)
    for i in range(4):
        damageRange = linspace(lowerCheckPoint, upperCheckPoint, num = checkPoints + 1)
        xN = (damageRange ** lifespan)
        topPart = maintMarginScalingFactor * damageRange * exp(inflationRate * lifespan) * (1 - exp(inflationRate * contractSpan)) * (xN - 1)
        bottomPart = contractSpan * exp(inflationRate * contractSpan) * (1 - exp(inflationRate * lifespan)) * (damageRange - 1)
        frac = topPart / bottomPart
        difference = abs(frac - xN)
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

    price = (maintNaughtUtil * contractSpan * (inflationRate + damageRate) * (1 - exp(lifespan * inflationRate))) / (maintMarginScalingFactor * (1 - exp(contractSpan * inflationRate)) * (exp((inflationRate + damageRate) * lifespan) - 1))
    if (diagnostic == 'yes'):
        priceString = asarray(round(price, 2), str)
        print 'Price: $%s' % priceString

    timePoints = linspace(1, lifespan, num = lifespan)
    timeSpace = linspace(0, lifespan, num = (12 * lifespan) + 1)

    # Annual Maintenance Graph Calculations
    annualMaintKC = (price / (inflationRate + damageRate)) * (1 - exp(-(inflationRate + damageRate))) * exp((inflationRate + damageRate) * timePoints)
    annualMaintUtil = MaintFuncUtil(maintNaughtUtil, inflationRate, contractSpan, timePoints)
    if (annualMaintKC[lifespan - 1] >= annualMaintUtil[lifespan - 1]):
        annualMaintUpperLim = 1.05 * annualMaintKC[lifespan - 1]
    else:
        annualMaintUpperLim = 1.05 * annualMaintUtil[lifespan - 1]

    # Total Maintenance Expenditure Graph Calculations
    maintExpKC = (price / (inflationRate + damageRate)) * (exp((inflationRate + damageRate) * timeSpace) - 1)
    j = asarray([ceil(x / contractSpan) for x in timeSpace])
    intercept = maintNaughtUtil * contractSpan * (((1 - exp((j - 1) * inflationRate * contractSpan)) / (1 - exp(inflationRate * contractSpan))) - ((j - 1) * exp((j - 1) * inflationRate * contractSpan))) # ((1 - (exp(j * inflationRate * contractSpan) * (1 + j - (j * exp(inflationRate * contractSpan))))) / (1 - exp(inflationRate * contractSpan)))
    maintExpUtil = (MaintFuncUtil(maintNaughtUtil, inflationRate, contractSpan, ceil(timeSpace)) * timeSpace) + intercept
    maintExpUpperLim = 1.1 * maintExpUtil[12 * lifespan]

    # LCOE Graph Calculations
    LCOENumer = annualMaintUtil / (ratio ** timePoints)
    LCOENumer[0] = LCOENumer[0] + (investment / ratio)
    LCOEDenom = annualEnergy / ((ratio * exp(efficiencyLossRate)) ** timePoints)
    LCOETime = zeros(lifespan, float)

    for i in range(lifespan):
        if (i == 0):
            LCOETime[i] = LCOENumer[i] / LCOEDenom[i]
        else:
            LCOETime[i] = sum(LCOENumer[0:i + 1]) / sum(LCOEDenom[0:i + 1])
    LCOEUpperLim = 1.05 * LCOETime[0]

    saleProfit = saleMargin * saleCost
    newMaintProfitMargin = (maintExpUtil[12 * lifespan] - maintExpKC[12 * lifespan]) / maintExpUtil[12 * lifespan]
    maintProfit = maintMargin * maintExpUtil[12 * lifespan]
    totalProfit = maintProfit + saleProfit
    maintBudgKCString1 = asarray(round(maintExpKC[12 * lifespan], 2), str)
    maintBudgKCString2 = asarray(round(sum(annualMaintKC), 2), str)
    maintBudgKCString3 = asarray(round((price / (inflationRate + damageRate)) * (exp((inflationRate + damageRate) * lifespan) - 1), 2), str)
    maintBudgUtilString1 = asarray(round(maintExpUtil[12 * lifespan], 2), str)
    maintBudgUtilString2 = asarray(round(sum(annualMaintUtil), 2), str)
    maintBudgUtilString3 = asarray(round((maintNaughtUtil * contractSpan * (1 - exp(inflationRate * lifespan))) / (1 - exp(inflationRate * contractSpan)), 2), str)
    marginString1 = asarray(100 * maintMargin, str)
    marginString2  = asarray(100 * newMaintProfitMargin, str)
    finalYearKC = asarray(annualMaintKC[lifespan - 1])
    finalYearUtil = asarray(annualMaintUtil[lifespan - 1], str)
    saleProfitString = asarray(round(saleProfit, 2), str)
    maintProfitString = asarray(round(maintProfit, 2), str)
    totalProfitString = asarray(round(totalProfit, 2), str)
    if (diagnostic == 'yes'):
        print 'Final Year Respective Maintenance Costs for KC and Utilities (If the damage rate precaution/override is not triggered, then these values should match.): $%s, $%s' % (finalYearKC, finalYearUtil)
        print 'Our Total Maintenance Costs (These values should match.): $%s, $%s, $%s' % (maintBudgKCString1, maintBudgKCString2, maintBudgKCString3)
        print 'Utilities\' Total Maintenance Costs (These values should match.): $%s, $%s, $%s' % (maintBudgUtilString1, maintBudgUtilString2, maintBudgUtilString3)
        print 'Profit Margin on Maintenance (These values should match.): %s%s, %s%s' % (marginString1, percentString, marginString2, percentString)
        print 'LCOE (These values should match.): $%f, $%f' % (LCOE, LCOETime[lifespan - 1])
    else:
        print 'Our Total Maintenance Costs: $%s' % maintBudgKCString1
        print 'Utilities\' Total Maintenance Costs: $%s' % maintBudgUtilString1
    print 'Sale Profit: $%s' % saleProfitString
    print 'Maintenance Profit: $%s' % maintProfitString
    print 'Overall Profit: $%s' % totalProfitString


    plt.figure('AnnualMaintenanceCost')
    plt.bar(timePoints, annualMaintUtil, zorder = 2, color = colorDefault(2), alpha = 0.95)
    plt.bar(timePoints, annualMaintKC, zorder = 3, color = colorDefault(0), alpha = 0.65)
    plt.grid(True, which = 'both', zorder = 1)
    plt.title('Annual Maintenance Cost')
    plt.xlabel('Time [yr]')
    plt.ylabel('Cost [$]')
    plt.xlim(0, lifespan + 1)
    plt.ylim(0, annualMaintUpperLim)
    plt.figure('MaintenanceExpenditureByYear')
    plt.plot(timeSpace, maintExpUtil, color = colorDefault(2), zorder = 2)
    plt.plot(timeSpace, maintExpKC, color = colorDefault(0), zorder = 3)
    plt.scatter(timeSpace[12 * lifespan], maintExpUtil[12 * lifespan], color = colorDefault(1), zorder = 3, s = 25)
    plt.scatter(timeSpace[12 * lifespan], maintExpKC[12 * lifespan], color = colorDefault(3), zorder = 4, s = 25)
    proportion = (((0.94 * maintExpUpperLim) - maintExpUtil[12 * lifespan]) + maintExpKC[12 * lifespan]) / maintExpUpperLim
    if (proportion > 0.79):
        proportion = ((maintExpKC[12 * lifespan] - ((0.94 * maintExpUpperLim) - maintExpUtil[12 * lifespan])) / maintExpUpperLim) - 0.01
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
        plt.plot(damageRange, difference)
        plt.xlim(damageRange[0], damageRange[checkPoints])
        plt.title(r'$\mathrm{Optimization} \: \: \mathrm{of} \: \: e^{R}$')
        plt.ylabel(r'$|\frac{\alpha x e^{\rho_{0} N - \rho_{0} \Delta t} (1 - e^{\rho_{0} \Delta t})  (x^{N} - 1)}{\Delta t (1 - e^{\rho_{0} N}) (x - 1)} - e^{NR}|$')
        plt.xlabel(r'$e^{R}$')
    plt.show()


def MaintFuncUtil(M_1, inflationRate, contractSpan, t):
    maintenance = M_1 * exp(inflationRate * contractSpan * floor((t - 1) / contractSpan))
    return maintenance

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
