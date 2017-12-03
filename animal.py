from collections import deque
from numpy.random import randint, rand
import matplotlib.pyplot as plt
import itertools
import utility
import abc
import numpy as np


class Animal(abc.ABC):
    animals = None
    xs = None
    ys = None

    def initialize(latticeLength):
        Animal._latticeLength = latticeLength
        Animal.animals = [[deque() for i in range(latticeLength)]
                          for j in range(latticeLength)]

    def __init__(self, x=None, y=None, visibilityRadius=2,
                 reproductionRate=0.005, child=False):
        self._child = child
        self._visibilityRadius = visibilityRadius
        self._reproductionRate = reproductionRate
        if x is None:
            x = randint(self._latticeLength)
        if y is None:
            y = randint(self._latticeLength)
        self.animals[y][x].append(self)

    def __repr__(self):
        return("Animal exists")

    def _periodic(self, value):
        return (value + self._latticeLength) % self._latticeLength

    def _visibility(self):
        radius = self._visibilityRadius
        xList = [self._periodic(self.x + i) for i in range(-radius, radius)]
        yList = [self._periodic(self.y + i) for i in range(-radius, radius)]
        return itertools.product(xList, yList)

    def step(self, targetCoord):
        def choice(difference, sizeGrid):
            if difference == 0:
                return 0
            if abs(difference) < sizeGrid / 2:
                return np.sign(difference)
            elif abs(difference) > sizeGrid / 2:
                return -1 * np.sign(difference)
            else:
                q = rand()
                if q < 0.5:
                    return 1
                else:
                    return -1
        xCoord = self.x
        yCoord = self.y

        # Check if to go right/left and up/down
        diffX = targetCoord[0] - xCoord
        diffY = targetCoord[1] - yCoord

        choices = [False, False]
        sizeGrid = self._latticeLength
        a = choice(diffX, sizeGrid)
        if a != 0:
            choices[0] = True
        b = choice(diffY, sizeGrid)
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

    def _random_walk(self, x, y):
        xTemp = x
        yTemp = y
        r = randint(1, 5)
        if (r == 1):
            xTemp += 1
        elif (r == 2):
            xTemp -= 1
        elif (r == 3):
            yTemp += 1
        elif (r == 4):
            yTemp -= 1
        return (xTemp, yTemp)

    @abc.abstractmethod
    def _walk(self, x, y):
        pass

    def _next_coordinates(self, x, y):
        (xTemp, yTemp) = self._walk(x, y)
        xTemp = utility.periodic(xTemp, Animal._latticeLength)
        yTemp = utility.periodic(yTemp, Animal._latticeLength)
        return (xTemp, yTemp)

    def iterate():
        Animal.xs = deque()
        Animal.ys = deque()
        newAnimals = [[deque() for i in range(Animal._latticeLength)]
                          for j in range(Animal._latticeLength)]
        for y in range(Animal._latticeLength):
            for x in range(Animal._latticeLength):
                for elem in Animal.animals[y][x]:
                    xTemp, yTemp = elem._next_coordinates(x, y)
                    newAnimals[yTemp][xTemp].append(elem)
                    (Animal.xs).append(x)
                    (Animal.ys).append(y)
        Animal.animals = newAnimals

    def update_handler(handler):
        handler.set_data(Animal.xs, Animal.ys)

