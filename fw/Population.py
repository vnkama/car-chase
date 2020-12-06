import numpy as np
from fw.neural_network import FeedForwardNetwork
#from fw.neural_network import *


#
#
#
class Population:

    #
    # size - размер популяции
    def __init__(self, size, NN_structure):
        self.NN_arr = np.empty([size])

        for i,v in enumerate(self.NN_arr):
            v = FeedForwardNetwork(NN_structure)


    def getIndivid(self,index):
        return self.NN_arr[index]





