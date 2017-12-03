from animal import Animal
import matplotlib.pyplot as plt

class Sheep(Animal):
    def _walk(self, x, y):
        return self._random_walk(x, y)

class Wolves(Animal):
    def _walk(self, x, y):
        return self._random_walk(x, y)


def main():
    nLatticeLength = 256
    Wolves.initialize(nLatticeLength)
    Sheep.initialize()
    [Sheep() for i in range(10)]
    [Wolves() for i in range(5)]
    plt.ioff()
    plt.show()
    plt.axis([-1, nLatticeLength, -1, nLatticeLength])
    handleSheep, = plt.plot([], [],  'or')
    handleWolves, = plt.plot([], [],  'ob')
    for i in range(1000):
        Sheep.update_handler(handleSheep)
        Sheep.iterate()
        Wolves.iterate()
        Wolves.update_handler(handleWolves)
        plt.draw()
        plt.pause(0.02)

if __name__ == "__main__":
    main()
