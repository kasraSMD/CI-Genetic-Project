import math
import matplotlib.pyplot as plt
from NewProjectPhase1 import *
from Genetic_Algorithm import *

population_size = 50
maximum_number_of_generations = 200
mutation_probability = 0.1
crossover_probability = 0.1


# p1 = City(20)
# p1.initialize_towers()
# p1.calculate_fitness()
# p2 = City(20)
# p2.initialize_towers()
# p2.calculate_fitness()
# c1, c2 = crossover(parent1=p1, parent2=p2)
# c1.calculate_fitness()
# c2.calculate_fitness()
# c1.show_city_info()
# c2.show_city_info()

for i in range(maximum_number_of_generations):
    generation = []
    parents = []
    offsprings = []

    for pop_inx in range(population_size):
        city = City(20)
        city.initialize_towers()
        city.calculate_fitness()
        parents.append(city)

    parents.sort(reverse=True)
    # print(generation[0].fitness_score)
    # print(generation[1].fitness_score)
    # print(generation[2].fitness_score)
    parents_pool = parents[:(math.ceil(population_size * crossover_probability))]
    for pop_inx in range(math.ceil(population_size*crossover_probability)):
        parent1, parent2 = random.choices(parents_pool, k=2)
        child1, child2 = crossover(parent1=parent1, parent2=parent2)
        child1.calculate_fitness()
        child2.calculate_fitness()
        offsprings.append(child1)
        offsprings.append(child2)



        child1.show_city_info()
        child2.show_city_info()

#     generation_fitnesses = []
#     generation_index = []
#     for i in range(len(offsprings)):
#         generation_fitnesses.append(offsprings[i].fitness_score)
#         generation_index.append(i)
#
#     print(generation_index)
#     print(generation_fitnesses)
#     plt.plot(generation_fitnesses, generation_index)
#     plt.xlabel('Generation')
#     plt.ylabel('Fitness')
# plt.show()


