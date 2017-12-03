from animal import Animal
import matplotlib.pyplot as plt

class Sheep(Animal):
    def _walk(self, x, y):
        return self._random_walk(x, y)


def main():
    nLatticeLength = 100
    Sheep.initialize(nLatticeLength)
    [Sheep() for i in range(100)]
    plt.ioff()
    plt.show()
    plt.axis([-1, nLatticeLength, -1, nLatticeLength])
    handle, = plt.plot([], [],  'o')
    for i in range(1000):
        Sheep.iterate()
        Sheep.update_handler(handle)
        plt.draw()
        plt.pause(0.02)

if __name__ == "__main__":
    main()

