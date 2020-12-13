import numpy as np
from config import *
from fw.neural_network import FeedForwardNetwork



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

        self.NN_arr = np.empty([POPULATION_SIZE], dtype=object)

        for i, v in enumerate(self.NN_arr):
            self.NN_arr[i] = FeedForwardNetwork(NN_structure, rng=self.rng)


    def getIndivid(self, index):
        return self.NN_arr[index]


    # пересчитываем нейросети
    # предварительно у всех сетей должен быть установлен фитнес
    def calcNextGeneration(self):

        individs_alive = np.empty([INDIVIDS_ALIVE_COUNT], dtype=object)

        # отберем лучших особей для перехода в следующее поколение
        individs_alive[:INDIVIDS_ALIVE_COUNT] = \
            self.sort_elitism(
                    self.NN_arr,
                    INDIVIDS_ALIVE_COUNT,
            )

        self.rng.shuffle(individs_alive)
        individs_spring = np.empty([], dtype=object)

        while len(individs_spring) < INDIVIDS_SPRING_COUNT:
            individ1, individ2 = self.selectionRouletteWheel(self.population, 2, True)

            crossover(individ1, individ2)

                p1_W_l = p1.params['W' + str(l)]
                p2_W_l = p2.params['W' + str(l)]
                p1_b_l = p1.params['b' + str(l)]
                p2_b_l = p2.params['b' + str(l)]

                c1_W_l, c2_W_l, c1_b_l, c2_b_l = self._crossover(p1_W_l, p2_W_l, p1_b_l, p2_b_l)





        # for i in range(INDIVIDS_ALIVE_COUNT, POPULATION_SIZE):
        #     NN_new_arr[i] = FeedForwardNetwork(self.NN_structure, rng=self.rng)



        self.NN_arr = individs_alive + individs_spring



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
    # remove_mode   : True выбранные элементы удаяются из population
    #               : False выбранные элементы переносятсяудаяются из population
    #
    def selectionRouletteWheel(self, population, selected_count, remove_mode=True):
        selection_arr = []
        fitness_sum = sum(individ.fitness for individ in population)

        for _ in range(selected_count):
            pick = self.rng.uniform(0, fitness_sum)

            current = 0
            for individ in population:
                current += individ.fitness
                if current > pick:
                    fitness_sum -= individ.fitness
                    fitness_sum = 0 if fitness_sum < 0 else fitness_sum
                    selection_arr.append(individ)
                    if remove_mode:
                        population.remove(individ)
                    break

        return selection_arr

    def crossover(self, individ1, individ2):
        # число слоев NN
        NN_layer_count = len(self.NN_structure)

        # обход слоев
        for l in range(1, NN_layer_count):

            individ1_W_l = individ1.params['W' + str(l)]
            individ1_b_l = individ1.params['b' + str(l)]

            individ2_W_l = individ2.params['W' + str(l)]
            individ2_b_l = individ2.params['b' + str(l)]

            # random 0...1
            #random_crossover = self.rng.random()

            # выбор метода для кроссовера
            crossover_method = np.digitize(self.rng.random(), [0.5, 1.0])

            # SBX
            if crossover_method == 0:
                child1_weights, child2_weights = simulated_binary_crossover(parent1_weights, parent2_weights, self._SBX_eta)
                child1_bias, child2_bias = simulated_binary_crossover(parent1_bias, parent2_bias, self._SBX_eta)

            # Single point binary crossover (SPBX)
            elif crossover_method == 1:
                child1_weights, child2_weights = single_point_binary_crossover(parent1_weights, parent2_weights,
                                                                               major=self._SPBX_type)
                child1_bias, child2_bias = single_point_binary_crossover(parent1_bias, parent2_bias, major=self._SPBX_type)



    def _crossover(
            self,
            parent1_weights,
            parent2_weights,
            parent1_bias,
            parent2_bias
    ):
        # random 0...1
        rand_crossover = self.rng.random()

        crossover_bucket = np.digitize(rand_crossover, self._crossover_bins)


        child1_weights, child2_weights = None, None
        child1_bias, child2_bias = None, None

        # SBX
        if crossover_bucket == 0:
            child1_weights, child2_weights = SBX(parent1_weights, parent2_weights, self._SBX_eta)
            child1_bias, child2_bias = SBX(parent1_bias, parent2_bias, self._SBX_eta)

        # Single point binary crossover (SPBX)
        elif crossover_bucket == 1:
            child1_weights, child2_weights = single_point_binary_crossover(parent1_weights, parent2_weights,
                                                                           major=self._SPBX_type)
            child1_bias, child2_bias = single_point_binary_crossover(parent1_bias, parent2_bias, major=self._SPBX_type)

        else:
            raise Exception('Unable to determine valid crossover based off probabilities')

        return child1_weights, child2_weights, child1_bias, child2_bias