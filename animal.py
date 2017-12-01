from numpy.random import randint, rand
import itertools
import abc
import numpy as np
import random


class Animal(abc.ABC):
    def __init__(self, latticeLength, x=None, y=None, visibilityRadius=2,
                 reproductionRate=0.005, child=False):
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
        if r < 0.2:
            self.previousStep=np.random.randint(1,4,1)

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
        visSquare = list(self.visibility())
        #3. Look around if anyone is nearby
        for object in objects:
            cord = (object.x, object.y)
            if cord in visSquare:
                possibleFollowList.append(cord)
        if(kindOfTarget=='prey'):
            possibleFollowList.remove((self.x, self.y))
        toFollow = None
        if possibleFollowList:
            toFollow = random.choice(possibleFollowList)
        return toFollow

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
            self._reproduce()
            self._die()

    def update_pointers(self, preys, predators, plants= None, plantClusters = None):
        self.preys = preys
        self.predators = predators
        self.plants = plants
        self.plantClusters = plantClusters


