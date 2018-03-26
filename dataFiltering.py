import csv
import os
import numpy as np

def ProcessData(path, files, filters):
    filterData = None
    for file in files:
        with open(os.path.join(path,file),'rU') as csvfile:
            csvreader = csv.reader(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                speed = 0.0001 / float(row[3]) * 1000.0 * 3600.0
                length = float(speed) * float(row[2]) / 100.0
                if (int(row[0]) > filters["EDateTime"]) and \
                    (int(row[0]) < filters["LDateTime"]) and \
                    (int(row[2]) > filters["MinTO"]) and \
                    (int(row[2]) < filters["MaxTO"]) and \
                    (int(row[4]) > filters["MinCMH"]) and \
                    (int(row[4]) < filters["MaxCMH"]) and \
                    (speed > filters["MinS"]) and \
                    (speed < filters["MaxS"]) and \
                    (length > filters["MinCML"]) and \
                    (length < filters["MaxCML"]):
                        if filterData is None:
                            filterData = np.array(row).astype(int)
                        else:
                            filterData = np.vstack((filterData, np.array(row).astype(int))) 
    return filterData

def SaveData(path, data):
    np.savetxt(path, data, fmt='%i', delimiter=",")
    