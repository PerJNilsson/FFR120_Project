# from predator import Predator
from prey import Prey
from predator import Predator
import matplotlib.pyplot as plt
import numpy as np
import plant_module
import math

def main():
    numberOfRuns = 3
    maximumLengthOfRun = 5000

    initialNumberOfPreys = 400
    initialNumberOfPredators = 10
    initialNumberOfClusters = 5
    gridSize = 300
    clusterSpawnRate = 0.005  # The probability of generating a new cluster for each generation
    clusterDistributionParameter = 20  # A higher value will tend to create the clusters more evenly spread.
    # In the limit that the parameter is 1 the clusters will spawn completely random.
    clusterSizeParameter = 100  # The amount of plants per cluster (SHOULD THIS BE THE UPPER LIMIT OR MEAN?!?!?!?!?!)
    clusterStandardDeviation = 12  # The standard deviation used to generate the plants which make up the cluster.

    file = open("run_data", "w")
    file.write("Initial number of preys = %i \n" %initialNumberOfPreys)
    file.write("Initial number of predators = %i \n" %initialNumberOfPredators)
    file.write("Initial number of plant clusters = %i \n" %initialNumberOfClusters)

    for iRun in range(0,numberOfRuns,1):
        file.write("\n========================================================== \n")

        clusterObjects, plantObjects = plant_module.InitializePlants(initialNumberOfClusters, gridSize,
                                                                     clusterDistributionParameter, clusterSizeParameter,
                                                                     clusterStandardDeviation)
        clusterObjects[0].setClusterCheckRadius(clusterStandardDeviation * math.sqrt(
            -2 * math.log(0.001 * clusterStandardDeviation * math.sqrt(2 * math.pi))) + 40)

        preys = [Prey(gridSize) for i in range(initialNumberOfPreys)]
        predators = [Predator(gridSize) for j in range(initialNumberOfPredators)]
        for prey in preys:
            prey.update_pointers(preys, predators, plantObjects, clusterObjects)
        for predator in predators:
            predator.update_pointers(preys, predators)
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

        # Save to text file here
        file.write("Iterations passed = %i\n" %i)
        file.write("number of preys = %i\n" %np.size(preys))
        file.write("number of predators = %i\n" %np.size(predators))
        file.write("number of plant clusters = %i\n" %np.size(clusterObjects))
        file.write("number of plants = %i\n" %np.size(plantObjects))

        # Awful way of deleting all the plants/clusters between runs
        i = 1
        while i > 0:
            for plant in plantObjects:
                plant.PlantGetsEaten()
            i = np.size(plantObjects)

    file.close()


if __name__ == "__main__":
    main()
