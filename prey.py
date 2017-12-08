import animal
import predator
import plant_module
from numpy.random import rand
import numpy as np
from plant_module import Plant


class Prey(animal.Animal):

    def __init__(self, x=None, y=None,
                 followHerdProbability=0.2, visibilityRadius=10, child=False):
        self._followHerdProbability = followHerdProbability
        super().__init__(x, y, visibilityRadius, child=child)
        self.plantToFollow = []
        self.iterationsMovingToFood = 0
        self.previousStep = np.random.randint(1, 4, 1)

    def _predator_found(self, x, y):
        return self._follow(x, y, predator.Predator.grid)

    def _walk(self, x, y):
        predatorCoordinates = self._predator_found(x, y)
        if predatorCoordinates:
            return self._step(x, y, predatorCoordinates, reverse=True)
        r = rand()
        if r < self._followHerdProbability:
            coordinates = self._follow(x, y, Prey.grid, reverse=True)
            if coordinates:
                return self._step(x, y, coordinates)
        return self._random_walk(x, y)

    def _eat(self, x, y):
        plant = plant_module.PlantCluster.grid[y][x]
        if plant:
            self.hunger += plant.foodValue 
            if plant.eaten():
                plant_module.PlantCluster.grid[y][x] = None
            if self.hunger > Prey.maxHunger:
                self.hunger = Prey.maxHunger

    def _create_child(self, x, y):
        return Prey(x, y, self._followHerdProbability, self._visibilityRadius,
                    child=True)

    # def LookForPlant(self):
    #    if np.size(self.plantToFollow) == 2:
    #        self.iterationsMovingToFood += 1

    #    if (np.size(self.plantToFollow) == 0 or self.iterationsMovingToFood > 30) and self.hunger < 90:
    #        # The prey will look for new food if it has not yet seen any food or if it has been moving towards the same
    #        # food for a long time. A new target is choosen to avoid preys getting stuck trying to eat food which has
    #        # already been eaten. The prey do not look for food if it's hunger bar is almost full.

    #        # Looks at one cluster at a time. Should be faster (might be optimized further).
    #        clusterList = np.zeros(
    #            (self.plantClusters[0].numberOfPlantClusters, 1))
    #        for i in range(0, self.plantClusters[0].numberOfPlantClusters, 1):
    #            diffX = abs(self.plantClusters[i].x - self.x)
    #            diffY = abs(self.plantClusters[i].y - self.y)
    #            if diffX > self._latticeLength / 2:
    #                diffX = self._latticeLength - diffX
    #            if diffY > self._latticeLength / 2:
    #                diffY = self._latticeLength - diffY
    #            clusterList[i, 0] = diffX + diffY
    #        # Finds the order of the clusters (according to proximity to prey)
    #        clusterSortedIndeces = np.argsort(
    #            clusterList, kind='quicksort', axis=0)
    #        for i in range(0, self.plantClusters[0].numberOfPlantClusters, 1):
    #            j = clusterSortedIndeces[i]
    #            tmpList = []
    #            currentClusterID = self.plantClusters[j[0]].ID
    #            for plantObject in self.plants:
    #                if(plantObject.clusterID == currentClusterID):
    #                    tmpList.append(plantObject)
    #                else:
    #                    if (plantObject.clusterID > currentClusterID):
    #                        break
    #            self.plantToFollow = self.follow(tmpList, 'plant')
    #            if self.plantToFollow:
    #                break

    #        # Looks at all plants at a time.
    #        #self.plantToFollow = self.follow(self.plants, 'plant')
    #        self.iterationsMovingToFood = 0
