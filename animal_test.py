from prey import Prey
from predator import Predator
import matplotlib.pyplot as plt


def main():
    nLatticeLength = 100
    Prey.initialize(nLatticeLength, life=10000, maxHunger=10000)
    Predator.initialize(maxHunger=155)
    [Prey() for i in range(10)]
    [Predator() for i in range(50)]
    Prey.update_pointers()
    Predator.update_pointers(Prey.grid)
    plt.ioff()
    plt.show()
    plt.axis([-1, nLatticeLength, -1, nLatticeLength])
    predatorsHandle, = plt.plot([], [],  'or')
    preyHandle, = plt.plot([], [],  'ob')
    for i in range(5000):
        Prey.iterate()
        Predator.update_pointers(Prey.grid)
        Predator.iterate()
        Prey.update_handler(preyHandle)
        Predator.update_handler(predatorsHandle)
        plt.title("Prey = {}, Predators = {}".format(Prey.population,
                                                     Predator.population))
        plt.draw()
        plt.pause(0.0001)


if __name__ == "__main__":
    main()
