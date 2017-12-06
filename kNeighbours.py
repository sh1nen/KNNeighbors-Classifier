import csv
import sys
import random
import math
import operator
import numpy as np

def loadDataset(filename,fullSet=[]):
	with open(filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset)-1):
			for y in range(len(dataset[x])-1):
				dataset[x][y] = float(dataset[x][y])
			fullSet.append(dataset[x])

def kFold(fullSet, split, species, trainingSet=[], testSet=[]):
	columns = np.shape(fullSet)[1]
	print('columns: ' + repr(species))
	for x in range(len(species)):
		kFoldSpecies([row for row in fullSet if (list(species)[x]) in row[(int)(repr(columns - 1))]], split, trainingSet, testSet)

def kFoldSpecies(species, split, trainingSet=[], testSet=[]):
	for x in range(len(species) - 1):
		if random.random() < split:
			trainingSet.append(species[x])
		else:
			testSet.append(species[x])

def countSpeciesInSet(dataSet, species):
	columns = np.shape(dataSet)[1]
	speciesOne = 0
	speciesTwo = 0
	speciesThree = 0
	for x in range(len(dataSet)):
		if dataSet[x][columns-1] == list(species)[0]:
			speciesOne += 1
		elif dataSet[x][columns-1] == list(species)[1]:
			speciesTwo += 1
		elif dataSet[x][columns-1] == list(species)[2]:
			speciesThree += 1
	print('Spiece one ' + repr(speciesOne))
	print('Spiece two ' + repr(speciesTwo))
	print('Spiece three ' + repr(speciesThree))

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
def normalize(dataSet=[]):
	for x in range(len(dataSet)-1):
		for y in range(len(dataSet[x]) - 1):
		 	dataSet[x][y] = (dataSet[x][y] - min(list([i[y] for i in dataSet]))) / (max(list([i[y] for i in dataSet])) - min(list([i[y] for i in dataSet])))

def main(fileName, distanceMethod, kNeighbors, isNormalized):
	# prepare data
	fullSet = []
	trainingSet=[]
	testSet=[]
	split = 0.33
	loadDataset(fileName, fullSet)
	print ('Full set: ' + repr(len(fullSet)))
	columns = np.shape(fullSet)[1]
	species = set([i[columns-1] for i in fullSet])
	kFold(fullSet, split, species, trainingSet, testSet)
	print ('Train set: ' + repr(len(trainingSet)))
	print ('Test set: ' + repr(len(testSet)))
	
	countSpeciesInSet(testSet, species)

	# generate predictions
	if isNormalized == 1:
		normalize(trainingSet)
		normalize(testSet)

	distanceMethods = (euclideanDistance, manhattanDistance, chybeshevDistance)
	for distanceMethod in distanceMethods:
		print('Method name: ' + repr(distanceMethod))
		for kNeighbor in kNeighbors:
			predictions=[]
			for x in range(len(testSet)):
				neighbors = getNeighbors(distanceMethod, trainingSet, testSet[x], kNeighbor)
				result = getResponse(neighbors)
				predictions.append(result)
				#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
			accuracy = getAccuracy(testSet, predictions)
			print('Accuracy: ' + repr(accuracy) + '%')

# MAIN FUNCTION CALL
# $1 - metric distanceMethod
# $2 - kNeighbors
# $3 - normalize dataSet ? (true or false)
kNeighbors = [1,3,5,10];
main(sys.argv[1], euclideanDistance, kNeighbors, int(sys.argv[2]))
