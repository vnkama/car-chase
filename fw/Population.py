import numpy as np
from config import *
from fw.neural_network import FeedForwardNetwork

from typing import Tuple


#
#
#
class Population:

    #
    # size - размер популяции
    def __init__(self, size, NN_structure):

        # размер популяции
        self.population_size = size

        self.NN_structure = NN_structure

        self.rng = np.random.default_rng(1000)

        self.individs = np.empty([POPULATION_SIZE], dtype=object)

        for i, v in enumerate(self.individs):
            self.individs[i] = FeedForwardNetwork(NN_structure, rng=self.rng)


    def getIndivid(self, index):
        return self.individs[index]


    # пересчитываем нейросети
    # предварительно у всех сетей должен быть установлен фитнес
    def calcNextGeneration(self):

        individs_alive = np.empty([INDIVIDS_ALIVE_COUNT], dtype=object)

        # отберем лучших особей для перехода в следующее поколение
        individs_alive[:INDIVIDS_ALIVE_COUNT] = \
            self.sort_elitism(
                    self.individs,
                    INDIVIDS_ALIVE_COUNT,
            )

        self.rng.shuffle(individs_alive)
        individs_spring = np.empty([0], dtype=object)

        while len(individs_spring) < INDIVIDS_CHILD_COUNT:

            # так как при выполнении selectionRouletteWheel, родители удаляются из self.individs
            # то число потомков не может быть больше числа родителей
            parent1, parent2 = self.selectionRouletteWheel(self.individs, 2, True)

            child1, child2 = self.crossover(parent1, parent2)

            # child1 = self.mutation(child1)
            # child2 = self.mutation(child2)

            individs_spring = np.append((individs_spring, [child1], [child2]))


        # сложим родителей и потомков
        self.individs = np.append((individs_alive, individs_spring))



    def sort_elitism(self, population, selected_count):
        A = sorted(
                population,
                key=lambda v: v.fitness,
                reverse=True,  # лучший в нулевом индексе
        )

        return A[:selected_count]


    #
    # отбор особей прошедших в следующий тур.
    # вероятность выхода особи в следущий тур пропорциональна их фитнесс функции
    #
    # remove_mode   : True выбранные элементы удаяются из population,
    #               : False выбранные элементы переносятсяудаяются из population
    #
    def selectionRouletteWheel(self, individs, selected_count, remove_mode=True):
        individs_childs = np.empty(shape=(0,1), dtype=object)
        fitness_sum = sum(individ.fitness for individ in individs)

        for _ in range(selected_count):
            pick = self.rng.uniform(0, fitness_sum)

            current = 0
            for individ in individs:
                current += individ.fitness
                if current > pick:
                    fitness_sum -= individ.fitness
                    fitness_sum = 0 if fitness_sum < 0 else fitness_sum
                    individs_childs = np.append((individs_childs, individ))
                    if remove_mode:
                        individs.remove(individ)
                    break

        return individs_childs



    #
    #
    #
    def crossover(self, individ1, individ2):
        # число слоев NN
        NN_layer_count = len(self.NN_structure)

        # обход слоев
        for l in range(1, NN_layer_count):

            individ_1_Weight = individ1.params['W' + str(l)]
            individ_1_bias = individ1.params['b' + str(l)]

            individ_2_Weight = individ2.params['W' + str(l)]
            individ_2_bias = individ2.params['b' + str(l)]

            # random 0...1
            #random_crossover = self.rng.random()

            # выбор метода для кроссовера
            crossover_method = np.digitize(self.rng.random(), [0.5, 1.0])

            #  simulated_binary_crossover
            if crossover_method == 0:
                individ_1_Weight, individ_2_Weight = crossover_simulated_binary(individ_1_Weight, individ_2_Weight, SBX_eta)
                individ_1_bias, individ_2_bias = crossover_simulated_binary(individ_1_bias, individ_2_bias, SBX_eta)

            # Single point binary crossover (SPBX)
            elif crossover_method == 1:
                individ_1_Weight, individ_2_Weight = crossover_single_point_binary(individ_1_Weight, individ_2_Weight)
                individ_1_bias, individ_2_bias = crossover_single_point_binary(individ_1_bias, individ_2_bias)

        return individ1, individ2


    #
    # мутация одного индивида
    #
    def mutation(self, individ):
        # число слоев NN
        NN_layer_count = len(self.NN_structure)

        # обход слоев
        for l in range(1, NN_layer_count):
            pass


        return individ





    # p.177

    #
    # на хромосоме выбирается ячейка,
    # ячейки до выбранной - меняются местами,
    #
    def crossover_single_point_binary(
            parent1,        # хромосома первого родителя
            parent2,        # хромосома второго родителя
            major='r'
    ):

        offspring1 = parent1.copy()
        offspring2 = parent2.copy()

        rows, cols = parent2.shape
        row = self.rng.randint(0, rows)
        col = self.rng.randint(0, cols)

        if major == 'r':
            offspring1[:row, :] = parent2[:row, :]
            offspring2[:row, :] = parent1[:row, :]

            offspring1[row, :col+1] = parent2[row, :col+1]
            offspring2[row, :col+1] = parent1[row, :col+1]

        elif major == 'c':
            offspring1[:, :col] = parent2[:, :col]
            offspring2[:, :col] = parent1[:, :col]

            offspring1[:row+1, col] = parent2[:row+1, col]
            offspring2[:row+1, col] = parent1[:row+1, col]

        return offspring1, offspring2



    #
    # меняются все хромосомы попарно,
    # но  происходит не посто обмен генами
    # а пересчета генов по определеному закону
    #
    def crossover_simulated_binary(
            self,
            parent1,
            parent2,
            eta: float
    ):
        """
        This crossover is specific to floating-point representation.
        Simulate behavior of one-point crossover for binary representations.

        For large values of eta there is a higher probability that offspring will be created near the parents.
        For small values of eta, offspring will be more distant from parents

        Equation 9.9, 9.10, 9.11
        @TODO: Link equations
        """
        # Calculate Gamma (Eq. 9.11)
        rand = self.rng.random(parent1.shape)
        gamma = np.empty(parent1.shape)
        gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))  # First case of equation 9.11
        gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))  # Second case

        # Calculate Child 1 chromosome (Eq. 9.9)
        offspring1 = 0.5 * ((1 + gamma) * parent1 + (1 - gamma) * parent2)
        # Calculate Child 2 chromosome (Eq. 9.10)
        offspring2 = 0.5 * ((1 - gamma) * parent1 + (1 + gamma) * parent2)

        return offspring1, offspring2



    #
    # каждая из 2х хромосома представляет из себя массив, оба массива одного размера
    # с вероятностью 0.5 происходит обмен генами между хромосомами
    #
    def crossover_uniform_binary(
            self,
            parent1,       # хромомома одного предка, массив numpy
            parent2,       # хромомома второго предка, массив numpy
    ):
        offspring1 = parent1.copy()
        offspring2 = parent2.copy()

        # массив случайных чисел
        mask = self.rng.uniform(0, 1, size=offspring1.shape)

        offspring1[mask > 0.5] = parent2[mask > 0.5]
        offspring2[mask > 0.5] = parent1[mask > 0.5]

        return offspring1, offspring2
