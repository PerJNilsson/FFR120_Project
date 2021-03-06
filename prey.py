from animal import Animal
from numpy.random import rand
import random
import numpy as np
import math

class Prey(Animal):

    maxHunger = 500# The maximum amount of food the prey can store.
    maxRestTime = 20 # The amount of turns a prey have to rest after having eaten a plant.
    maxExplorationTime = 200 # NOT SURE IF THIS IS USED ANYMORE
    maxFleeTime = 50

    # Example of using a parent's constructor
    def __init__(self, nLatticeLength, x=None, y=None,
                 followHerdProbability=0, breakFromHerdProbability=0.9, randomTurnProbability=0.4,
                 probabilityOfExploration = 1, reproductionRate = 0.08, probabilityOfDetectingPredator = 0.1, visibilityRadius=17, child=False):
        self.followHerdProbability = followHerdProbability
        self.breakFromHerdProbability = breakFromHerdProbability
        self.randomTurnProbability = randomTurnProbability
        self.probabilityOfExploration = probabilityOfExploration
        self.probabilityOfDetectingPredator = probabilityOfDetectingPredator
        super().__init__(nLatticeLength, x, y, reproductionRate=reproductionRate, visibilityRadius=visibilityRadius, child=child)
        self.life = 20000
        if child:
            self.hunger = round(Prey.maxHunger/10) # Children start out with semi-full hunger bar.
        else:
            self.hunger = Prey.maxHunger-20 # The initial preys start out with full hunger bar.

        self.plantToFollow = [] # Coordinates to the plant which are top be eaten.
        self.lastPlantEaten = [self.x, self.y] # Coordinates to the last plant eaten.
        self.iterationsMovingToFood = 0 # Counts the number of iterations the prey has been moving to a certain plant.
        self.iterationsSinceEat = 40
        self.previousStep = np.random.randint(1, 5, 1) # 1: left, 2: down, 3: right, 4: up
        self.preyToFollow = [] # Coordinates to the prey which is to be followed.
        self.restTimer = 0 # Will be used to count the number of turns a prey hase been resting (after eating).
        self.predatorToAvoid = []
        self.fleeTimer = 0 # Will be used to count the number of iterations the prey has been fleing for.
        self.alertStatus = 0 # 1: The prey has been alerted and will alert other preys.
                             # 2: The prey has been alerted and has already alerted other preys.

    def _look(self):
        self.iterationsSinceEat += 1

        # If the prey has gone in the same direction for a long time, a new direction is choosen.
        if self.lastPlantEaten:
            diffX = abs(self.lastPlantEaten[0] - self.x)
            diffY = abs(self.lastPlantEaten[1] - self.y)
            if diffX > self._latticeLength/2:
                diffX = self._latticeLength - diffX
            if diffY > self._latticeLength/2:
                diffY = self._latticeLength - diffY
            if diffX + diffY > 0.9*self._latticeLength:
                self.lastPlantEaten = [self.x, self.y]
                self.iterationsSinceEat == 0

        self.LookForPredator()
        if np.size(self.predatorToAvoid) < 2:
            if self.restTimer < 1:
                self.LookForPlant()
                if np.size(self.plantToFollow) < 2 and self.iterationsSinceEat > 5:
                    self.LookForPrey()

    def _walk(self):
        if self.fleeTimer > 0:                      #
            self.stepAway(self.predatorToAvoid)     #
            #self.stepAway(self.predatorToAvoid)
        else:
            if self.restTimer < 1:
                if self.plantToFollow:
                    self.step(self.plantToFollow)
                elif self.preyToFollow:
                    self.step(self.preyToFollow)
                else:
                    r = rand()
                    if r < self.probabilityOfExploration and self.hunger < 480 and self.lastPlantEaten: # Only explore if the food is running low.
                        self.stepAway(self.lastPlantEaten)
                    else:
                        self._random_walk()
            else:
                self.restTimer -= 1

    def _eat(self):
        # Checks if the food has been reached.
        if self.plantToFollow:
            if self.plantToFollow[0] == self.x and self.plantToFollow[1] == self.y:
                for plantObject in self.plants:
                    if plantObject.x == self.plantToFollow[0] and plantObject.y == self.plantToFollow[1]:
                        self.hunger += plantObject.foodValue  # The prey consumes the plant
                        for specificCluster in self.plantClusters:
                            if specificCluster.ID == plantObject.clusterID:
                                self.lastPlantEaten = [specificCluster.x, specificCluster.y]
                                break
                        plantObject.PlantGetsEaten()  # The plant is consumed
                        break
                self.restTimer = Prey.maxRestTime
                self.iterationsMovingToFood = 0
                self.iterationsSinceEat = 0
                self.plantToFollow = []
                self._reproduce()
                if self.hunger > Prey.maxHunger:
                    self.hunger = Prey.maxHunger

    def _die(self, killed=False):
        if self.life == 0 or self.hunger == 0:
            self.preys.remove(self)
        #if killed == True:
            #self.preys.remove(self)
        self.life -= 1
        self.hunger -= 1

    def _reproduce(self):
        if self.life < 50:
            return
        r = rand()
        if r < self._reproductionRate:
            newBorn = Prey(self._latticeLength, self.x, self.y,
                           followHerdProbability=self.followHerdProbability,
                           visibilityRadius=self._visibilityRadius, child=True)
            newBorn.update_pointers(self.preys, self.predators, self.plants, self.plantClusters)
            newBorn.lastPlantEaten=self.lastPlantEaten
            self.preys.append(newBorn)

    def LookForPlant(self):
        if np.size(self.plantToFollow)==2:
            self.iterationsMovingToFood += 1
        if self.iterationsMovingToFood > 30:
            self.plantToFollow=[]

        if np.size(self.plantToFollow) < 2 and self.hunger < 480:
            # The prey will look for new food if it has not yet seen any food or if it has been moving towards the same
            # food for a long time. A new target is choosen to avoid preys getting stuck trying to eat food which has
            # already been eaten.

            if np.size(self.plantClusters) > 0:


                # Looks at one cluster at a time. Should be faster (might be optimized further).
                clusterList = np.zeros((np.size(self.plantClusters), 1))
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
                    if clusterList[j] > self.plantClusters[j[0]].getClusterCheckRadius():
                        break
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

    def LookForPrey(self):
        if np.size(self.preyToFollow) < 2:
            r = rand()
            if r < self.followHerdProbability:
                # Look for prey to follow
                self.preyToFollow = self.follow(self.preys,'prey')

                # If a prey is followed the preferential direction of the random walk is synched.
                if self.preyToFollow and self.iterationsSinceEat > 20:
                    for specificPrey in self.preys:
                        if specificPrey.lastPlantEaten:
                            if specificPrey.x == self.preyToFollow[0] and specificPrey.y == self.preyToFollow[1]:
                                self.lastPlantEaten = specificPrey.lastPlantEaten
                                self.fleeTimer = specificPrey.fleeTimer
                                self.predatorToAvoid = specificPrey.predatorToAvoid
                                break
        else:
            r = rand()
            if (self.x == self.preyToFollow[0] and self.y == self.preyToFollow[1]) or r < self.breakFromHerdProbability:
                self.preyToFollow = []
                self.previousStep = np.random.randint(1, 5, 1)

    def LookForPredator(self):

        if self.alertStatus > 0:
            self.alertStatus -= 1

        if  self.fleeTimer > 0:
            self.fleeTimer -= 1
            if self.fleeTimer == 0:
                self.predatorToAvoid = []

        r = rand()
        if r < self.probabilityOfDetectingPredator:
            tmpVar = self.follow(self.predators, 'predator')
            if tmpVar:
                self.predatorToAvoid = tmpVar
                self.lastPlantEaten = [self.x, self.y]
                self.iterationsSinceEat == 0
                self.fleeTimer=Prey.maxFleeTime
                if self.alertStatus == 0:
                    self.alertStatus = 5
                    self.WarnOtherPrey()
                #for specificPrey in self.preys:
                #    specificPrey.alertStatus = 0 # The prey are no longer alerted

    def WarnOtherPrey(self):
        # The chance of alerting the herd has been set to the followHerdProbability ! ! !(THIS SHOULD PROBABLY HAVE ITS OWN PARAMETER)! ! !
        r = rand()
        if r < self.followHerdProbability:
        #if r < 0.7:
            # Find prey in alert radius.               ! ! !(RIGHT NOW THE VISIBILITY RADIUS IS USED)! ! !

        #possibleAlertList = []
            for specificPrey in self.preys:
                # Noticably faster than using the visibility sphere
                diffX = abs(specificPrey.x - self.x)
                diffY = abs(specificPrey.y - self.y)
                if diffX > self._latticeLength / 2:
                    diffX = self._latticeLength - diffX
                if diffY > self._latticeLength / 2:
                    diffY = self._latticeLength - diffY
                if diffX+diffY < self._visibilityRadius and diffX+diffY > 0 and specificPrey.alertStatus==0:
                    #possibleAlertList.append([objects[i].x,objects[i].y])
                    specificPrey.alertStatus = 5
                    specificPrey.predatorToAvoid = self.predatorToAvoid
                    specificPrey.lastPlantEaten = [specificPrey.x, specificPrey.y]
                    specificPrey.iterationsSinceEat == 0
                    specificPrey.fleeTimer = Prey.maxFleeTime

            #visSquare = list(self.visibility())
            #possibleAlertList = []
            #for specificPrey in self.preys:
            #    cord = (specificPrey.x, specificPrey.y)
            #    if cord in visSquare:
            #        possibleAlertList.append(cord)


            '''    
            if possibleAlertList:
                # Find the preys of found coordinates
                preysToAlert = []
                for specificCoordinates in possibleAlertList:
                    for prey in self.preys:
                        if prey.x == specificCoordinates[0] and prey.y == specificCoordinates[1] and prey.alertStatus == 0:
                            preysToAlert.append(prey)
                            prey.alertStatus = 5
                            break
                # Loop over the found prey and warns new prey
                if preysToAlert:
                    for specificPrey in preysToAlert:
                        specificPrey.predatorToAvoid = self.predatorToAvoid
                        specificPrey.lastPlantEaten = [specificPrey.x, specificPrey.y]
                        specificPrey.iterationsSinceEat == 0
                        specificPrey.fleeTimer = Prey.maxFleeTime
                        #specificPrey.WarnOtherPrey() # warn new prey (iteratively)
            '''
