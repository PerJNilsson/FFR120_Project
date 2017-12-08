from prey import Prey
from predator import Predator
from plant_module import PlantCluster
import matplotlib.pyplot as plt


def main():
    nLatticeLength = 200
    Prey.initialize(nLatticeLength, life=10000, maxHunger=10000)
    Predator.initialize(maxHunger=155)
    PlantCluster.initialize(nLatticeLength)
    [Prey() for i in range(300)]
    [Predator() for i in range(200)]
    PlantCluster.iterate()

    plt.ioff()
    plt.show()
    plt.axis([-1, nLatticeLength, -1, nLatticeLength])
    predatorsHandle, = plt.plot([], [],  'or')
    preyHandle, = plt.plot([], [],  'ob')
    for i in range(5000):
        Prey.iterate()
        Predator.iterate()
        Prey.update_handler(preyHandle)
        Predator.update_handler(predatorsHandle)
        plt.title("Prey = {}, Predators = {}".format(Prey.population,
                                                     Predator.population))
        plt.draw()
        plt.pause(0.001)


if __name__ == "__main__":
    main()
