import pyqtgraph as pg
import numpy as np


def saveGraph(fileName, pyqtwidget):
    pass


def plotGraph(files):
    def graph_decorator(func):
        x, y, xaxis, xunits, yaxis, yunits, title = func(files)
    return(graph_decorator)

@plotGraph([])
def carsPerHour(files):
    return [0], [0], "", "", "", "", ""


graph_handles = {
    "Cars/Hour" : carsPerHour,
}
