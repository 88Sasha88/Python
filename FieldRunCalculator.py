import numpy as numpy
from numpy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

area = 0.123 # relevant cross-sectional area for calculating scoopy flux [m^2]
rho = 1000 # density of water [kg / m^3]

def main():

    fileString = '/Users/sashacurcic/Documents/Sasha/MarkStuff/IMG_0040-IMG_0041.txt' # field test readings file
    resistance = 25 # resistor Mark used for the alternator or rectifier
    velocity = [x.split()[0] for x in open(fileString).readlines()] # read in velocity values [km / hr]
    velocity = [float(i) for i in velocity] # convert velocity string values to floats [km / hr]
    voltage = [x.split()[1] for x in open(fileString).readlines()] # read in voltage values [V]
    voltage = [float(i) for i in voltage] # convert voltage string values to floats [V]
    velocityConv = list(map(lambda x: (1000. / (60. * 60.)) * x, velocity)) # convert velocity values [m / sec]
    dataPoints = shape(velocityConv)[0] # total number of data points
    maxVelocity = max(velocityConv) # maximum recorded velocity [m / sec]
    minVelocity = min(velocityConv) # minimum recorded velocity [m / sec]
    velocityLinpace = linspace(minVelocity, maxVelocity, num = 50) # evenly segmented linspace of velocity points in range of actual readings [m / sec]
    wattage = multiply(voltage, voltage) / resistance # power readings we gathered corresponding to our voltage readings (assuming a simple, single-loop circuit, which isn't perfectly accurate) [W]
    wattageMax = 0.5 * area * rho * multiply(multiply(velocityLinpace, velocityLinpace), velocityLinpace) # maximum available velocity at given flux [W]

    params, garbage = curve_fit(WattFunction, velocityConv, wattage) # data fitted for coefficient of third-degree monomial function
    print 'params =', params # best fit coefficient of third-degree monomial [kg / m]
    print 'Watts at 2 m/sec:', WattFunction(2, params)
    print 'Watts at 5 mi/hr:', WattFunction(EnglishToMetric(5), params)
    print 'Area needed to produce 15 kW at current performance:', (area * 15000) / (params * (2 ** 3)), (2 * 15000) / (0.38 * rho * (2 ** 3)) # two ways of calculating same value for comparison

    velocityRange = maxVelocity - minVelocity # range of velocity readings [m / sec]
    bins = 5 # number points at which I wanted to calculate efficiency
    binSize = velocityRange / bins # increments between which I wanted to calculate efficiency [m / sec]
    x = linspace(velocityConv[0] + (binSize / 2), velocityConv[dataPoints - 1] - (binSize / 2), bins) # linspace of velocities at which I want to calculate efficiency
    y = WattFunction(x, params) + 10 # linspace of y coordinates at which I want to print efficiency on graph [W]
    percentage = ((y - 10) * 100) / (0.5 * area * rho * multiply(multiply(x, x), x)) # efficiency at given point [%]
    print percentage
    for i in range(bins):
        percentage[i] = round(percentage[i], 0) # round percentages to integer values [%]
    percentage = asarray(asarray(percentage, int), str) # convert percentages to ints and then to strings [%]
    percent = '%' # percent symbol string
    for i in range(bins):
        percentage[i] = '%s%s' %(percentage[i], percent) # percent symbol to percentages [%]

    fig, ax = plt.subplots()
    ax.scatter(velocityConv, wattage, zorder = 1, s = 8, label = '1', color = colorDefault(0)) # plot scatter of collected data
    plot2, = plt.plot(numpy.unique(velocityConv), numpy.unique(WattFunction(velocityConv, params)), zorder = 2, color = colorDefault(3), linewidth = 1.5, label = '2') # plot best fit line of collected data
    plt.plot(x, y, alpha = 0) # plot percent efficiencies
    for i in range(bins):
        plt.text(x[i], y[i], percentage[i])
    plot3, = plt.plot(velocityLinpace, wattageMax, zorder = 3, color = colorDefault(1), linewidth = 1.5, label = '3') # plot maximum power curve
    plt.title(r'$\mathrm{25} \: \: \Omega \: \: \mathrm{Resistance,} \: \: \mathrm{1.5} \: \: \mathrm{Inch} \: \: \mathrm{Pulley}}$')
    plt.xlabel('Speed [m/sec]')
    plt.ylabel('Power [W]')
    handles, labels = ax.get_legend_handles_labels() # This gets your labels for use in the legend.
    print 'HANDLES ARE RIGHT HERE:', handles
    print labels
    labels, handles = zip(*sorted(zip(labels, handles), key = lambda t: t[-2])) # This sorts your labels alphabetically for use in the legend. (t takes either -2, -1, 0, or 1) I really don't fully get what's happening here, but after about an hour of trial and error, this is what worked.
    print 'HANDLES ARE RIGHT HERE:', handles
    print labels
    labels = ['Experimentally Collected Data', 'Best Fit of Experimental Data', 'Maximum Available Power'] # This renames your labels for use in the legend. (You cannot dependably give the labels these names within the parameters of the plot original plot() and scatter() commands. You have to first label them with numbers for it to work as it should every time.)
    print labels
    ax.legend(handles, labels) # add legend

    # Mark wanted to know the power available in I think 10 square meters of Shasta Dam. The code from here is hideous because I didn't spend time prettying it up.

    plt.figure(2)
    wattageMax = (10 / area) * wattageMax
    meterToMile = (60. * 60.) / (0.0254 * 12. * 5280.)
    mileToMeter = (0.0254 * 12. * 5280.) / (60. * 60.)
    velocityLinpace = list(map(lambda x: meterToMile * x, velocityLinpace))
    mileVelocity = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    meterVelocity = list(map(lambda x: mileToMeter * x, mileVelocity))
    ShastaEnergy = 0.5 * 10 * rho * 24 * 365.25 * (10 ** (-9)) * multiply(multiply(meterVelocity, meterVelocity), meterVelocity)

    plt.plot(mileVelocity, ShastaEnergy, color = colorDefault(1))
    plt.plot(mileVelocity, ShastaEnergy, alpha = 0)
    ShastaEnergyRound = ShastaEnergy
    for i in range(11):
        ShastaEnergyRound[i] = round(ShastaEnergyRound[i], 3)
    for i in range(11):
        plt.text(mileVelocity[i], ShastaEnergy[i], ShastaEnergyRound[i])
    plt.title('Total Annual energy')
    plt.xlabel('Speed [mi/hr]')
    plt.ylabel('Energy [GW hr]')
    plt.show()

