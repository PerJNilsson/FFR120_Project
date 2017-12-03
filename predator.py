from animal import Animal
import numpy as np

class Predator(Animal):
    def __init__(self, x=None, y=None, visibilityRadius=20, child=False):
        super().__init__(x, y, visibilityRadius, child=child)
        self.iterationsMovingToFood = 0
        self.previousStep = np.random.randint(1, 4, 1)

    def update_pointers(preys):
        Predator.preys = preys

    def _eat(self, x, y):
        if Predator.preys[y][x]:
            Predator.preys[y][x].pop()
            Predator.hunger = Predator.maxHunger

    def _walk(self, x, y):
        if self.hunger > 150:
            return (x, y)
        targetToChase = self._follow(x, y, self.preys)
        if targetToChase:
            x, y = self._step(x, y, targetToChase)
            self._step(x, y, targetToChase)
        return self._random_walk(x, y)

    def _create_child(self, x, y):
        return Predator(x, y, self._visibilityRadius, child=True)
