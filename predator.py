from animal import Animal
from prey import Prey
import numpy as np


class Predator(Animal):
    hungerBeforeChase = 150
    def __init__(self, x=None, y=None, visibilityRadius=20, child=False):
        super().__init__(x, y, visibilityRadius, child=child)
        self.iterationsMovingToFood = 0
        self.previousStep = np.random.randint(1, 4, 1)

    def _eat(self, x, y):
        if self.hunger > hungerBeforeChase:
            return
        if Prey.grid[y][x]:
            Prey.grid[y][x].pop()
            self.hunger = Predator.maxHunger

    def _walk(self, x, y):
        if self.hunger > hungerBeforeChase:
            return (x, y)
        targetToChase = self._follow(x, y, Prey.grid)
        if targetToChase:
            x, y = self._step(x, y, targetToChase)
            return self._step(x, y, targetToChase)
        return self._random_walk(x, y)

    def _create_child(self, x, y):
        return Predator(x, y, self._visibilityRadius, child=True)
