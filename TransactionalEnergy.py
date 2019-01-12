import os.path
import numpy as numpy
from numpy import *
import sys as sys
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize, fmin_l_bfgs_b


def main():
    startTime = time.time()
    print os.path.basename(__file__)

    #####   CUSTOMIZABLE PARAMETERS   #####

    t_max = 24  # maximum radius
    dt = 1. / (60 * 60)  # radius increment

    V = 24  # sensor noise
    I_max = 30

    CCRange = 1.
    CCCenter = 12

    itermax = 12000  # maximum number of iterations

    #####   MODIFYING ANYTHING AFTER THIS POINT COULD ALTER THE LOGIC AND STRUCTURE OF THE CODE!!!   #####

    # numpy.set_printoptions(threshold = numpy.nan)

    if (itermax <= 0):
        sys.exit('itermax must be greater than 0!')
    if (type(itermax) is not int):
        sys.exit('itermax must be an integer!')

    if ((type(V) is not float) and (type(V) is not int)):
        sys.exit('V must be a numerical value!')

    if ((type(I_max) is not float) and (type(I_max) is not int)):
        sys.exit('I_max must be a numerical value!')

    Nt = int(t_max / dt)  # number of grid points in vertical direction

    tAxis = linspace(0, t_max, num = Nt + 1)

    P = V * (((I_max / 2) * sin((pi / 12) * tAxis)) + (I_max / 2))

    Dimensions = [tAxis, t_max, dt]
    Calculations = [P, V, CCRange]
    Constants = [Dimensions, Calculations]

    PMinimum, PMaximum, TotalEnergy = residuals(CCCenter, Constants)
    results = minimize(energyMax, CCCenter, args = (Constants), method = 'L-BFGS-B', bounds = ((V * (CCRange / 2), V * I_max), ), options \
        = {'maxiter': itermax, 'maxcor': 625, 'gtol': 1e-8})

    # results2 = fmin_l_bfgs_b(energyMax(CCCenter, ), maxiter = itermax, pgtol = 1e-8)

    print 'Total Energy =', TotalEnergy

    print results



    plt.figure()
    plt.plot(tAxis, P)
    plt.fill_between(tAxis, PMinimum, PMaximum)
    plt.xlim(0, 24)
    plt.title('Power Availability Throughout Day')
    plt.xlabel('Time [hr]')
    plt.ylabel('Power [W]')
    plt.show()

def energyMax(CCCenter, Constants):
    PMinimum, PMaximum, TotalEnergy = residuals(CCCenter, Constants)
    inverseEnergy = 1 / (TotalEnergy ** 2)
    return inverseEnergy

def residuals(CCCenter, Constants):
    Dimensions, Calculations = Constants
    tAxis, t_max, dt = Dimensions
    P, V, CCRange = Calculations

    PControlCenter = V * CCCenter
    PControlRange = V * CCRange

    P_max = PControlCenter + (PControlRange / 2)
    P_min = PControlCenter - (PControlRange / 2)

    PMaximum = ma.masked_where(P > P_max, P).filled(fill_value = P_max)
    PMinimum = ma.masked_where(P > P_min, P).filled(fill_value = P_min)
    EnergyMax = trapz(PMaximum, dx = dt)
    EnergyMin = trapz(PMinimum, dx = dt)

    TotalEnergy = EnergyMax - EnergyMin

    return PMinimum,PMaximum, TotalEnergy

def errorChecker(x, y):
    if (shape(x) != shape(y)):
        message = 'These results are not the same shape.'
    else:
        if (all(equal(x, y)) != True):
            differenceArray = y - x
            if (size(x) == 1):
                difference = differenceArray
                percentError = (difference / y) * 100
                differenceString = str(difference)
                percentErrorString = str(percentError)
                percentSign = str('%')
                message = 'These results are %s off from each other with a %s%s error.' % (differenceString, \
                                                                                           percentErrorString,
                                                                                           percentSign)
            else:
                percentError = mean(numpy.ma.masked_invalid(differenceArray / y, nan)) * 100
                difference = mean(differenceArray)
                differenceString = str(difference)
                percentErrorString = str(percentError)
                percentSign = str('%')
                message = 'These results are an average of %s off from each other with a %s%s error on average.' \
                          % (differenceString, percentErrorString, percentSign)
        else:
            message = 'These results are the same.'
    return message


main()