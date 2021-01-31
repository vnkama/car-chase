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
    def __init__(self, size, NN_structure, random_generator):

        # размер популяции
        self.population_size = size

        self.NN_structure = NN_structure

        self.rng = random_generator


        self.individs = np.empty([POPULATION_SIZE], dtype=object)

        for i, v in enumerate(self.individs):
            self.individs[i] = FeedForwardNetwork(self.NN_structure, rng=self.rng)


    def getIndivid(self, index):
        return self.individs[index]


    # пересчитываем нейросети
    # предварительно у всех сетей должен быть посчитан фитнес
    def calcNextGeneration(self):


        # отберем лучших особей для перехода в следующее поколение

        #individs_alive - это ссылки на объекты из self.individs
        individs_alive = self.sort_elitism(
                self.individs,
                INDIVIDS_ALIVE_COUNT,
        )

        # особи из которых будем выбирать родителей
        # individs_parents, individs_alive -списки разные, но указывают на одни и теже FeedForwardNetwork
        individs_4_parents = np.copy(individs_alive)

        # перемешаем выживших
        # self.rng.shuffle(individs_alive)

        # массив потомков
        individs_childs = np.empty([INDIVIDS_CHILD_COUNT], dtype=object)


        for child_ind in range(0, INDIVIDS_CHILD_COUNT, 2):

            # если при выполнении selectionRouletteWheel, указать, что родители удаляются из self.individs
            # то в таком случае число потомков не может быть больше числа родителей
            # отбираем потомков
            parent1, parent2 = self.selectionRouletteWheel(individs_4_parents, 2, True)

            #
            child1, child2 = self.crossover(parent1, parent2)

            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            # при нечетном INDIVIDS_CHILD_COUNT , последний child записывается только child1
            if child_ind + 2 <= INDIVIDS_CHILD_COUNT:
                individs_childs[child_ind:child_ind+2] = (child1, child2)
            else:
                individs_childs[child_ind] = child1


        # сложим родителей и потомков
        self.individs = np.append(individs_alive, individs_childs)
        #self.rng.shuffle(self.individs)



    #
    #
    #
    def sort_elitism(self, population, selected_count):
        A = sorted(
                population,
                key=lambda v: v.fitness,
                reverse=True,  # лучший в нулевом индексе
        )

        return A[:selected_count]


    #

    #
    # отбор особей прошедших в следующий тур.
    # вероятность выхода особи в следущий тур пропорциональна их фитнесс функции
    #
    # remove_mode   : True выбранные элементы удаяются из individs,
    #               : False выбранные элементы не удаяются из individs
    # функ-ция НЕ делает копии особей, возвращает то что содеражалось в individs
    #
    #
    def selectionRouletteWheel(self, individs, selected_count, remove_mode=True):

        individs_selected = np.empty([0], dtype=object)
        fitness_sum = sum(individ.fitness for individ in individs)

        for _ in range(selected_count):
            pick = self.rng.uniform(0, fitness_sum)

            current = 0
            for i, individ in np.ndenumerate(individs):
            #for individ in individs:
                current += individ.fitness
                if current > pick:
                    individs_selected = np.append(individs_selected, individ)
                    if remove_mode:
                        try:
                            individs = np.delete(individs,i)
                        except Exception as ex:
                            pass
                        fitness_sum -= individ.fitness
                    break

        return individs_selected



    #
    #
    #
    def crossover(self, individ1, individ2):

        child1 = FeedForwardNetwork(self.NN_structure, rng=self.rng)
        child2 = FeedForwardNetwork(self.NN_structure, rng=self.rng)

        # число слоев NN
        NN_layer_count = len(self.NN_structure)

        # обход слоев
        for l in range(1, NN_layer_count):
            W_ind = 'W' + str(l)
            b_ind = 'b' + str(l)

            individ_1_Weight = individ1.params[W_ind]    # копирует по ссылке(без копии)
            individ_1_bias = individ1.params[b_ind]

            individ_2_Weight = individ2.params[W_ind]
            individ_2_bias = individ2.params[b_ind]

            # выбор метода для кроссовера
            crossover_method = np.digitize(self.rng.random(), [0.5, 1.0])
            crossover_method = 0

            #  simulated_binary_crossover
            if crossover_method == 0:
                child1.params[W_ind], child2.params[W_ind] = self.crossover_simulated_binary(individ_1_Weight, individ_2_Weight, SBX_eta)
                child1.params[b_ind], child2.params[b_ind] = self.crossover_simulated_binary(individ_1_bias, individ_2_bias, SBX_eta)

            # Single point binary crossover (SPBX)
            elif crossover_method == 1:
                child1.params[W_ind], child2.params[W_ind] = self.crossover_single_point_binary(individ_1_Weight, individ_2_Weight)
                child1.params[b_ind], child2.params[b_ind] = self.crossover_single_point_binary(individ_1_bias, individ_2_bias)


        return child1, child2


    #
    # мутация одного индивида
    #
    def mutation(self, individ):
        # число слоев NN
        NN_layer_count = len(self.NN_structure)

        rnd = self.rng.random()
        mutation_bucket = np.digitize(rnd, [0.5, 1.0])

        mutation_probabilty = 0.05
        mutation_scale = 0.2

        # обход слоев
        for l in range(1, NN_layer_count):
            individ_Weight = individ.params['W' + str(l)]
            individ_bias = individ.params['b' + str(l)]



            if mutation_bucket == 0 or True:
                # Mutate weights
                self.gaussian_mutation(individ_Weight, mutation_probabilty, mutation_scale)

                # Mutate bias
                self.gaussian_mutation(individ_bias, mutation_probabilty, mutation_scale)

            else:
                self.random_uniform_mutation(individ_Weight, mutation_probabilty, -2, 2)

            # Mutate bias
                self.random_uniform_mutation(individ_bias, mutation_probabilty, -2, 2)

        return individ

    #
    #
    #
    def gaussian_mutation(self, chromosome_arr, mutation_probabilty, mutation_scale):


        # булевский массив, true -соответствующаф хромосома меняется
        mutation_arr = np.random.random(chromosome_arr.shape) < mutation_probabilty

        gaussian_mutation = np.random.normal(size=chromosome_arr.shape)

        gaussian_mutation[mutation_arr] *= mutation_scale

        # те хромосомы на которые mutation_array=True вносим коррекцию
        chromosome_arr[mutation_arr] += gaussian_mutation[mutation_arr]

    #
    #
    #
    def random_uniform_mutation(self, chromosome_arr, mutation_probabilty, low, high):

        # булевский массив, true -соответствующаф хромосома меняется
        mutation_arr = np.random.random(chromosome_arr.shape) < mutation_probabilty

        # генерируем массив случайных чисел
        uniform_mutation = np.random.uniform(low, high, size=chromosome_arr.shape)

        # копируем только те мутировавшие гены где mutation_arr = True
        chromosome_arr[mutation_arr] = chromosome_arr[mutation_arr] * uniform_mutation[mutation_arr]



    #
    # на хромосоме выбирается ячейка,
    # ячейки до выбранной - меняются местами,
    #
    def crossover_single_point_binary(
            self,
            parent1,        # хромосома первого родителя
            parent2,        # хромосома второго родителя
            major='r'
    ):

        offspring1 = parent1.copy()
        offspring2 = parent2.copy()

        rows, cols = parent2.shape
        row = self.rng.integers(0, rows)
        col = self.rng.integers(0, cols)

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
    # но  происходит не просто обмен генами
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
