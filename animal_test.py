from prey import Prey
from predator import Predator
from plant_module import PlantCluster
import matplotlib.pyplot as plt
import numpy as np

nLatticeLength = 200


def update_plant_handle(plantHandle, clusterHandle):
    # Since we don't have a list of plants we need to find them all the grid.
    # Alternatively, we implement list just for plotting.
    xPlant = []
    yPlant = []
    for i in range(nLatticeLength):
        for j in range(nLatticeLength):
            if PlantCluster.grid[i][j]:
                yPlant.append(i)
                xPlant.append(j)
    plantHandle.set_data(xPlant, yPlant)

    numberOfClusters = len(PlantCluster.list)
    xCluster = np.zeros(numberOfClusters)
    yCluster = np.zeros(numberOfClusters)
    for i, singleClusterObject in enumerate(PlantCluster.list):
        xCluster[i] = singleClusterObject.x
        yCluster[i] = singleClusterObject.y

    clusterHandle.set_data(xCluster, yCluster)


def main():
    Prey.initialize(nLatticeLength, life=10000, maxHunger=10000)
    Predator.initialize(maxHunger=155)
    PlantCluster.initialize(nLatticeLength)
    [Prey() for i in range(0)]
    [Predator() for i in range(0)]
    [PlantCluster() for i in range(4)]
    plt.ioff()
    plt.show()
    plt.axis([-1, nLatticeLength, -1, nLatticeLength])
    predatorsHandle, = plt.plot([], [],  'or')
    preyHandle, = plt.plot([], [],  'ob')
    plantHandle, = plt.plot([], [], '.', markersize=2, color=(0.3, 0.9, 0.1))
    clusterHandle, = plt.plot([], [], 'o', markersize=10, color=(0.3, 0.5, 0.7), alpha=0.5)
    for i in range(5000):
        PlantCluster.iterate()
        Prey.iterate()
        Predator.iterate()
        Prey.update_handler(preyHandle)
        Predator.update_handler(predatorsHandle)
        update_plant_handle(plantHandle, clusterHandle)
        plt.title("Prey = {}, Predators = {}".format(Prey.population,
                                                     Predator.population))
        plt.draw()
        plt.pause(0.001)


if __name__ == "__main__":
    main()
