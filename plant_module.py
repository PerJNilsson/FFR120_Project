import numpy as np
from numpy.random import randint

class Plant:
    maxNumberOfCharges = 10

    def __init__(self, cluster):
        self.charges = maxNumberOfCharges
        self.cluster = cluster

    def eaten(self):
        if self.charges > 0:
            self.charges -= 1
        if self.charges == 0:
            self.cluster.decrement()
            return True
        return False


class PlantCluster:
    spawnRate = 0.025  # The probability of generating a new cluster for each generation
    distributionParameter = 20  # A higher value will tend to create the clusters more evenly spread.
    # In the limit that the parameter is 1 the clusters will spawn completely random.
    size = 150  # The amount of plants per cluster (SHOULD THIS BE THE UPPER LIMIT OR MEAN?!?!?!?!?!)
    standardDeviation = 7  # The standard deviation used to generate the plants which make up the cluster.

    def initialize(latticeLength=None):
        if latticeLength:
            PlantCluster._latticeLength = latticeLength
        PlantCluster.grid = [[None for i in range(PlantCluster._latticeLength)]
                              for j in range(PlantCluster._latticeLength)]
        PlantCluster.list = []

    def __init__(self):
        if PlantCluster.distributionParameter == 1 or not PlantCluster.list:
            self.coordinates = numpy.random.randint(0, gridSize,2)
            return

        candidateCoordinates = randint(0, gridSize, (PlantCluster.distributionParameter, 2))
        distanceToClosestCluster = numpy.zeros(PlantCluster.distributionParameter)
        for i, currentCandidateCoordinates in enumerate(candidateCoordinates):
            distanceToExistingClusters = numpy.zeros((numberOfClusters, 1))
            for j, cluster in enumerate(PlantCluster.list):
                distanceToExistingClusters[j] = np.linalg.norm(currentCandidateCoordinates - cluster.coordinates)
            distanceToClosestCluster[i] = distanceToExistingClusters.min()

        idxOfFurthestCluster = distanceToClosestCluster.argmax()
        self.coordinates = candidateCoordinates[idxOfFurthestCluster]
        self.grow()

    def decrement(self):
        if self.plants > 0:
            self.plants -= 1
        if self.plants == 0:
            PlantCluster.list.delete(self)

    def grow(self):
        candidateXCoordinates = np.round(np.random.normal(clusterObject.x, standardDeviation, [PlantCluster.size, 1]))
        candidateYCoordinates = np.round(np.random.normal(clusterObject.y, standardDeviation, [PlantCluster.size, 1]))
        candidateCoordinates = np.hstack((candidateXCoordinates, candidateYCoordinates))
        candidateCoordinates = PlantCluster.apply_boundary_conditions(candidateCoordinates)
        # uniqueCandidateCoordinates = np.unique(candidateCoordinates, axis=0)
        for coordinates in uniqueCandidateCoordinates:
            if not PlantCluster.grid[coordinates[0]][coordinates[1]]: 
                PlantCluster.grid[coordinates[0]][coordinates[1]] = Plant(self)
                self.plants += 1

    def iterate():
        r = np.random.rand()
        if r < PlantCluster.spawnRate:
            PlantCluster.list.append(PlantCluster())
        for plantCluster in PlantCluster.list:
            plantCluster.grow()

    def apply_boundary_conditions(coordinates):
        gridSize = PlantCluster._latticeLength
        coordinates[coordinates[0::1, 0] >= gridSize, 0] = coordinates[coordinates[0::1, 0] >= gridSize, 0] - gridSize
        coordinates[coordinates[0::1, 0] < 0, 0] = coordinates[coordinates[0::1, 0] < 0, 0] + gridSize
        coordinates[coordinates[0::1, 1] >= gridSize, 1] = coordinates[coordinates[0::1, 1] >= gridSize, 1]
        coordinates[coordinates[0::1, 1] < 0, 1] = coordinates[coordinates[0::1, 1] < 0, 1] + gridSize
        return coordinates


