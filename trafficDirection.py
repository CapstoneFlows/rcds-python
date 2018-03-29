import os
import numpy as np
from array import array

def getTrafficFlow(infiles, outfiles):
	return None

def getTrafficFlow(filterData,directions):

	# Data Initialization
	maxTime = 20
	minTime = 2
	errorHeight = 0.1
	errorLength = 0.1
	found = False
	identified = []
	directionsTime = {"EWEW":[],"EWSN":[],"EWNS":[],"EWWE":[],
						"WEWE":[],"WENS":[],"WESN":[],"WEEW":[],
						"NSNW":[],"NSEW":[], "NSWE":[],"NSSN":[],
						"SNSN":[],"SNWE":[],"SNEW":[],"SNNS":[],"UNIDENTIFIED":[]}
	directionsCount = {"EWEW":0,"EWSN":0,"EWNS":0,"EWWE":0,
						"WEWE":0,"WENS":0,"WESN":0,"WEEW":0,
						"NSNW":0,"NSEW":0, "NSWE":0,"NSSN":0,
						"SNSN":0,"SNWE":0,"SNEW":0,"SNNS":0,"UNIDENTIFIED":0}

	# Iterate through every data with i
	for i in range(len(filterData)):
		found = False #Initialize found with false

		# If id of filterData matches any in list of directions
		# Assign the directions to the last field
		if any((id == filterData[i][0]) for id in directions["EW"]):
			filterData[i].append("EW")
		if any((id == filterData[i][0]) for id in directions["WE"]):
			filterData[i].append("WE")
		if any((id == filterData[i][0]) for id in directions["NS"]):
			filterData[i].append("NS")
		if any((id == filterData[i][0]) for id in directions["SN"]):
			filterData[i].append("SN")

		# If the vehicle is outbound
		if (filterData[i][2] == 0):


			# For every vehicle before it
			for j in range(i):		

				if  ((j not in identified)
					(found == False) and  # If not found yet
					(filterData[j][1] > (filterData[i][1] - maxTime)) and # if the vehicle is not too early
					(filterData[j][1] < filterData[i][1] - minTime) and # if the vehicle is not late
					(filterData[j][2] == 1) and # if the vehicle is inbound
					(filterData[j][5] * (1 - errorHeight) < filterData[i][5] < filterData[j][5] *(1 + errorHeight)) and # If the vehicle's height is smillar within error
					(getLength(filterData[j][3],filterData[j][4]) * (1 - errorLength) < getLength(filterData[i][3],filterData[i][4]) < getLength(filterData[j][3],filterData[j][4]) *(1 + errorLength))): # If the vehicle's length is smillar within error
						# Inbound direction join outbound direction  += 1
						directionsTime[filterData[j][6] + filterData[i][6]].append(filterData[j][1])
						directionsCount[filterData[j][6] + filterData[i][6]] += 1
						found = True # found is true
						identified.append(j)

			# If not found at the end, unidentified vehicle +=1
			if (found == False):
				directionsCount["UNIDENTIFIED"] += 1

	return directionsCount, directionsTime


def getLength(timeOccluded, deltaTime):
	speed = 0.0001 / float(deltaTime) * 1000.0 * 3600.0
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