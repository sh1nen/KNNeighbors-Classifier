import csv
import random
import math
import operator

def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'r') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(len(dataset[x]) - 1):
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

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

#NOT WORKING AS IT SHOULD/ NORMALIZE EACH ROW TO [0-1]
def normalize(dataSet):
	for x in range(len(dataSet)):
		for y in range(len(dataSet[x]) - 1):
		 	dataSet[x][y] = (dataSet[x][y] - min(dataSet[x][0:len(dataSet[x]) - 1])) / (max(dataSet[x][0:len(dataSet[x]) - 1]) - min(dataSet[x][0:len(dataSet[x]) - 1]))

def main(distanceMethod, kNeighbors):
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('iris.data', split, trainingSet, testSet)
	print ('Train set: ' + repr(len(trainingSet)))
	print ('Test set: ' + repr(len(testSet)))
	# generate predictions
	predictions=[]
	for x in range(len(testSet)):
		neighbors = getNeighbors(distanceMethod, trainingSet, testSet[x], kNeighbors)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')

# MAIN FUNCTION CALL
main(euclideanDistance, 3)