# This marks the return to non-garbage code.

def WattFunction(xVector, a): # third-degree monomial function (basically sets P = 0.5 * rho * area * velocity ** 3 to P = a * velocity ** 3. In other words, a = 0.5 * rho * area)
    yVector = a * multiply(multiply(xVector, xVector), xVector)
    return yVector

def MetricToEnglish(value): # velocity unit conversion function ([m / sec] to [mi / hr])
    newValue = (60 * 60 * value) / (0.0254 * 12 * 5280)
    return newValue

def EnglishToMetric(value): # velocity unit conversion function ([mi / hr] to [m / sec])
    newValue = (0.0254 * 12 * 5280 * value) / (60 * 60)
    return newValue

def colorDefault(k):
    if (k == 0):
        color = '#1f77b4' # blue
    else:
        if (k % 9 == 0):
            color = '#17becf' # cyan
        else:
            if (k % 8 == 0):
                color = '#bcbd22' # sickly greenish tan
            else:
                if (k % 7 == 0):
                    color = '#7f7f7f' # grey
                else:
                    if (k % 6 == 0):
                        color = '#e377c2' # pink
                    else:
                        if (k % 5 == 0):
                            color = '#8c564b' # brown
                        else:
                            if (k % 4 == 0):
                                color = '#9467bd' # purple
                            else:
                                if (k % 3 == 0):
                                    color = '#d62728' # red
                                else:
                                    if (k % 2 == 0):
                                        color = '#2ca02c' # green
                                    else:
                                        color = '#ff7f0e' # orange
    return color

main()
