from animal import Animal
import matplotlib.pyplot as plt

class Sheep(Animal):
    def _walk(self, x, y):
        return self._random_walk(x, y)


def main():
    nLatticeLength = 100
    Sheep.initialize(nLatticeLength)
    [Sheep() for i in range(100)]
    handle, = plt.plot([], [],  'o')
    plt.show()
    plt.set_xlimit(0, nLatticeLength)
    plt.set_ylimit(0, nLatticeLength)
    for i in range(1000):
        Sheep.iterate()
        Sheep.update_handler(handle)
        plt.draw()
        plt.pause(0.02)

if __name__ == "__main__":
    main()

