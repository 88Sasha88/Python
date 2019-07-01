import numpy as numpy
from scipy import *
from numpy import *
from numpy import linalg as LA
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axisartist.grid_finder import MaxNLocator
from mpl_toolkits.axisartist import (angle_helper, Subplot, SubplotHost, ParasiteAxesAuxTrans)
from mpl_toolkits.axisartist.grid_helper_curvelinear import (GridHelperCurveLinear)


def main():

    origin = [0, 0]
    xCoord = [1, -1]
    yCoord = [1, 2]
    transformation = [[1, 3], [5, 2]]
    [eigenvalue1, eigenvalue2], [eigenvector1, eigenvector2] = LA.eig(transformation)
    print eigenvalue1, eigenvalue2, (3 - sqrt(61)) / 2, (3 + sqrt(61)) / 2
    eigenvector1 = eigenvector1 / dot(eigenvector1, eigenvector1)
    eigenvector2 = eigenvector2 / dot(eigenvector2, eigenvector2)
    eigenCoord1 = zip(origin, 3 * eigenvalue1 * eigenvector1)
    print eigenvector1


    fig, ax = plt.subplots()
    x_grid_locator = MaxNLocator(3 // 0.0125)
    y_grid_locator = MaxNLocator(3 // 0.00625)
    ax = AA.Axes(fig, [0.1, 0.1, 0.8, 0.8], grid_helper = GridHelperCurveLinear((tr, inv_tr), grid_locator1 = x_grid_locator, grid_locator2 = y_grid_locator)) # This appears to be your margins
    fig.add_axes(ax)
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.axis["left"].set_visible(False)
    ax.axis["bottom"].set_visible(False)
    ax.grid(True, zorder = 0)
    # ax.set_xticks([0.01, 0.02, 0.03])
    ax.axis["t"] = ax.new_floating_axis(0, 0) # first argument appears to be slope, second argument appears to be starting point on vertical
    ax.axis["t2"] = ax.new_floating_axis(1, 0)
    # ax.axis["t"].set_xticks([1, 2, 3, 4, 5, 6])
    # ax.axis["t"].label.set_pad(2)
    ax.plot([0, 1], [0, 1])
    # ax.axis["y=0"] = ax.new_floating_axis(nth_coord=0, value=0)
    # # ax.axis["x=0"] = ax.new_floating_axis(nth_coord=0, value=0)
    # ax.axis["right2"] = ax.new_fixed_axis(loc="right", offset=(-184, 0))
    # ax.axis["t"] = ax.new_floating_axis(0, 0) # first argument appears to be slope, second argument appears to be starting point on vertical
    # ax.axis["t2"] = ax.new_floating_axis(1, 0)
    scalingFactor = (24 * sqrt(29)) / 5
    otherFactor = 12 * sqrt(5)
    print scalingFactor / 3
    print otherFactor / 3
    ax.set_xlim(-scalingFactor, scalingFactor)
    ax.set_ylim(-otherFactor, otherFactor)
    ax.quiver(origin, origin, xCoord, yCoord, color = [colorDefault(0), colorDefault(3)], angles = 'xy', scale_units = 'xy', scale=1)
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    # axis_to_data = ax.transAxes + ax.transData.inverted()
    # points_data = axis_to_data.transform((2, 3))
    # data_to_axis = axis_to_data.inverted()
    # numpy.testing.assert_allclose((2, 3), data_to_axis.transform(points_data))
    plt.xlim(-8, 8)
    plt.ylim(-8, 8)


    plt.figure()
    plt.quiver(origin, origin, xCoord, yCoord, color = [colorDefault(0), colorDefault(3)], angles = 'xy', scale_units = 'xy', scale=1)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    # axis_to_data = ax.transAxes + ax.transData.inverted()
    # points_data = axis_to_data.transform((2, 3))
    # data_to_axis = axis_to_data.inverted()
    # numpy.testing.assert_allclose((2, 3), data_to_axis.transform(points_data))
    plt.xlim(-8, 8)
    plt.ylim(-8, 8)

    fig = plt.figure()
    x_grid_locator = MaxNLocator(3 // 0.0125)
    y_grid_locator = MaxNLocator(3 // 0.00625)
    ax = AA.Axes(fig, [0.1, 0.1, 0.8, 0.8], grid_helper = GridHelperCurveLinear((tr, inv_tr), grid_locator1 = x_grid_locator, grid_locator2 = y_grid_locator)) # This appears to be your margins
    fig.add_axes(ax)
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.axis["left"].set_visible(False)
    ax.axis["bottom"].set_visible(False)
    ax.grid(True, zorder = 0)
    # ax.set_xticks([0.01, 0.02, 0.03])
    ax.axis["t"] = ax.new_floating_axis(0, 0) # first argument appears to be slope, second argument appears to be starting point on vertical
    ax.axis["t2"] = ax.new_floating_axis(1, 0)
    # ax.axis["t"].set_xticks([1, 2, 3, 4, 5, 6])
    # ax.axis["t"].label.set_pad(2)
    ax.plot([0, 1], [0, 1])
    # ax.axis["y=0"] = ax.new_floating_axis(nth_coord=0, value=0)
    # # ax.axis["x=0"] = ax.new_floating_axis(nth_coord=0, value=0)
    # ax.axis["right2"] = ax.new_fixed_axis(loc="right", offset=(-184, 0))
    # ax.axis["t"] = ax.new_floating_axis(0, 0) # first argument appears to be slope, second argument appears to be starting point on vertical
    # ax.axis["t2"] = ax.new_floating_axis(1, 0)
    scalingFactor = (24 * sqrt(29)) / 5
    otherFactor = 12 * sqrt(5)
    print scalingFactor / 3
    print otherFactor / 3
    ax.set_xlim(-scalingFactor, scalingFactor)
    ax.set_ylim(-otherFactor, otherFactor)

    plt.show()

def tr(x, y):
    x, y = numpy.asarray(x), numpy.asarray(y)
    return x + (3 * y), (2 * y) + (5 * x)

def inv_tr(x, y):
    x, y = numpy.asarray(x), numpy.asarray(y)
    return x - (3 * y), (2 * y) - (5 * x)

def curvelinear_test1(fig):
    """
    Grid for custom transform.
    """

    def tr(x, y):
        x, y = numpy.asarray(x), numpy.asarray(y)
        return x, y - (2 * x) # return x + (5 * y), (7 * y) + (3 * x)

    def inv_tr(x, y):
        x, y = numpy.asarray(x), numpy.asarray(y)
        return x, y + (2 * x)

    grid_helper = GridHelperCurveLinear((tr, inv_tr))

    ax1 = Subplot(fig, 1, 1, 1, grid_helper = grid_helper)
    # ax1 will have a ticks and gridlines defined by the given
    # transform (+ transData of the Axes). Note that the transform of
    # the Axes itself (i.e., transData) is not affected by the given
    # transform.

    fig.add_subplot(ax1)

    xx, yy = tr([0,1], [0, 2])
    ax1.plot(xx, yy, linewidth = 2.0)

    ax1.set_aspect(1)
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)

    ax1.axis["t"] = ax1.new_floating_axis(0, 0) # first argument appears to be slope, second argument appears to be starting point on vertical
    ax1.axis["t2"] = ax1.new_floating_axis(1, 0)
    ax1.axhline(y = 0, color = 'r')
    ax1.axvline(x = 0, color = 'r')
    ax1.grid(True, zorder = 0)

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

if __name__ == "__main__":
    fig = plt.figure(figsize=(7, 4))

    curvelinear_test1(fig)

    plt.show()

main()
