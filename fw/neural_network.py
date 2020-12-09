import numpy as np
from typing import List, Callable, NewType, Optional


ActivationFunction = NewType('ActivationFunction', Callable[[np.ndarray], np.ndarray])

sigmoid = ActivationFunction(lambda X: 1.0 / (1.0 + np.exp(-X)))
tanh = ActivationFunction(lambda X: np.tanh(X))
relu = ActivationFunction(lambda X: np.maximum(0, X))
leaky_relu = ActivationFunction(lambda X: np.where(X > 0, X, X * 0.01))
linear = ActivationFunction(lambda X: X)



class FeedForwardNetwork:

    def __init__(self,
                 layer_nodes,
                 hidden_activation = 'sigmoid',
                 output_activation = 'sigmoid',
                 init_method = 'uniform',
                 rnd_start_value = 3000      # Число в интервале [0, 2**32]
    ):

        self.params = {}
        self.layer_nodes = layer_nodes
        self.hidden_activation = get_activation_by_name(hidden_activation)
        self.output_activation = get_activation_by_name(output_activation)
        self.inputs = None
        self.out = None
        self.fitness = None


        # Initialize weights and bias
        for l in range(1, len(self.layer_nodes)):
            if init_method == 'uniform':
                # генерим связи случайным образом
                self.params['W' + str(l)] = np.random.uniform(-1, 1, size=(self.layer_nodes[l], self.layer_nodes[l-1]))
                self.params['b' + str(l)] = np.random.uniform(-1, 1, size=(self.layer_nodes[l], 1))
            
            else:
                raise Exception('Implement more options, bro')

            self.params['A' + str(l)] = None


    def setFitness(self, fitness):
        self.fitness = fitness


    def feed_forward(self, X_arr):
        # X_arr массив входных данных
        A_prev = X_arr

        L = len(self.layer_nodes) - 1       # len(self.params) // 2

        # Feed hidden layers
        for l in range(1, L):
            W = self.params['W' + str(l)]
            b = self.params['b' + str(l)]
            dot = np.dot(W, A_prev)
            Z = dot + b
            A_prev = self.hidden_activation(Z)
            self.params['A' + str(l)] = A_prev

        # Feed output
        W = self.params['W' + str(L)]
        b = self.params['b' + str(L)]
        Z = np.dot(W, A_prev) + b
        out = self.output_activation(Z)
        self.params['A' + str(L)] = out

        self.out = out.reshape(len(out))
        return self.out

    # def softmax(self, X: np.ndarray) -> np.ndarray:
    #     return np.exp(X) / np.sum(np.exp(X), axis=0)

def get_activation_by_name(name: str):
    activations = [('relu', relu),
                   ('sigmoid', sigmoid),
                   ('linear', linear),
                   ('leaky_relu', leaky_relu),
                   ('tanh', tanh),
    ]

    func = [activation[1] for activation in activations if activation[0].lower() == name.lower()]
    assert len(func) == 1

    return func[0]
