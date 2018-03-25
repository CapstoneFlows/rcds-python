import csv
import numpy as np
import pyqtgraph as pg
import datetime


def saveGraph(fileName, pyqtwidget):
    pass


def plotGraph(func):
    def graph_decorator(files, plotwidget):
        x, y, xaxis, xunits, yaxis, yunits, title = func(files, plotwidget)
        if isinstance(x, dict):
            plotwidget.plot(list(x.keys()), y)
            ax = plotwidget.getAxis("bottom")
            ax.setTicks([x.items()])
        else:
            plotwidget.plot(x, y)
        plotwidget.setTitle(title)
        plotwidget.setLabel("bottom", xaxis, xunits)
        plotwidget.setLabel("left", yaxis, yunits)
    return(graph_decorator)

@plotGraph
def carsPerHour(files, plotwidget):
    graphDict = {}
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                t = (int(row[0]) / 3600) * 3600
                if t in graphDict:
                    graphDict[t] += 1
                else:
                    graphDict[t] = 1
    x = []
    y = []
    keylist = graphDict.keys()
    keylist.sort()
    for key in keylist:
        x.append(datetime.datetime.fromtimestamp(int(key)).strftime('%Y-%m-%d %H:%M:%S'))
        y.append(int(graphDict[key]))
    x = dict(enumerate(x))
    return x, y, "Time", "Hours", "Flow", "# of Cars", "Cars Per Hour"


graph_handles = {
    "Cars/Hour" : carsPerHour,
}
