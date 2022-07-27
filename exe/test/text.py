import pickle
import matplotlib.pyplot as plt

with open('a.p', 'rb') as file:
    GENOME = pickle.load(file)
    plt.scatter(list(GENOME.keys())[0], list(GENOME.keys())[1])
    plt.show()