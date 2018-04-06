import os
import csv
import json
import numpy as np


def takeTime(data):
    return data[1]

def GetIDs(path, mapfiles):
    ids = {}
    for file in mapfiles:
        with open(os.path.join(path,file),'rU') as csvfile:
            csvreader = csv.reader(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                if row[0] not in ids:
                    ids[row[0]] = 1
    dids = ids.keys()
    dids.sort()
    return dids

def SaveOrderFile(path, name, data):
    with open(os.path.join(path, name), 'w') as f:
        json.dump(data, f)

def getTrafficFlow(path, files, inIds, outIds):

    # Data Initialization
    maxTime = 20
    minTime = 2
    errorHeight = 0.1
    errorLength = 0.1
    found = False
    identified = []
    directions = {"NS":[0,[]],"NE":[0,[]],"NW":[0,[]],
                  "SN":[0,[]],"SE":[0,[]],"SW":[0,[]],
                  "EN":[0,[]],"ES":[0,[]], "EW":[0,[]],
                  "WN":[0,[]],"WE":[0,[]],"WS":[0,[]], "UNIDENTIFIED":[0,[]]}

    files.sort()
    filterData = []
    for file in files:
        with open(os.path.join(path, file), 'rU') as f:
            csvreader = csv.reader(f, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                row[0] = str(row[0])
                row[1] = int(row[1])
                row[2] = int(row[2])
                row[3] = int(row[3])
                row[4] = int(row[4])
                row[5] = int(row[5])
                filterData.append(row)

    filterData.sort(key=takeTime)

    # Iterate through every data with i
    for i in range(len(filterData)):
        found = False #Initialize found with false
        filterData[i].append("")
        # If id of filterData matches any in list of directions
        # Assign the directions to the last field
        if "EIn" in inIds:
            if filterData[i][0] in inIds["EIn"]:
                filterData[i][6] = "EIn"
        if "WIn" in inIds:
            if filterData[i][0] in inIds["WIn"]:
                filterData[i][6] ="WIn"
        if "NIn" in inIds:
            if filterData[i][0] in inIds["NIn"]:
                filterData[i][6] ="NIn"
        if "SIn" in inIds:
            if filterData[i][0] in inIds["SIn"]:
                filterData[i][6] ="SIn"
        if "EOut" in outIds:
             if filterData[i][0] in outIds["EOut"]:
                 filterData[i][6] ="EOut"
        if "WOut" in outIds:
            if filterData[i][0] in outIds["WOut"]:
                filterData[i][6] ="WOut"
        if "NOut" in outIds:
            if filterData[i][0] in outIds["NOut"]:
                filterData[i][6] ="NOut"
        if "SOut" in outIds:
            if filterData[i][0] in outIds["SOut"]:
                filterData[i][6] ="SOut"
        
        # If the vehicle is outbound
        if 'Out' in filterData[i][6]:

            # For every vehicle before it
            for j in range(i):
                if  (j not in identified) and ('In' in filterData[j][6]): # if the vehicle is inbound
                    if (found == False) and \
                        (filterData[j][1] > (filterData[i][1] - maxTime)) and \
                        (filterData[j][1] < filterData[i][1] - minTime) and \
                        (filterData[j][5] * (1 - errorHeight) < filterData[i][5] < filterData[j][5] *(1 + errorHeight)) and \
                        (getLength(filterData[j][3],filterData[j][4]) * (1 - errorLength) < getLength(filterData[i][3],filterData[i][4]) < getLength(filterData[j][3],filterData[j][4]) *(1 + errorLength)): # If the vehicle's length is smillar within error
                            # Inbound direction join outbound direction  += 1
                            dirStr = filterData[j][6].split('In')[0] + filterData[i][6].split('Out')[0]
                            directions[dirStr][0] += 1
                            directions[dirStr][1].append(filterData[i][1])
                            found = True # found is true
                            identified.append(j)
                            break

            # If not found at the end, unidentified vehicle +=1
            if (found == False):
                directions["UNIDENTIFIED"][0] += 1
                directions["UNIDENTIFIED"][1].append(filterData[i][1])

    return directions


def getLength(timeOccluded, deltaTime):
    speed = 0.0001 / float(deltaTime) * 1000.0 * 1000.0 * 3600.0
    return (float(speed) * float(timeOccluded) / 100.0)
    

if __name__ == "__main__":

    # Hardcode testing
    car1 = [1,1521230448, 1, 704, 70, 21]
    car2 = [1,1521230452, 1, 693, 104, 22]
    car3 = [2,1521230450, 1, 981, 36, 20]
    car4 = [2,1521230453, 1, 678, 32, 20]

    car5 = [3,1521230458, 0, 704, 70, 22] #left
    car6 = [3,1521230459, 0, 693, 104, 22] #left
    car7 = [4,1521230456, 0, 981, 36, 20] #right
    car8 = [4,1521230459, 0, 678, 32, 20] #right
    car9 = [4,15459, 0, 499, 60,21] # Unidentified(Too early)
    car10 = [4,152123500, 0, 499, 60,21] # Unidentified(Too late)
    car11 = [4,152120459, 0, 499, 60,24] # Unidentified(Too high)
    car12 = [4,152120459, 0, 200, 60,20] # Unidentified(Too fast)

    directions={"EW":[1],"WE":[4],"NS":[3],"SN":[2]}

    filterData = np.empty((0,6), int)
    filterData = [car9, car1,car3, car2, car4, car7, car5, car6, car8, car11,car12,car10]
    directionsCount, directionsTime = getTrafficFlow(filterData, directions)


    for key,value in directionsCount.items():
        print key + " " + str(value)

    for key,value in directionsTime.items():
        print key + " " + str(value)