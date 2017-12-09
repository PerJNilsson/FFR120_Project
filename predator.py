from animal import Animal
import numpy as np
from numpy.random import rand
import random

class Predator(Animal):
    maxHunger = 800  # The maximum amount of food the predator can store.

    # Example of using a parent's constructor
    def __init__(self, nLatticeLength, x=None, y=None, visibilityRadius=15, reproductionRate=0.015,child=False, randomTurnProbability=0.3):
        super().__init__(nLatticeLength, x, y,reproductionRate=reproductionRate, visibilityRadius=visibilityRadius, child=child)
        self.life = 4000
        self.randomTurnProbability = randomTurnProbability
        if child:
            self.hunger = round(Predator.maxHunger / 4)  # Children start out with semi-full hunger bar.
        else:
            self.hunger = 750  # The initial preys start out with almost full hunger bar.

        self.iterationsMovingToFood = 0  # Counts the number of iterations the prey has been moving to a certain plant.
        self.previousStep = np.random.randint(1, 4, 1)  # 1: left, 2: down, 3: right, 4: up
        # Returns coordinate of a prey to follow. If there are no prey within the
        # visibility radius it should random walk....



    def eatPrey(self, target):
        # Will eat the prey if they are on the same square
        xCoords = self.x
        yCoords = self.y
        listOfPrey = self.preys
        if xCoords == target[0] and yCoords == target[1]:
            for prey in self.preys:
                if prey.x == target[0] and prey.y == target[1]:
                    #prey._die(killed = True)
                    self.preys.remove(prey) # kills the prey, this is used instead of the modified _die() function since that caused a rare run time error.
                    self.hunger = self.maxHunger
                    self._reproduce()


    # Follow, if same point: eat.
    # Searching for prey, need visibility sphere, list of prey
    # If no prey, call random walk
    def searchPrey(self):
        # Getting the coords of the predator
        if self.hunger < 750: # If recently eaten will not move
            coordsPredator = [self.x, self.y]
            targetToChase = self.follow(self.preys, 'predator')
            if targetToChase == None:
                self._random_walk()
            else:
                self.step(targetToChase)
                self.step(targetToChase)
                self.eatPrey(targetToChase)


    def _reproduce(self):
        if self.life < 100:
            return
        r = rand()
        if r < self._reproductionRate*4:
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