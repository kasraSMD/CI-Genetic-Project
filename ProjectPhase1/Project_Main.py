from cmath import exp

import matplotlib.pyplot as plt
from Genetic_Algorithm import *

n_pop = 50
maximum_number_of_generations = 200
mutation_probability = 0.9
crossover_probability = 0.9

generations = []
generation1 = []
for pop_inx in range(n_pop):
    parent = City(20)
    parent.allocate_Towers_to_Blocks_by_shortest_path()
    parent.calculate_fitness()
    generation1.append(parent)

generations.append(generation1)

for gen in range(0, maximum_number_of_generations - 1):
    print(f"generation {gen}")
    ss = 0
    for g3 in range(len(generations[gen])):
        ss += generations[gen][g3].fitness_score
    print(ss)

    parents = list(generations[gen])
    offsprings = []
    new_generation = []

    # parents.sort(reverse=True)
    # parents_pool = parents[:(math.ceil(population_size * crossover_probability))]

    # parents pool selection

    # winner_index = tournament_selection(population=parents, tournament_size=population_size,
    #                                     num_winners=math.ceil(population_size * crossover_probability))
    # parents_pool = []
    # for i in range(len(winner_index)):
    #     parents_pool.append(parents[winner_index[i]])

    # recombination
    parents.sort(reverse=True)
    WorstCost = parents[n_pop - 1].fitness_score
    if WorstCost < 0:
        WorstCost = WorstCost * -1
    parentsCosts = []
    beta = 0.1  # selection pressure
    for i in range(len(parents)):
        parentsCosts.append(parents[i].fitness_score)
    nc = 2 * round(crossover_probability * n_pop / 2)
    for pop_inx in range(nc // 2):
        Ci = [(ci / WorstCost) for ci in parentsCosts]
        Pi = [(exp(-beta * ci)) for ci in Ci]
        s = sum(Pi)
        P = [Pi / s for Pi in Pi]
        i1 = RouletteWheelSelection(P)
        i2 = RouletteWheelSelection(P)
        # parent1, parent2 = random.choices(parents_pool, k=2)
        parent1 = parents[i1]
        parent2 = parents[i2]

        child1, child2 = crossover(parent1=parent1, parent2=parent2)
        # mutation=round(pm*nPop)
        child1 = mutation(child1, mutation_prob=mutation_probability)
        child2 = mutation(child2, mutation_prob=mutation_probability)
        child1.allocate_Towers_to_Blocks_by_shortest_path()
        child2.allocate_Towers_to_Blocks_by_shortest_path()
        child1.calculate_fitness()
        child2.calculate_fitness()

        offsprings.append(child2)
        offsprings.append(child2)

        # child1.show_city_info()
        # child2.show_city_info()

    # for i in range(len(offsprings)):
    #     parents.append(offsprings[i])

    # parents.sort(reverse=True)
    # print(len(parents))
    # new_generation = parents[:n_pop]
    # winner_index2 = tournament_selection(population=parents, tournament_size=len(parents), num_winners=n_pop)
    # for i in range(len(winner_index2)):
    #     new_generation.append(parents[winner_index2[i]])
    temp_generation = []
    for parent_inx in range(len(parents)):
        temp_generation.append(parents[parent_inx])
    for offsprings_inx in range(len(offsprings)):
        temp_generation.append(offsprings[offsprings_inx])

    # temp_generation.sort(reverse=True)
    new_generation = np.random.choice(temp_generation, n_pop)
    # random.shuffle(temp_generation)
    # new_generation = temp_generation[:n_pop]
    generations.append(new_generation)

generation_fitnesses_avg = []
generation_index = [i + 1 for i in range(maximum_number_of_generations)]
for i in range(len(generations)):
    fitness_sum = 0
    fitness_avg = 0
    for j in range(n_pop):
        fitness_sum += generations[i][j].fitness_score

    fitness_avg = fitness_sum / n_pop
    generation_fitnesses_avg.append(fitness_avg)

print(generation_index)
print(generation_fitnesses_avg)
plt.plot(generation_index, generation_fitnesses_avg)
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
