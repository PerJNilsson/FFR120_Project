from animal import Animal
from numpy.random import rand
import random
import numpy as np

class Prey(Animal):

    maxHunger = 100  # The maximum amount of food the prey can store.

    # Example of using a parent's constructor
    def __init__(self, nLatticeLength, x=None, y=None,
                 followHerdProbability=0.2, visibilityRadius=10, child=False):
        self.followHerdProbability = followHerdProbability
        super().__init__(nLatticeLength, x, y, visibilityRadius, child=child)
        self.life = 2000
        if child:
            self.hunger = round(Prey.maxHunger/4)  # Children start out with semi-full hunger bar.
        else:
            self.hunger = Prey.maxHunger  # The initial preys start out with full hunger bar.

        self.plantToFollow = []  # Coordinates to the plant which are top be eaten.
        self.iterationsMovingToFood = 0  # Counts the number of iterations the prey has been moving to a certain plant.
        self.previousStep=np.random.randint(1,4,1) # 1: left, 2: down, 3: right, 4: up

        # Returns coordinate of a prey to follow. If there are no prey within the
        # visibility radius it should random walk....

    def _look(self):
        pass
        #self.LookForPredator()

        #self.LookForPlant()

        #self.LookForPrey()

    def _walk(self):
        if self.plantToFollow:
            self.step(self.plantToFollow)
        else:
            r = rand()
            if r < self.followHerdProbability:
                followPrey = self.follow(self.preys,'prey')
                if followPrey:
                    self.step(followPrey)
                    #return  # Walk towards prey
                else:
                    self._random_walk()
            else:
                self._random_walk()

    def _eat(self):
        # Checks if the food has been reached.
        if self.plantToFollow:
            if self.plantToFollow[0] == self.x and self.plantToFollow[1] == self.y:
                for plantObject in self.plants:
                    if plantObject.x == self.plantToFollow[0] and plantObject.y == self.plantToFollow[1]:
                        self.hunger += plantObject.foodValue  # The prey consumes the plant
                        plantObject.PlantGetsEaten()  # The plant is consumed
                        break
                self.iterationsMovingToFood = 0
                self.plantToFollow = []
                if self.hunger > Prey.maxHunger:
                    self.hunger = Prey.maxHunger



    def _reproduce(self):
        if self.life < 50:
            return
        r = rand()
        if r < self._reproductionRate:
            newBorn = Prey(self._latticeLength, self.x, self.y,
                           followHerdProbability=self.followHerdProbability,
                           visibilityRadius=self._visibilityRadius, child=True)
            newBorn.update_pointers(self.preys, self.predators, self.plants, self.plantClusters)
            self.preys.append(newBorn)


        #if len(possibleFollowList) == 0: # If there are no other prey nearby
        #		prey.randomWalk or whatever. This shouldnot be implemented here
    def _die(self, killed = False):
        if self.life == 0 or self.hunger == 0:
            self.preys.remove(self)
        if killed == True:
            self.preys.remove(self)
        self.life -= 1
        self.hunger -= 1

    def LookForPlant(self):
        if np.size(self.plantToFollow)==2:
            self.iterationsMovingToFood += 1

        if (np.size(self.plantToFollow) == 0 or self.iterationsMovingToFood>30) and self.hunger<90:
            # The prey will look for new food if it has not yet seen any food or if it has been moving towards the same
            # food for a long time. A new target is choosen to avoid preys getting stuck trying to eat food which has
            # already been eaten. The prey do not look for food if it's hunger bar is almost full.


            # Looks at one cluster at a time. Should be faster (might be optimized further).
            clusterList = np.zeros((self.plantClusters[0].numberOfPlantClusters, 1))
            for i in range(0,self.plantClusters[0].numberOfPlantClusters,1):
                diffX = abs(self.plantClusters[i].x - self.x)
                diffY = abs(self.plantClusters[i].y - self.y)
                if diffX > self._latticeLength/2:
                    diffX = self._latticeLength-diffX
                if diffY > self._latticeLength/2:
                    diffY = self._latticeLength-diffY
                clusterList[i,0]=diffX+diffY
            # Finds the order of the clusters (according to proximity to prey)
            clusterSortedIndeces=np.argsort(clusterList,kind='quicksort',axis=0)
            for i in range(0,self.plantClusters[0].numberOfPlantClusters,1):
                j = clusterSortedIndeces[i]
                tmpList = []
                currentClusterID = self.plantClusters[j[0]].ID
                for plantObject in self.plants:
                    if(plantObject.clusterID==currentClusterID):
                        tmpList.append(plantObject)
                    else:
                        if (plantObject.clusterID > currentClusterID):
                            break
                self.plantToFollow = self.follow(tmpList, 'plant')
                if self.plantToFollow:
                    break


            # Looks at all plants at a time.
            #self.plantToFollow = self.follow(self.plants, 'plant')
            self.iterationsMovingToFood = 0


"""
        # Returns coordinate of grass. If there are no grass in visibility sphere
        # it should return a coordinate either follow another prey or random walk
        
        def searchGrass:
            possibleGrassPlace
            #1. Get position of the prey
            if grass in visibilityRadius
                possibleGrassPlace.add()

            #if len(possibleGrassPlace) == 0: This should not be implemented here
            #	walk or follow

            possibleGrassPlace = random.choice(possibleGrassPlace)
"""
    	
