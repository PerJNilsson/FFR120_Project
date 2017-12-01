import plant_module
import numpy
import matplotlib.pyplot as plt

#
# This file contains some "tests" of the PlantCluster and Plant classes.
# The choice has been made to use the class name Plant instead of Food since food is very general and doesn't just include plants.
# The code might not follow the coding standard well, this shall be changed later on.
#


# Parameters
N=1000
gridSize=300
clusterSpawnRate=0.025 # The probability of generating a new cluster for each generation
clusterDistributionParameter=20 # A higher value will tend to create the clusters more evenly spread.
                                # In the limit that the parameter is 1 the clusters will spawn completely random.
clusterSizeParameter=50 #The amount of plants per cluster (SHOULD THIS BE THE UPPER LIMIT OR MEAN?!?!?!?!?!)
clusterStandardDeviation=7 # The standard deviation used to generate the plants which make up the cluster.


# initializeation
clusterObjects = []
plantObjects = []
clusterHistogram=numpy.zeros((N,1))
plantHistogram=numpy.zeros((N,1))


# Setup for the animation
plt.figure(1)
plt.axis([0, gridSize, 0, gridSize])
plantPlot=plt.plot([], [], '.', markersize=2, color=(0.6, 0.1, 0.1))
clusterPlot=plt.plot([], [], 'o', markersize=clusterStandardDeviation * 2 + 7,
         color=(0.3, 0.5, 0.7), alpha=0.5)


# Simulation loop
for j in range(0, N, 1):
    #
    clusterObjects, plantObjects=plant_module.PlantGrowth(clusterObjects, plantObjects, gridSize, clusterSpawnRate,
                                            clusterDistributionParameter,clusterSizeParameter,clusterStandardDeviation)
    if numpy.size(clusterObjects)!=0:
        # Performs the eating step, in this case a random plant is eaten in each step (This should not be the case
        #                                                                              in the "real" simulation)
        indexOfEatenPlant = numpy.random.randint(0, plantObjects[0].numberOfPlants, 1)
        plantObjects, clusterObjects = plant_module.PlantGetsEaten(plantObjects, clusterObjects, indexOfEatenPlant[0])

        # Updates the histograms.
        if numpy.size(clusterObjects)!=0:
            clusterHistogram[j] = clusterObjects[0].numberOfPlantClusters
            plantHistogram[j] = plantObjects[0].numberOfPlants
        else:
            plantHistogram[j] = 0

    # Updates the animation objects
    if numpy.size(clusterObjects) != 0:
        plotDataCluster = numpy.zeros((clusterObjects[0].numberOfPlantClusters, 2))
        for i in range(0, clusterObjects[0].numberOfPlantClusters, 1):
            plotDataCluster[i, 0] = clusterObjects[i].xCoordinate
            plotDataCluster[i, 1] = clusterObjects[i].yCoordinate
        plotData = numpy.zeros((plantObjects[0].numberOfPlants, 2))
        for i in range(0, plantObjects[0].numberOfPlants, 1):
            plotData[i, 0] = plantObjects[i].xCoordinate
            plotData[i, 1] = plantObjects[i].yCoordinate
        plt.setp(plantPlot, xdata=plotData[0::1, 0], ydata=plotData[0::1, 1])
        plt.setp(clusterPlot, xdata=plotDataCluster[0::1, 0], ydata=plotDataCluster[0::1, 1])
    else:
        plt.setp(plantPlot, xdata=[], ydata=[])
        plt.setp(clusterPlot, xdata=[], ydata=[])
    plt.draw()
    plt.pause(0.00001)


if numpy.size(clusterObjects)!=0:
    print("number of clusters = %i" %clusterObjects[0].numberOfPlantClusters)
    print("Number of plants = %i\n" %plantObjects[0].numberOfPlants)
    meanNumberOfPlantsPerCluster=plantObjects[0].numberOfPlants/clusterObjects[0].numberOfPlantClusters
    print("Average number of plants per cluster = %f\n" %meanNumberOfPlantsPerCluster)


# Creates the 2 histogram plots
plt.figure(2)
plt.plot(range(0,N,1),clusterHistogram)
plt.ylabel('NUMBER OF CLUSTERS')
plt.xlabel('ITERATION')
plt.draw()

plt.figure(3)
plt.plot(range(0,N,1),plantHistogram)
plt.ylabel('NUMBER OF PLANTS')
plt.xlabel('ITERATION')
plt.show()



