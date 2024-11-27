import json
import math
import numpy as np


def read_blocks_population_from_file(path, matrix):
    i = 0
    with open(path, 'r') as file:
        for line in file:
            x = line.split(',')
            for j in range(20):
                matrix[i][j] = int(x[j])
            i += 1


def read_problem_config(path):
    with open(path) as file:
        js = json.loads(file.read())
    return js


# blocks_matrix = np.int_(np.zeros((3, 3)))
blocks_matrix = np.array([[196, 887, 783],
                          [697, 679, 566],
                          [513, 549, 830]])
blocks_matrix_len = len(blocks_matrix)



def distance(xyBlocks, xyTowers):
    return math.sqrt((xyBlocks[0] - xyTowers[0]) ** 2 + (xyBlocks[1] - xyTowers[1]) ** 2)


def allocate_towers(blocks, towers, allocation_matrix):
    for x in range(len(blocks)):
        for y in range(len(blocks)):
            min_distance = np.inf
            for z in range(len(towers)):
                dis = distance([x, y], towers[z])
                if min_distance >= dis:
                    min_distance = dis
                    allocation_matrix[x][y] = np.array(towers[z])


def calculate_BW_ui(BW_ui, blocks_matrix, allocation_matrix):
    for i in range(len(blocks_matrix)):
        for j in range(len(blocks_matrix)):
            BW_ui[i][j] = allocation_matrix[i][j][2] / blocks_matrix[i][j]


towers = [[0, 0, 100], [1, 2, 200]]
allocation_matrix = np.array([np.zeros((blocks_matrix_len, len(towers[0]))) for i in range(len(blocks_matrix))])
print(allocation_matrix)

BW_ui = np.zeros((blocks_matrix_len, blocks_matrix_len))

print()
print(BW_ui)


def fitness(target):
    allocate_towers(blocks=target, towers=towers, allocation_matrix=allocation_matrix)
    calculate_BW_ui(BW_ui=BW_ui, blocks_matrix=blocks_matrix, allocation_matrix=allocation_matrix)