from collections import deque
from numpy.random import randint, rand
import itertools
import utility
import abc
import numpy as np
import random


class Animal(abc.ABC):
    @classmethod
    def initialize(cls, latticeLength=None, maxHunger=100, life=2000):
        cls.maxHunger = maxHunger
        cls.life = life
        if latticeLength:
            Animal._latticeLength = latticeLength
        cls.grid = [[deque() for i in range(Animal._latticeLength)] for j in
                    range(Animal._latticeLength)]
        cls.xs = None
        cls.ys = None

    def __init__(self, x=None, y=None, visibilityRadius=2,
                 reproductionRate=0.005, child=False):

        self._child = child
        self._visibilityRadius = visibilityRadius
        self._reproductionRate = reproductionRate
        if x is None:
            x = randint(Animal._latticeLength)
        if y is None:
            y = randint(Animal._latticeLength)
        type(self).grid[y][x].append(self)

        if child:
            self.hunger = round(type(self).maxHunger / 4)
        else:
            self.hunger = type(self).maxHunger / 2

    def __repr__(self):
        return("Animal exists")

    def _visibility(self, x, y):
        radius = self._visibilityRadius
        xList = [utility.periodic(x + i, Animal._latticeLength) for i in
                 range(-radius, radius)]
        yList = [utility.periodic(y + i, Animal._latticeLength) for i in
                 range(-radius, radius)]
        return itertools.product(xList, yList)

    def _step(self, x, y, targetCoord):
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
        # Check if to go right/left and up/down
        diffX = targetCoord[0] - x
        diffY = targetCoord[1] - y

        choices = [False, False]
        sizeGrid = Animal._latticeLength
        a = choice(diffX, sizeGrid)
        if a != 0:
            choices[0] = True
        b = choice(diffY, sizeGrid)
        if b != 0:
            choices[1] = True

        if sum(choices) == 0:
            return (x, y)
        result = randint(sum(choices))
        if result == 1:
            y += b
        elif choices[0]:
            x += a
        else:
            y += b
        return (x, y)

    def _follow(self, x, y, objects):
        possibleFollowList = []
        #  Get the visibility sphere
        visSquare = list(self._visibility(x, y))
        #  Look around if anyone is nearby
        for xCo, yCo in visSquare:
            if xCo == x and yCo == y:
                continue
            if objects[xCo][yCo]:
                possibleFollowList.append([xCo, yCo])

        toFollow = None
        if possibleFollowList:
            toFollow = random.choice(possibleFollowList)
        return toFollow

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

    @abc.abstractmethod
    def _eat(self, x, y):
        pass

    def _die(self):
        if self.life == 0 or self.hunger == 0:
            return True
        self.life -= 1
        self.hunger -= 1

    @abc.abstractmethod
    def _create_child(self, x, y):
        pass

    def _reproduce(self):
        if self.life < 50:
            return False
        r = rand()
        if r < self._reproductionRate:
            return True
        return False

    def _next_coordinates(self, x, y):
        (xTemp, yTemp) = self._walk(x, y)
        xTemp = utility.periodic(xTemp, Animal._latticeLength)
        yTemp = utility.periodic(yTemp, Animal._latticeLength)
        return (xTemp, yTemp)

    @classmethod
    def iterate(cls):
        cls.xs = deque()
        cls.ys = deque()
        cls.population = 0
        newGrid = [[deque() for i in range(Animal._latticeLength)] for j in
                   range(Animal._latticeLength)]
        for y in range(Animal._latticeLength):
            for x in range(Animal._latticeLength):
                for elem in list(cls.grid[y][x]):
                    if elem._reproduce():
                        newGrid[y][x].append(elem._create_child(x, y))
                        (cls.xs).append(x)
                        (cls.ys).append(y)
                        cls.population += 1
                    xTemp, yTemp = elem._next_coordinates(x, y)
                    newGrid[yTemp][xTemp].append(elem)
                    elem._eat(xTemp, yTemp)
                    if elem._die():
                        continue
                    (cls.xs).append(xTemp)
                    (cls.ys).append(yTemp)
                    cls.population += 1
        cls.grid = newGrid

    @classmethod
    def update_handler(cls, handler):
        handler.set_data(cls.xs, cls.ys)
