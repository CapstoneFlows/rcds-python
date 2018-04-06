import csv
import os
import json
import datetime
import numpy as np

def ProcessData(path, files, filters):
    filterData = None
    for file in files:
        with open(os.path.join(path,file),'rU') as csvfile:
            csvreader = csv.reader(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
            for row in csvreader:
                speed = 0.0001 / float(row[4]) * 1000.0 * 1000.0 * 3600.0
                length = float(speed) * float(row[3]) / 100.0
                if (int(row[1]) > filters["EDateTime"]) and \
                    (int(row[1]) < filters["LDateTime"]) and \
                    (int(row[3]) > filters["MinTO"]) and \
                    (int(row[3]) < filters["MaxTO"]) and \
                    (int(row[5]) > filters["MinCMH"]) and \
                    (int(row[5]) < filters["MaxCMH"]) and \
                    (speed > filters["MinS"]) and \
                    (speed < filters["MaxS"]) and \
                    (length > filters["MinCML"]) and \
                    (length < filters["MaxCML"]):
                        if filterData is None:
                            filterData = np.array(row).astype(int)
                        else:
                            filterData = np.vstack((filterData, np.array(row).astype(int))) 
    filterData = json.dumps(filterData.tolist()).replace('],', '],\n')
    return filterData

def SaveData(path, data):
    data = np.array(json.loads(data.replace ('],\n', '],')))
    np.savetxt(path, data, fmt='%s', delimiter=",")


def SavePrettyData(path, data):
    data = np.array(json.loads(data.replace ('],\n', '],')))
    with open(path, 'wb') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(['ID', 'Start Time', 'Time Occluded', 'Length', 'Speed', 'Ground Clearance'])
        writer.writerow(['', '', 'ms', 'cm', 'kmh', 'cm'])

        def MakeRow( x ):
            row = []
            speed = 0.0001 / float(x[4]) * 1000.0 * 1000.0 * 3600.0
            length = float(speed) * float(x[3]) / 100.0
            row.append(x[0])
            row.append(datetime.datetime.fromtimestamp(int(x[1])).strftime('%Y-%m-%d %H:%M:%S'))
            row.append(x[3])
            row.append(length)
            row.append(speed)
            row.append(x[5])
            writer.writerow(row)

        np.apply_along_axis( MakeRow, axis=1, arr=data )