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
    numberOfRuns = 5
    maximumLengthOfRun = 30000

    initialNumberOfPreys = 400
    initialNumberOfPredators = 10
    initialNumberOfClusters = 30
    gridSize = 512
    clusterSpawnRate = 0.02  # The probability of generating a new cluster for each generation
    clusterDistributionParameter = 40  # A higher value will tend to create the clusters more evenly spread.
    # In the limit that the parameter is 1 the clusters will spawn completely random.
    clusterSizeParameter = 30  # The amount of plants per cluster (SHOULD THIS BE THE UPPER LIMIT OR MEAN?!?!?!?!?!)
    clusterStandardDeviation = 9  # The standard deviation used to generate the plants which make up the cluster.


    # Initializes "graphics"
    plt.ioff()
    plt.show()
    plt.axis([-1, gridSize, -1, gridSize])
    preyPlotHandle      = plt.plot([], [], '.', markersize = 3 , color = (0.2, 0.3, 0.8))[0]
    predatorsPlotHandle = plt.plot([], [], '.', markersize = 5 , color = (0.9, 0.1, 0.1))[0]
    plantPlotHandle     = plt.plot([], [], '.', markersize = 2 , color = (0.3, 0.9, 0.1))[0]
    clusterPlotHandle   = plt.plot([], [], 'o', markersize = 10, color = (0.3, 0.5, 0.7), alpha = 0.5)[0]


    file = open("run_data", "w")
    file.write("Initial number of preys = %i \n" %initialNumberOfPreys)
    file.write("Initial number of predators = %i \n" %initialNumberOfPredators)
    file.write("Initial number of plant clusters = %i \n" %initialNumberOfClusters)
    file.write("Grid size = %i \n" % gridSize)
    file.write("cluster spawn rate = %f \n" %clusterSpawnRate)
    file.write("cluster distribution parameter = %i \n" %clusterDistributionParameter)
    file.write("cluster size parameter = %i \n" % clusterSizeParameter)
    file.write("cluster standard deviation %f \n" %clusterStandardDeviation)


    for iRun in range(0,numberOfRuns,1):
        file.write("\n========================================================== \n")
        clusterObjects, plantObjects = plant_module.InitializePlants(initialNumberOfClusters, gridSize,
                                                                     clusterDistributionParameter, clusterSizeParameter,
                                                                     clusterStandardDeviation)
        clusterObjects[0].setClusterCheckRadius(clusterStandardDeviation * math.sqrt(
            -2 * math.log(0.001 * clusterStandardDeviation * math.sqrt(2 * math.pi))) + 40)

        preys = [Prey(gridSize, visibilityRadius = 27, reproductionRate = 0.1) for i in range(initialNumberOfPreys)]
        predators = [Predator(gridSize, visibilityRadius = 22, reproductionRate = 0.2) for j in
                     range(initialNumberOfPredators)]
        for prey in preys:
            prey.update_pointers(preys, predators, plantObjects, clusterObjects)
        for predator in predators:
            predator.update_pointers(preys, predators)

        number_of_preys = []
        number_of_predators = []
        number_of_plants = []
        number_of_preys.append(np.size(preys))
        number_of_predators.append(10*np.size(predators))
        number_of_plants.append(np.size(plantObjects))
        i=0
        while preys and predators and i < maximumLengthOfRun:
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
            plt.title("Prey = {}, Predators = {}, Iteration = {}".format(np.size(preys),
                                                     np.size(predators),i))

            #if i%100 == 0:
            #    print("i = %i\n# of preys = %i\n# of plants = %i\n# of predators = %i" %(i,np.size(preys),np.size(plantObjects),np.size(predators)))
            #if i%1 == 0:
            #    plt.axis([-1, gridSize, -1, gridSize])
            #    plot(preys, predators, plantObjects, clusterObjects, preyPlotHandle, plantPlotHandle, clusterPlotHandle,
            #         predatorsPlotHandle)
            #    plt.savefig('pictures/pic{:04}.png'.format(i), format='png')
            number_of_preys.append(np.size(preys))
            number_of_predators.append(10*np.size(predators))
            number_of_plants.append(np.size(plantObjects))

        plt.figure(2+iRun)
        tmpList=[max(number_of_plants), max(number_of_preys), max(number_of_predators)]
        plt.axis([0, i, 0, max(tmpList)])
        plt.plot(range(0, i+1), number_of_plants, 'g')
        plt.plot(range(0, i + 1), number_of_preys, 'b')
        plt.plot(range(0,i+1), number_of_predators, 'r')
        plt.title("iRun = %i" %iRun)
        plt.savefig('pictures/aBlood{:04}.png'.format(iRun), format='png')
        #plt.show()

        # Save to text file here
        file.write("Iterations passed = %i\n" %i)
        file.write("number of preys = %i\n" %np.size(preys))
        file.write("number of predators = %i\n" %np.size(predators))
        file.write("number of plant clusters = %i\n" %np.size(clusterObjects))
        file.write("number of plants = %i\n" %np.size(plantObjects))

        print("Run number %i complete\n" %(iRun+1))
        print("i = %i\n# of preys = %i\n# of plants = %i\n# of predators = %i" %(i,np.size(preys),np.size(plantObjects),np.size(predators)))

        # Awful way of deleting all the plants/clusters between runs
        i = 1
        while i > 0:
            for plant in plantObjects:
                plant.PlantGetsEaten()
            i = np.size(plantObjects)

    file.close()
    print("All runs are done")

if __name__ == "__main__":
    main()
