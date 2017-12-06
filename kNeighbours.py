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

def kFold(fullSet, species, firstFold=[], secondFold=[], thirdFold=[]):
	columns = np.shape(fullSet)[1]
	for x in range(len(species)):
		kFoldSpecies([row for row in fullSet if (list(species)[x]) in row[(int)(repr(columns - 1))]], firstFold, secondFold, thirdFold)

def kFoldSpecies(species, firstFold=[], secondFold=[], thirdFold=[]):
	random.shuffle(species)
	listOfLists = list(chunkify(species, 3))
	firstFold.extend(listOfLists[0])
	secondFold.extend(listOfLists[1])
	thirdFold.extend(listOfLists[2])

def chunkify(species, nFolds):
	return [species[i::nFolds] for i in range(nFolds)]

def xCrossValidation(firstFold, secondFold, thirdFold, case, trainingSet=[], testSet=[]):
	trainingSet.clear()
	testSet.clear()
	if case == 1:
		for x in range(len(firstFold)):
			testSet.append(firstFold[x])
		for x in range(len(secondFold)):
			trainingSet.append(secondFold[x])
		for x in range(len(thirdFold)):
			trainingSet.append(thirdFold[x]),
	elif case == 2:
		for x in range(len(secondFold)):
			testSet.append(secondFold[x])
		for x in range(len(firstFold)):
			trainingSet.append(firstFold[x])
		for x in range(len(thirdFold)):
			trainingSet.append(thirdFold[x]),
	elif case == 3:
		for x in range(len(thirdFold)):
			testSet.append(thirdFold[x])
		for x in range(len(firstFold)):
			trainingSet.append(firstFold[x])
		for x in range(len(secondFold)):
			trainingSet.append(secondFold[x])

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

def normalize(dataSet=[]):
	for x in range(len(dataSet)):
		for y in range(len(dataSet[x])-1):
		 	dataSet[x][y] = (dataSet[x][y] - min(list([i[y] for i in dataSet]))) / (max(list([i[y] for i in dataSet])) - min(list([i[y] for i in dataSet])))

def main(fileName, distanceMethod, kNeighbors, isNormalized):
	# prepare data
	fullSet = []
	loadDataset(fileName, fullSet)
	columns = np.shape(fullSet)[1]
	species = set([i[columns-1] for i in fullSet])

	firstFold=[]
	secondFold=[]
	thirdFold=[]
	#create 3 folds with randomly picked up sets from specific species
	kFold(fullSet, species, firstFold, secondFold, thirdFold)

	#create trainingSet and testSet based on cross validation rule 1,2,3
	#2 + 3 = trainingSet, 1 - testSet
	#1 + 3 = trainingSet, 2 - testSet
	#1 + 2 = trainingSet, 3 - testSet

	distanceMethods = (euclideanDistance, manhattanDistance, chybeshevDistance)
	for distanceMethod in distanceMethods:
		print('Method name: ' + repr(distanceMethod))
		for kNeighbor in kNeighbors:
			print('Neighbours: ' + repr(kNeighbor))
			totalAccuracy = 0
			for case in range(1, 4):
				#create trainingSet and testSet
				trainingSet=[]
				testSet=[]
				xCrossValidation(firstFold, secondFold, thirdFold, case, trainingSet, testSet)
				#normalize sets
				if isNormalized == 1:
					normalize(trainingSet)
					normalize(testSet)

				predictions=[]
				for x in range(len(testSet)):
					neighbors = getNeighbors(distanceMethod, trainingSet, testSet[x], kNeighbor)
					result = getResponse(neighbors)
					predictions.append(result)
					#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
				accuracy = getAccuracy(testSet, predictions)
				totalAccuracy += accuracy
				print('Accuracy: ' + repr(accuracy) + '%')
			print('Total Accuracy:' + repr(totalAccuracy/3) + '%')

# MAIN FUNCTION CALL
# $1 - filename
# $2 - metric distanceMethod
# $3 - n-neighbours
# $4 - normalize dataSet ? (true or false)
kNeighbors = [1,3,5,10];
main(sys.argv[1], euclideanDistance, kNeighbors, int(sys.argv[2]))
