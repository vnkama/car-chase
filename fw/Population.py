import numpy as np
from fw.neural_network import FeedForwardNetwork



#
#
#
class Population:

    #
    # size - размер популяции
    def __init__(self, size, NN_structure):
        self.NN_arr = np.empty([size],dtype=object)

        for i,v in enumerate(self.NN_arr):
            self.NN_arr[i] = FeedForwardNetwork(NN_structure)


    def getIndivid(self,index):
        return self.NN_arr[index]





