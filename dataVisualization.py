import csv
import numpy as np
import pyqtgraph as pg
import datetime


def SaveGraph(fileName, pyqtwidget):
    exporter = pg.exporters.ImageExporter(pyqtwidget.plotItem)
    exporter.export(fileName)

def plotGraph(func):
    def graph_decorator(files, plotwidget, hour):
        x, y, xaxis, xunits, yaxis, yunits, title, pen = func(files, plotwidget, hour)
        symbol = None
        ticks = None
        if isinstance(x, dict):
            ticks = [x.items()]
            x = list(x.keys())
        if len(x) == 1:
            pen = None
        if not pen:
            symbol = 'o'
        ax = plotwidget.getAxis("bottom")
        ax.setTicks(ticks)
        plotwidget.plot(x, y, pen=pen, symbol=symbol)
        plotwidget.setTitle(title)
        plotwidget.setLabel("bottom", xaxis, xunits)
        plotwidget.setLabel("left", yaxis, yunits)
    return(graph_decorator)

@plotGraph
def carsPerHour(files, plotwidget, hour):
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
    return x, y, "Time", "Hours", "Flow", "# of Cars", "Cars Per Hour", (1,1)

@plotGraph
def carsPerSpeed(files, plotwidget, hour):
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

@plotGraph
def heightPerLength(files, plotwidget, hour):
    x = []
    y = []
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                speed = 0.0001 / float(row[4]) * 1000.0 * 3600.0
                length = float(speed) * float(row[3]) / 100.0
                x.append(row[5])
                y.append(length)
    return x, y, "Length of Cars", "cm", "Ground Clearance", "cm", "Ground Clearance per Car Length", None

@plotGraph
def speedPerLength(files, plotwidget, hour):
    x = []
    y = []
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                speed = 0.0001 / float(row[4]) * 1000.0 * 3600.0
                length = float(speed) * float(row[3]) / 100.0
                x.append(speed)
                y.append(length)
    return x, y, "Length of Cars", "cm", "Speed", "kmh", "Car Speed per Car Length", None

@plotGraph
def speedPerHour(files, plotwidget, hour):
    graphDict = {}
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                speed = 0.0001 / float(row[4]) * 1000.0 * 3600.0
                t = (int(row[1]) / 3600) * 3600
                if t in graphDict:
                    graphDict[t][0] += speed
                    graphDict[t][1] += 1
                else:
                    graphDict[t] = [speed, 1]
    x = []
    y = []
    keylist = graphDict.keys()
    keylist.sort()
    for key in keylist:
        x.append(datetime.datetime.fromtimestamp(int(key)).strftime('%Y-%m-%d %H:%M:%S'))
        y.append(int(graphDict[key][0]/graphDict[key][1]))
    x = dict(enumerate(x))
    return x, y, "Time", "Hours", "Speed", "kmh", "Speed of Cars Per Hour", (1,1)

@plotGraph
def speedDistribution(files, plotwidget, hour):
    graphDict = {}
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                speed = 0.0001 / float(row[4]) * 1000.0 * 3600.0
                t = datetime.datetime.fromtimestamp((int(row[1]) / 3600) * 3600).hour
                if t == hour:
                    if speed in graphDict:
                        graphDict[t] += 1
                    else:
                        graphDict[t] = 1
    x = []
    y = []
    keylist = graphDict.keys()
    keylist.sort()
    for key in keylist:
        x.append(int(key))
        y.append(int(graphDict[key]))
    return x, y, "Speed", "kmh", "Flow", "# of Cars", "Speed distribution at "+str(hour)+" o'clock", None

@plotGraph
def longPerHour(files, plotwidget, hour):
    graphDict = {}
    for file in files:
        with open(file, 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                length = float(speed) * float(row[3]) / 100.0
                if length > 700:
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
    return x, y, "Time", "Hours", "Long Flow", "# of Long Vehicles", "Vehicles Longer than 7m Per Hour", (1,1)


graph_handles = {
    "Cars/Hour" : carsPerHour,
    "Cars/Speed" : carsPerSpeed,
    "Height/Length" : heightPerLength,
    "Speed/Length" : speedPerLength,
    "Avg Speed/Hour" : speedPerHour,
    "Speed Distribution" : speedDistribution,
    "Long Cars/Hour" : longPerHour,
}
