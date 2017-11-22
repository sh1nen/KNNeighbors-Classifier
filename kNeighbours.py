import csv
import random
import math
import operator
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'r') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def manhattanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += abs(instance1[x] - instance2[x])
	return distance

def chybeshevDistance(instance1, instance2, lenght):
	distanceMax = []
	distance = 0
	for x in range(lenght):
		distance = abs(instance1[x] - instance2[x])
		distanceMax.append(distance)
	return max(distanceMax)

def getNeighbors(distanceMethod, trainingSet, testInstance, k):
	distances = []
	lenght = len(testInstance) - 1
	for x in range(len(trainingSet)):
		dist = distanceMethod(testInstance, trainingSet[x], lenght)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

trainSet = [[2,2,2,'a'], [4,4,4,'b']]
testInstance = [5,5,5]
k = 1
neighbors = getNeighbors(manhattanDistance, trainSet, testInstance, 1)
print(neighbors)
