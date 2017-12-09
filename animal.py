from numpy.random import randint, rand
import itertools
import abc
import numpy as np
import random


class Animal(abc.ABC):
    def __init__(self, latticeLength, x=None, y=None, visibilityRadius=2,
                 reproductionRate=0.05, child=False):
        self.child = child
        self._latticeLength = latticeLength
        self._visibilityRadius = visibilityRadius
        self._reproductionRate = reproductionRate
        if x is None:
            self.x = randint(latticeLength)
        else:
            self.x = x
        if y is None:
            self.y = randint(latticeLength)
        else:
            self.y = y

    def __repr__(self):
        return("Animal is at x = {}, y = {}".format(self.x, self.y))

    def _periodic(self, value):
        return (value + self._latticeLength) % self._latticeLength

    def visibility(self):
        radius = self._visibilityRadius
        xList = [self._periodic(self.x + i) for i in range(-radius, radius)]
        yList = [self._periodic(self.y + i) for i in range(-radius, radius)]
        return itertools.product(xList, yList)

        # Takes a target coordinate and move towards it. If the target coordinate is an empty list
        # the function will call random walk.
    def step(self, targetCoord):
        def choise(difference, sizeGrid):
            if difference == 0:
                return 0
            if abs(difference) < sizeGrid/2:
                return np.sign(difference)
            elif abs(difference) > sizeGrid/2:
                return -1*np.sign(difference)
            else:
                q = rand()
                if q < 0.5:
                    return 1
                else:
                    return -1

        xCoord = self.x
        yCoord = self.y

        # Check if to go right/left and up/down
        diffX = targetCoord[0]-xCoord
        diffY = targetCoord[1]-yCoord

        choices = [False, False]
        sizeGrid = self._latticeLength
        a = choise(diffX, sizeGrid)
        if a != 0:
            choices[0] = True
        b = choise(diffY, sizeGrid)
        if b != 0:
            choices[1] = True

        if sum(choices) == 0:
            return
        result = randint(sum(choices))
        if result == 1:
            self.y += b
        elif choices[0]:
            self.x += a
        else:
            self.y += b


    def stepAway(self, targetCoord):
        def choise(difference, sizeGrid):
            if difference == 0:
                q = rand()
                if q < 0.5:
                    return 1
                else:
                    return -1
                #return 0
            if abs(difference) < sizeGrid/2:
                return np.sign(difference)
            elif abs(difference) > sizeGrid/2:
                return -1*np.sign(difference)
            else:
                q = rand()
                if q < 0.5:
                    return 1
                else:
                    return -1

        xCoord = self.x
        yCoord = self.y

        # Check if to go right/left and up/down
        diffX = targetCoord[0]-xCoord
        diffY = targetCoord[1]-yCoord

        choices = [False, False]
        sizeGrid = self._latticeLength
        a = choise(diffX, sizeGrid)
        if a != 0:
            choices[0] = True
        b = choise(diffY, sizeGrid)
        if b != 0:
            choices[1] = True

        if sum(choices) == 0:
            r = rand()
            q = rand() - 0.5
            if r < 0.5:
                self.x = self.x + np.sign(q)
            else:
                self.y = self.y + np.sign(q)
            return
        result = randint(sum(choices))
        if result == 1:
            self.y -= b
        elif choices[0]:
            self.x -= a
        else:
            self.y -= b



    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = self._periodic(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = self._periodic(value)

    def _random_walk(self):

        r = rand()
        if r < self.randomTurnProbability: # Checks if the agent should change direction.
            self.previousStep = np.random.randint(1, 5, 1)

        if self.previousStep == 1:
            self.x = self.x - 1
        elif self.previousStep == 2:
            self.y = self.y - 1
        elif self.previousStep == 3:
            self.x = self.x + 1
        elif self.previousStep == 4:
            self.y = self.y + 1

    def follow(self, objects, kindOfTarget):
        possibleFollowList = []
        sizeGrid = self._latticeLength
        #1. Get position of the prey
        tmpVar = [self.x, self.y]
        #2. Get the visibility sphere
        #if kindOfTarget == 'prey':
        #    visSquare = list(self.visibility())
            #------------------------------------------
        #3. Look around if anyone is nearby

        possibleFollowList = []
        for i in range(0, np.size(objects), 1):
            # Noticably faster than using the visibility sphere
            diffX = abs(objects[i].x - self.x)
            diffY = abs(objects[i].y - self.y)
            if diffX > self._latticeLength / 2:
                diffX = self._latticeLength - diffX
            if diffY > self._latticeLength / 2:
                diffY = self._latticeLength - diffY
            if diffX+diffY < self._visibilityRadius and diffX+diffY > 0:
                possibleFollowList.append([objects[i].x,objects[i].y])

        toFollow = None
        if(kindOfTarget=='prey') or (kindOfTarget == 'predator'):
            if possibleFollowList:
                distanceList = np.zeros((len(possibleFollowList), 1))
                for i in range(0,len(possibleFollowList),1):
                    diffX = abs(possibleFollowList[i][0] - self.x)
                    diffY = abs(possibleFollowList[i][1] - self.y)
                    if diffX > self._latticeLength / 2:
                        diffX = self._latticeLength - diffX
                    if diffY > self._latticeLength / 2:
                        diffY = self._latticeLength - diffY
                    distanceList[i, 0] = diffX + diffY
                # Finds the order of the preys (according to proximity to the searching prey)
                preySortedIndeces = np.argsort(distanceList, kind='quicksort', axis=0)
                if kindOfTarget == 'prey':
                    toFollow = possibleFollowList[preySortedIndeces[-1, 0]] # Pick prey furthest away.
                else:
                    toFollow = possibleFollowList[preySortedIndeces[0, 0]]  # Pick prey closest.
                #toFollow = random.choice(possibleFollowList)  # Pick random prey.
        elif(kindOfTarget=='plant'):
            if possibleFollowList:
                toFollow = random.choice(possibleFollowList) # Pick random plant.
        return toFollow
        #if len(possibleFollowList) == 0: # If there are no other prey nearby
        #		prey.randomWalk or whatever. This shouldnot be implemented here



    @abc.abstractmethod
    def _look(self):
        pass

    @abc.abstractmethod
    def _walk(self):
        pass

    @abc.abstractmethod
    def _eat(self):
        pass

    @abc.abstractmethod
    def _reproduce(self):
        pass

    @abc.abstractmethod
    def _die(self):
        pass

    def __call__(self):
        if self.child:
            self.child = False
        else:
            self._look()
            self._walk()
            self._eat()
            #self._reproduce()
            self._die()

    def update_pointers(self, preys, predators, plants=[], plantClusters=[]):
        self.preys = preys
        self.predators = predators
        self.plants = plants
        self.plantClusters = plantClusters
