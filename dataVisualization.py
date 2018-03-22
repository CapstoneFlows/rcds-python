import pyqtgraph as pg
import numpy as np


def saveGraph(fileName, pyqtwidget):
    pass


def plotGraph(files, plotwidget):
    def graph_decorator(func):
        x, y, xaxis, xunits, yaxis, yunits, title = func(files, plotwidget)
        plotwidget.plot(x,y, title=title, labels={"left":(yaxis, yunits), "right":(xaxis, xunits)})
    return(graph_decorator)

@plotGraph([], pg)
def carsPerHour(files, plotwidget):
    return [0], [0], "", "", "", "", ""


graph_handles = {
    "Cars/Hour" : carsPerHour,
}
