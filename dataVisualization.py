import csv
import numpy as np
import pyqtgraph as pg
import datetime


def saveGraph(fileName, pyqtwidget):
    pass


def plotGraph(func):
    def graph_decorator(files, plotwidget):
        x, y, xaxis, xunits, yaxis, yunits, title, pen = func(files, plotwidget)
        symbol = None
        ticks = None
        if not pen:
            symbol = 'o'
        if isinstance(x, dict):
            ticks = [x.items()]
            x = list(x.keys())
        ax = plotwidget.getAxis("bottom")
        ax.setTicks(ticks)
        plotwidget.plot(x, y, pen=pen, symbol=symbol)
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
                t = (int(row[1]) / 3600) * 3600
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
    return x, y, "Time", "Hours", "Flow", "# of Cars", "Cars Per Hour", ((1,1) if len(x.keys()) > 1 else None)


@plotGraph
def carsPerSpeed(files, plotwidget):
    graphDict = {}
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                s = int(0.0001 / float(row[4]) * 1000.0 * 3600.0)
                if s in graphDict:
                    graphDict[s] += 1
                else:
                    graphDict[s] = 1
    x = []
    y = []
    keylist = graphDict.keys()
    keylist.sort()
    for key in keylist:
        x.append(key)
        y.append(int(graphDict[key]))
    return x, y, "Speed", "kmh", "Flow", "# of Cars", "Cars Per Speed", None


graph_handles = {
    "Cars/Hour" : carsPerHour,
    "Cars/Speed" : carsPerSpeed,
}
