# from predator import Predator
from prey import Prey
from predator import Predator
import matplotlib.pyplot as plt
import numpy as np
import plant_module
import math



def plot(animals, predators, plantObjects, clusterObjects, preyPlotHandle, plantPlotHandle, clusterPlotHandle,
        predatorsPlotHandle):
    numberOfAnimals = len(animals)
    xPrey = np.zeros(numberOfAnimals)
    yPrey = np.zeros(numberOfAnimals)
    for i, animal in enumerate(animals):
        xPrey[i] = animal.x
        yPrey[i] = animal.y

    numberOfPredators = len(predators)
    xPredator = np.zeros(numberOfPredators)
    yPredator = np.zeros(numberOfPredators)
    for i, predator in enumerate(predators):
        xPredator[i] = predator.x
        yPredator[i] = predator.y

    numberOfPlants = len(plantObjects)
    xPlant = np.zeros(numberOfPlants)
    yPlant = np.zeros(numberOfPlants)
    for i, singlePlantObject in enumerate(plantObjects):
        xPlant[i] = singlePlantObject.x
        yPlant[i] = singlePlantObject.y

    numberOfClusters = len(clusterObjects)
    xCluster = np.zeros(numberOfClusters)
    yCluster = np.zeros(numberOfClusters)
    for i, singleClusterObject in enumerate(clusterObjects):
        xCluster[i] = singleClusterObject.x
        yCluster[i] = singleClusterObject.y

    preyPlotHandle.set_data(xPrey, yPrey)
    predatorsPlotHandle.set_data(xPredator, yPredator)
    plantPlotHandle.set_data(xPlant, yPlant)
    clusterPlotHandle.set_data(xCluster, yCluster)
    plt.draw()
    plt.pause(0.00001)

def main():

    '''
    initialNumberOfPreys = 1
    initialNumberOfClusters = 2
    gridSize = 10
    clusterSpawnRate = 0.005  # The probability of generating a new cluster for each generation
    clusterDistributionParameter = 20  # A higher value will tend to create the clusters more evenly spread.
    # In the limit that the parameter is 1 the clusters will spawn completely random.
    clusterSizeParameter = 1  # The amount of plants per cluster (SHOULD THIS BE THE UPPER LIMIT OR MEAN?!?!?!?!?!)
    clusterStandardDeviation = 1  # The standard deviation used to generate the plants which make up the cluster.
    '''


    initialNumberOfPreys = 200
    initialNumberOfPredators = 5
    initialNumberOfClusters = 3
    gridSize = 150
    clusterSpawnRate = 0.005  # The probability of generating a new cluster for each generation
    clusterDistributionParameter = 20  # A higher value will tend to create the clusters more evenly spread.
    # In the limit that the parameter is 1 the clusters will spawn completely random.
    clusterSizeParameter = 100  # The amount of plants per cluster (SHOULD THIS BE THE UPPER LIMIT OR MEAN?!?!?!?!?!)
    clusterStandardDeviation = 8  # The standard deviation used to generate the plants which make up the cluster.


    # Initializes "graphics"
    plt.ioff()
    plt.show()
    plt.axis([-1, gridSize, -1, gridSize])
    preyPlotHandle      = plt.plot([], [], '.', markersize = 3 , color = (0.2, 0.3, 0.8))[0]
    predatorsPlotHandle = plt.plot([], [], '.', markersize = 5 , color = (0.9, 0.1, 0.1))[0]
    plantPlotHandle     = plt.plot([], [], '.', markersize = 2 , color = (0.3, 0.9, 0.1))[0]
    clusterPlotHandle   = plt.plot([], [], 'o', markersize = 10, color = (0.3, 0.5, 0.7), alpha = 0.5)[0]

    clusterObjects, plantObjects=plant_module.InitializePlants(initialNumberOfClusters, gridSize, clusterDistributionParameter, clusterSizeParameter,
                     clusterStandardDeviation)
    clusterObjects[0].setClusterCheckRadius(clusterStandardDeviation * math.sqrt(-2 * math.log(0.001 * clusterStandardDeviation * math.sqrt(2 * math.pi)))+40)
    print(clusterStandardDeviation * math.sqrt(-2 * math.log(0.001 * clusterStandardDeviation * math.sqrt(2 * math.pi)))+40)

    preys = [Prey(gridSize) for i in range(initialNumberOfPreys)]
    #predators = [Predator(gridSize) for j in range(initialNumberOfPredators)]
    predators = []
    for prey in preys:
        prey.update_pointers(preys, predators, plantObjects, clusterObjects)
    #for predator in predators:
    #    predator.update_pointers(preys, predators)

    i=0
    while preys:
        i+=1
        clusterObjects, plantObjects = plant_module.PlantGrowth(clusterObjects, plantObjects, gridSize,
                                                                clusterSpawnRate,
                                                                clusterDistributionParameter, clusterSizeParameter,
                                                                clusterStandardDeviation)

        if np.size(clusterObjects)==1:
            plantObjects[0].UpdatePointers(plantObjects, clusterObjects)  # Needed when new plants grow when before there
            for prey in preys:                                            # were no plants. Without this code the preys
                prey.update_pointers(preys, predators, plantObjects, clusterObjects) # seem to lose track of the plants

        for prey in preys:
            prey()
        for predator in predators:
            predator()

        if i == 500:
            predators = [Predator(gridSize) for j in range(initialNumberOfPredators)]
            for prey in preys:
                prey.update_pointers(preys, predators, plantObjects, clusterObjects)
            for predator in predators:
                predator.update_pointers(preys, predators)

        if i%100 == 0:
            print("i = %i\n# of preys = %i\n# of plants = %i\n# of predators = %i" %(i,np.size(preys),np.size(plantObjects),np.size(predators)))
            #r = np.random.randint(0, gridSize,2)
            #print(r)
            #for prey in preys:
            #    prey.lastPlantEaten = [r[0], r[1]]
            #    prey.explorationTimer = Prey.maxExploreTime
        if i%1 == 0:
            plot(preys, predators, plantObjects, clusterObjects, preyPlotHandle, plantPlotHandle, clusterPlotHandle,
                 predatorsPlotHandle)

    print("i = %i\n# of preys = %i\n# of plants = %i\n# of predators = %i" % (
        i, np.size(preys), np.size(plantObjects), np.size(predators)))
    plot(preys, predators, plantObjects, clusterObjects, preyPlotHandle, plantPlotHandle, clusterPlotHandle,
         predatorsPlotHandle)

    # prey1 = Prey(90, 1, 1,followHerdProbability=0)
    # prey2 = Prey(90, 88, 3, followHerdProbability=0.5, visibilityRadius=6)
    # preys = [prey1, prey2]
    # for prey in preys:
    #     prey.update_pointers(preys, None)
    # for i in range(0,100):
    #     plot(preys, ax)
    #     prey2()
    #     prey1()

if __name__ == "__main__":
    main()
