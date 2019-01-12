import numpy as numpy
from numpy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit

area = 0.123
rho = 1000
resistance = 25

def main():

    fileString = '/Users/sashacurcic/Documents/Sasha/MarkStuff/IMG_0040-IMG_0041.txt'
    resistance = 25
    velocity = [x.split()[0] for x in open(fileString).readlines()]
    velocity = [float(i) for i in velocity]
    voltage = [x.split()[1] for x in open(fileString).readlines()]
    voltage = [float(i) for i in voltage]
    velocityConv = list(map(lambda x: (1000. / (60. * 60.)) * x, velocity))
    dataPoints = shape(velocityConv)[0]
    Vandermonde = zeros((dataPoints, 4), float)
    Vandermonde[:, 3] = multiply(multiply(velocityConv, velocityConv), velocityConv)
    VandermondeTrans = transpose(Vandermonde)
    VandermondeMult = matmul(VandermondeTrans, Vandermonde)
    velocityFew = sort(Counter(velocity).keys())
    velocityFewConv = list(map(lambda x: (1000. / (60. * 60.)) * x, velocityFew))
    wattage = multiply(voltage, voltage) / resistance
    wattageMax = 0.5 * area * rho * multiply(multiply(velocityFewConv, velocityFewConv), velocityFewConv)
    print Vandermonde
    print VandermondeTrans
    print VandermondeMult

    params, params_covariance = curve_fit(WattFunction, velocityConv, wattage)
    print 'params =', params
    print 'params_covariance =', params_covariance

    vRange = velocityConv[dataPoints - 1] - velocityConv[0]
    bins = 5
    binSize = vRange / bins
    x = linspace(velocityConv[0] + (binSize / 2), velocityConv[dataPoints - 1] - (binSize / 2), bins)
    y = WattFunction(x, params) + 10
    percentage = ((y - 10) * 100) / (0.5 * area * rho * multiply(multiply(x, x), x))
    print percentage
    for i in range(bins):
        percentage[i] = round(percentage[i], 0)
    percentage = asarray(asarray(percentage, int), str)
    percent = '%'
    for i in range(bins):
        percentage[i] = '%s%s' %(percentage[i], percent)
    print velocityConv[0], velocityConv[dataPoints - 1]
    print binSize
    print percentage
    print int(round(5.666, 0))



    plt.figure()
    color1 = '#d62728'
    color2 = '#ff7f0e'
    plt.scatter(velocityConv, wattage, s = 8)
    # plt.plot(numpy.unique(velocityConv), numpy.poly1d(numpy.polyfit(velocityConv, wattage, 3))(numpy.unique(velocityConv)), color = 'g')
    plt.plot(numpy.unique(velocityConv), numpy.unique(WattFunction(velocityConv, params)), color = color1)
    # x = [1, 2, 3]
    # y = [9, 8, 7]
    plt.plot(x, y, alpha = 0)
    for i in range(bins):
        # print a, b
        plt.text(x[i], y[i], percentage[i])
    # plt.plot(velocityConv[0], label = '50%')
    plt.plot(velocityFewConv, wattageMax, color = color2)
    plt.title('25-Ohm Resistance, 1.5-Inch Diameter Pulley')
    plt.xlabel('Speed [m/sec]')
    plt.ylabel('Power [W]')
    plt.show()

def WattFunction(xVector, a):
    yVector = a * multiply(multiply(xVector, xVector), xVector)
    return yVector


main()
