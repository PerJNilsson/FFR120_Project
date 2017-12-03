from prey import Prey
import matplotlib.pyplot as plt


def main():
    nLatticeLength = 100
    Prey.initialize(nLatticeLength)
    [Prey() for i in range(10)]
    Prey.update_pointers()
    plt.ioff()
    plt.show()
    plt.axis([-1, nLatticeLength, -1, nLatticeLength])
    preyHandle, = plt.plot([], [],  'or')
    for i in range(5000):
        Prey.iterate()
        Prey.update_handler(preyHandle)
        plt.draw()
        plt.pause(0.0001)


if __name__ == "__main__":
    main()
