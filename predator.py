from animal import Animal
import numpy as np
from numpy.random import rand
import random

class Predator(Animal):
    maxHunger = 200  # The maximum amount of food the predator can store.

    # Example of using a parent's constructor
    def __init__(self, nLatticeLength, x=None, y=None, visibilityRadius=20, child=False):
        super().__init__(nLatticeLength, x, y, visibilityRadius, child=child)
        self.life = 4000
        if child:
            self.hunger = round(Predator.maxHunger / 4)  # Children start out with semi-full hunger bar.
        else:
            self.hunger = 150  # The initial preys start out with full hunger bar.

        self.iterationsMovingToFood = 0  # Counts the number of iterations the prey has been moving to a certain plant.
        self.previousStep = np.random.randint(1, 4, 1)  # 1: left, 2: down, 3: right, 4: up
        # Returns coordinate of a prey to follow. If there are no prey within the
        # visibility radius it should random walk....



    def _eat(self, x, y):
        # Will eat the prey if they are on the same square

        #  Now want to check if a prey is on the same point, if they are it should die
        if Predator.preyMatrix[y][x]:
            Predator.preyMatrix.pop()
            Predator.hunger = Predator.maxHunger


    #  Follow, if same point: eat.
    #  Searching for prey, need visibility sphere, list of prey
    #  If no prey, call random walk
    def searchPrey(self, x, y):
        # Getting the coords of the predator
        if self.hunger < 150:  # If recently eaten, predator will not move
            targetToChase = self._follow(x, y, self.prey)
            if targetToChase == None:
                self._random_walk
            else:
                self._step(targetToChase)
                self._step(targetToChase)
                self.eatPrey(targetToChase)


    def _reproduce(self):
        if self.life < 100:
            return
        r = rand()
        if r < self._reproductionRate:
            newBorn = Predator(self._latticeLength, self.x, self.y,
                           visibilityRadius=self._visibilityRadius, child=True)
            newBorn.update_pointers(self.preys, self.predators)
            self.predators.append(newBorn)
    def _walk(self):
        self.searchPrey()
    def _eat(self):
        pass
    def _look(self):
        pass

    def _die(self):
        if self.life == 0 or self.hunger == 0:
            self.predators.remove(self)
        self.life -= 1
        self.hunger -= 1