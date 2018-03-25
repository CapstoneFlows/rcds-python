import csv
import os

def ProcessData(path, files, filters):
	filterData = np.empty((0,6), int)
	for file in files:
		with open(os.path.join(path,file),'rb') as csvfile:
             csvreader = csv.reader(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
             for row in reader:
				speed = (0.1/1.6 / row[4]/1000/3600)
				if (row[1] > filters["EDateTime"]) and
    				(row[1] < filters["LDateTime"]) and
    				(row[3] > filters["MinTO"]) and
					(row[3] < filters["MaxTO"]) and
    				(row[5] > filters["MinCM"]) and
    				(row[5] < filters["MaxCM"]) and
    				(row[4] < filters["MinMD"]) and
    				(row[4] > filters["MaxMD"]) and
    				(speed < filters["MinS"]) and
    				(speed > filters["MaxS"]):
						np.append(filterData, np.array(row), axis=0) 

    return filterData;

def SaveData(data, savePath):
    pass