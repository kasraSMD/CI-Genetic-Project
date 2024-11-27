import json
import math
import random
import numpy as np


class Block:
    def __init__(self):
        self.position = []
        self.connected_tower = None
        self.population = 0
        self.BW_bx = 0
        self.BW_ui = 0
        self.BWprime_bx = 0
        self.user_satisfaction_score = 0


class Tower:
    def __init__(self, position, BW_ty):
        self.position = position
        self.BW_ty = BW_ty
        self.connected_population = 0


class City:
    def __init__(self, size, is_child=False):
        self.size = size
        self.blocks_matrix = np.array([[Block() for _ in range(size)] for _ in range(size)])
        self.towers = []
        self.tower_construction_cost = 0
        self.tower_maintenance_cost = 0
        self.total_tower_cost = 0
        self.fitness_score = 0
        self.total_satisfaction_score = 0
        self.user_satisfaction_levels = None
        self.user_satisfaction_scores = None
        self.read_blocks_population_from_file('blocks_population.txt')
        self.read_problem_config('problem_config.txt')
        if not is_child:
            self.initialize_towers()

    def __eq__(self, other):
        return self.fitness_score == other.fitness_score

    def __gt__(self, other):
        return self.fitness_score > other.fitness_score

    def __lt__(self, other):
        return self.fitness_score < other.fitness_score

    def read_problem_config(self, path):
        with open(path) as file:
            js = json.loads(file.read())
        self.tower_construction_cost = js['tower_construction_cost']
        self.tower_maintenance_cost = js['tower_maintanance_cost']
        self.user_satisfaction_levels = js['user_satisfaction_levels']
        self.user_satisfaction_scores = js['user_satisfaction_scores']

    def read_blocks_population_from_file(self, path):
        i = 0
        with open(path, 'r') as file:
            for line in file:
                x = line.split(',')
                for j in range(len(self.blocks_matrix)):
                    self.blocks_matrix[i][j].position = np.array([i, j])
                    self.blocks_matrix[i][j].population = int(x[j])
                i += 1

    def initialize_towers(self):
        for i in range(np.random.randint(1, 400)):
            # X, Y coordination of the tower and bandwidth
            #  search not implemented yet!
            self.towers.append(Tower([random.uniform(0, 19), random.uniform(0, 19)], random.randint(1, 10000)))

    def distance_between_Blocks_Towers(self, xyBlocks, xyTowers):
        return math.sqrt((xyBlocks[0] - xyTowers[0]) ** 2 + (xyBlocks[1] - xyTowers[1]) ** 2)

    def allocate_Towers_to_Blocks_by_shortest_path(self):
        for x in range(self.size):
            for y in range(self.size):
                min_distance = np.inf
                for z in range(len(self.towers)):
                    dis = self.distance_between_Blocks_Towers(self.blocks_matrix[x][y].position,
                                                              self.towers[z].position)
                    if min_distance >= dis:
                        min_distance = dis
                        self.blocks_matrix[x][y].connected_tower = self.towers[z]
                        self.towers[z].connected_population += self.blocks_matrix[x][y].population

    def calculate_BW_bx_in_each_block(self):
        for x in range(self.size):
            for y in range(self.size):
                sigma = np.array([[8, 0], [0, 8]])  # Covariance matrix
                inv_sigma = np.linalg.inv(sigma)
                connected_tower = self.blocks_matrix[x][y].connected_tower
                cov = np.exp(
                    -0.5 * np.dot(np.dot((self.blocks_matrix[x][y].position - connected_tower.position), inv_sigma),
                                  (self.blocks_matrix[x][y].position - connected_tower.position).T))
                self.blocks_matrix[x][y].BWprime_bx = (self.blocks_matrix[x][
                                                           y].population * connected_tower.BW_ty) / connected_tower.connected_population
                self.blocks_matrix[x][y].BW_bx = cov * self.blocks_matrix[x][y].BWprime_bx

    def calculate_BW_ui_in_each_block(self):
        for i in range(self.size):
            for j in range(self.size):
                self.blocks_matrix[i][j].BW_ui = self.blocks_matrix[i][j].BW_bx / self.blocks_matrix[i][j].population

    def calculate_user_satisfaction_score_in_each_block(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.blocks_matrix[i][j].BW_ui < self.user_satisfaction_levels[0]:
                    self.blocks_matrix[i][j].user_satisfaction_score = 0
                elif self.user_satisfaction_levels[0] <= self.blocks_matrix[i][j].BW_ui < self.user_satisfaction_levels[
                    1]:
                    self.blocks_matrix[i][j].user_satisfaction_score = self.user_satisfaction_scores[0]
                elif self.user_satisfaction_levels[1] <= self.blocks_matrix[i][j].BW_ui < self.user_satisfaction_levels[
                    2]:
                    self.blocks_matrix[i][j].user_satisfaction_score = self.user_satisfaction_scores[1]
                elif self.blocks_matrix[i][j].BW_ui >= self.user_satisfaction_levels[2]:
                    self.blocks_matrix[i][j].user_satisfaction_score = self.user_satisfaction_scores[2]

    def objective_function(self):
        self.total_tower_cost = self.tower_construction_cost * len(self.towers)
        for tower_inx in range(len(self.towers)):
            self.total_tower_cost += self.towers[tower_inx].BW_ty * self.tower_maintenance_cost

        self.total_satisfaction_score = 0
        for i in range(self.size):
            for j in range(self.size):
                self.total_satisfaction_score += self.blocks_matrix[i][j].user_satisfaction_score * self.blocks_matrix[i][j].population

        self.fitness_score = self.total_satisfaction_score - self.total_tower_cost

    def show_city_info(self):
        print(f"Towers Info : len = {len(self.towers)}\n")
        for i in range(len(self.towers)):
            print(f"position: {self.towers[i].position}")
            print(f"BW_ty: {self.towers[i].BW_ty}")
            print()
        print()
        print("Blocks Info :\n")
        for i in range(self.size):
            for j in range(self.size):
                print(f"Block position: {self.blocks_matrix[i][j].position}")
                print(f"Block population: {self.blocks_matrix[i][j].population}")
                print(f"Block BW_bx: {self.blocks_matrix[i][j].BW_bx}")
                print(f"Block BW_ui: {self.blocks_matrix[i][j].BW_ui}")
                print(f"Block BWprime_bx: {self.blocks_matrix[i][j].BWprime_bx}")
                print(f"user satisfaction score: {self.blocks_matrix[i][j].user_satisfaction_score}")
                print(
                    f"connected tower: {self.blocks_matrix[i][j].connected_tower.position},{self.blocks_matrix[i][j].connected_tower.BW_ty}")
                print()

        print(f"total_tower_cost : {self.total_tower_cost}")
        print(f"total_satisfaction_score : {self.total_satisfaction_score}")
        print(f"fitness score : {self.fitness_score}")

    def calculate_fitness(self):
        self.allocate_Towers_to_Blocks_by_shortest_path()
        self.calculate_BW_bx_in_each_block()
        self.calculate_BW_ui_in_each_block()
        self.calculate_user_satisfaction_score_in_each_block()
        self.objective_function()
