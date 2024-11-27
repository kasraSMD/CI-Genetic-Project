from copy import copy

from Project_Main_Classes import *
import random


def crossover(parent1, parent2):
    child1 = City(20, True)
    child2 = City(20, True)
    child1.copy_parent_attribute_to_child(parent1)
    child2.copy_parent_attribute_to_child(parent2)

    pSinglePoint = 0.2
    pDoublePoint = 0.3
    pUniform = 1 - pSinglePoint - pDoublePoint
    num = RouletteWheelSelection([pSinglePoint, pDoublePoint, pUniform])

    if num == 0:  # single point crossover
        # print('single point crossover')
        nVar = len(parent1.towers)
        c = np.random.randint(1, nVar)
        child1.towers = np.concatenate((parent1.towers[:c], parent2.towers[c:]))
        child2.towers = np.concatenate((parent2.towers[:c], parent1.towers[c:]))

    elif num == 1:  # double point crossover
        # print('double point crossover')
        nVar = len(parent1.towers)
        cc = np.random.choice(nVar - 1, 2, replace=False)
        c1 = min(cc)
        c2 = max(cc)
        child1.towers = np.concatenate((parent1.towers[:c1], parent2.towers[c1:c2], parent1.towers[c2:]))
        child2.towers = np.concatenate((parent2.towers[:c1], parent1.towers[c1:c2], parent2.towers[c2:]))

    elif num == 2:  # uniform crossover
        # print('uniform crossover')
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

    # child1.allocate_towers_to_child(parent1=parent1, parent2=parent2)
    # child2.allocate_towers_to_child(parent1=parent1, parent2=parent2)

    return child1, child2


def mutation(child, mutation_prob=None):
    towers_position = []
    for tower_inx in range(len(child.towers)):
        towers_position.append(child.towers[tower_inx].position)

    number_rnd_change = np.random.randint(0, len(child.towers))
    random_inx_change = 0
    for i in range(number_rnd_change):
        random_inx_change = np.random.randint(0, number_rnd_change)
    newTower = Tower(Tower.define_random_xy(), random.randint(1, Tower.MAX_BANDWIDTH))
    while newTower.position in towers_position:
        newTower = Tower(Tower.define_random_xy(), random.randint(1, Tower.MAX_BANDWIDTH))

    child.towers[random_inx_change] = newTower
    towers_position[random_inx_change] = newTower.position

    return child


def RouletteWheelSelection(P):
    r = np.random.rand()
    c = np.cumsum(P)
    i = np.where(r <= c)[0][0]
    return i


def tournament_selection(population, tournament_size, num_winners):
    # Choose `tournament_size` individuals from the population at random
    tournament_indices = np.random.choice(len(population), size=tournament_size, replace=False)
    tournament_members = [population[i] for i in tournament_indices]

    # Find the `num_winners` individuals with the lowest cost in the tournament
    tournament_costs = [ind.fitness_score for ind in tournament_members]
    winner_indices = tournament_indices[np.argpartition(tournament_costs, num_winners - 1)[:num_winners]]

    return winner_indices
