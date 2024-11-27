import numpy as np
import matplotlib.pyplot as plt
from NewProjectPhase1 import *
import random


def crossover(parent1, parent2):
    child1 = City(20)
    child2 = City(20)
    random.shuffle(parent1.towers)
    random.shuffle(parent2.towers)

    pSinglePoint = 0.1
    pDoublePoint = 0.1
    pUniform = 1 - pSinglePoint - pDoublePoint
    num = RouletteWheelSelection([pSinglePoint, pDoublePoint, pUniform])

    if num == 0:  # single point crossover
        print('single point crossover')
        nVar = len(parent1.towers)
        c = np.random.randint(1, nVar)
        child1.towers = np.concatenate((parent1.towers[:c], parent2.towers[c:]))
        child2.towers = np.concatenate((parent2.towers[:c], parent1.towers[c:]))

    elif num == 1:  # double point crossover
        print('double point crossover')
        nVar = len(parent1.towers)
        cc = np.random.choice(nVar - 1, 2, replace=False)
        c1 = min(cc)
        c2 = max(cc)
        child1.towers = np.concatenate((parent1.towers[:c1], parent2.towers[c1:c2], parent1.towers[c2:]))
        child2.towers = np.concatenate((parent2.towers[:c1], parent1.towers[c1:c2], parent2.towers[c2:]))

    elif num == 2:  # uniform crossover
        print('uniform crossover')
        # alpha = np.random.randint(0, 2, size=len(parent1.towers))
        # child1.towers = [parent1.towers[i] if alpha[i] else parent2.towers[i] for i in range(len(parent1.towers))]
        # child2.towers = [parent2.towers[i] if alpha[i] else parent1.towers[i] for i in range(len(parent2.towers))]

        min_len = min(len(parent1.towers), len(parent2.towers))
        alpha = np.random.randint(0, 2, size=min_len)
        tower1 = np.empty(len(parent1.towers), dtype=type(parent1.towers[0]))
        tower2 = np.empty(len(parent2.towers), dtype=type(parent2.towers[0]))
        for i in range(len(tower1)):
            if i < min_len:
                tower1[i] = parent1.towers[i] if alpha[i] else parent2.towers[i]
            else:
                tower1[i] = parent1.towers[i]
        for i in range(len(tower2)):
            if i < min_len:
                tower2[i] = parent2.towers[i] if alpha[i] else parent1.towers[i]
            else:
                tower2[i] = parent2.towers[i]

        child1.towers = tower1
        child2.towers = tower2
    return child1, child2


def mutation(child):
    for i in range(np.random.randint(1, 10, size=1)):
        child.towers[np.random.randint(0, len(child.towers), size=1)] = Tower(
            [random.uniform(0, 19), random.uniform(0, 19)], random.randint(1, 10000))
    return child


def RouletteWheelSelection(P):
    r = np.random.rand()
    c = np.cumsum(P)
    i = np.where(r <= c)[0][0]
    return i
