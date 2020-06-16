"""Implementation of Multilayer Perceptron.

Multilayer Perceptron, that implemented here has next features:
- Net  includes one or several inputs (x=[float,...]),
  one or several outputs (y=[float,...]), and may include hidden layers.
- Number of units on hidden layers may be different.
- All net groupped as sequence of layers.
  As zero layer - inputs, then - hidden layers and the last - output layer.
- Each unit in the net (except input units) nas connection with each unit
  on previous layer.
- Each layer can have its own activation function (except input layer).

Order of indexation:
All data in this class grouped by certain order. Here I describe this order
and used designations:
i - index of layer: [0;N], where 0 - input layer and N - output layer.
j - index of unit in layer: [0;M], where 0 corresponds with imagined
    unit value of that always equal to 1.
k - index of output unit: [1;K], where K - number of outputs.
g - index of unit on layer previous to i, don't mess with j.
q - index of unit on layer next after i.

Structure of data:
All data stored in multidimentsional arrays with next structure:
[i] - something corresponding with i-layer. Examples: activation functions,
      derivatives from them.
[i][j] - something corresponding with unit j on i-layer. Examples: z, a, b.
[i][j][g] - something corresponding with connection of unit j on layer i with
            unit g on layer i-1. Examples: weights, derivatives from weights.

Designations:
Usually capital letter corresponds with data-structure and lowercase letter
with certain value from this array. W - array of weights, w - certain weight.
w - weight;
h - activation function;
z - unit value;
a - unit value before applying activation function;
x - input value;
y - output value;
t - value from train data that corresponds with output value
b - backpropagation coefficient for unit
"""

import math
import copy


class NeuralNetwork():
    """Implementation of multilayer perceptron."""

    __config = {}
    __W = []
    __layers = []  # info about num of units for each layer
    __afuncs = []  # activation function for each layer
    __afunc_derivs = []  # derivatives od afuncs for each layer

    def __init__(self, configuration):
        """Create MultilayerPerceptron with certain configuration."""
        self.__configuration = configuration
        # Copy some data from __config for fast access:
        self.__layers.append(self.__configuration['NumberOfInputUnits'])
        self.__afuncs.append(None)
        self.__afunc_derivs.append(None)
        for info in self.__configuration['LayersInfo']:
            self.__layers.append(info['NumberOfUnits'])
            afunc_name = info['ActivationFunction']
            afunc = self.__get_activation_function(afunc_name)
            self.__afuncs.append(afunc)
            afunc_deriv = self.__get_deriv_of_afunc(afunc_name)
            self.__afunc_derivs.append(afunc_deriv)
        self.__init_weights_()

    def train(self, train_data):
        """Train network."""
        self.__init_weights_()

    def process(self, x):
        """Calculate output of network for certain x.

        x must be a list, and y must be a list. Length must correspond with
        configuration of net.
        """
        Z = self.__process_forward_propagation(x, self.__W)
        y = []
        for k in range(1, len(Z[-1])):
            y.append(Z[-1][k])
        return y

    def get_configure(self):
        """Return information about configuration of network."""
        return self.__configuration

    def __get_activation_function(self, func_name):
        funcs = {'tanh': math.tanh,
                 'sigmoid': lambda x: 1/(1 + math.exp(-x)),
                 'linear': lambda x: x}
        return funcs[func_name]

    def __get_deriv_of_afunc(self, func_name):
        # for all functions that we have derivatives of activation function
        # may be calculated through value of the activation function in this
        # point. This function return derivative as function from itself:
        funcs = {'tanh': lambda x: 1 - x**2,
                 'sigmoid': lambda x: x * (1 - x),
                 'linear': lambda x: 1}
        return funcs[func_name]

    def __init_weights_(self):
        """Set initial value for all weights."""
        if self.__W:
            return
        INIT_VAL = 0.5
        W = []
        for _, units_num in enumerate(self.__layers):
            W.append([None]*(units_num + 1))
        for i in range(1, len(W)):
            for j in range(1, len(W[i])):
                W[i][j] = [INIT_VAL] * len(W[i-1])
        self.__W = W

    def __process_forward_propagation(self, x, W):
        """Return result as array, argument - array as well."""
        # Z - array of unit-outputs, that consists also unput value and
        # imagined zero-indexed units:
        Z = []

        # Preinitialize Z-list, because it makes next code more readable:
        for units_num in self.__layers:
            Z.append([None]*(units_num + 1))
        for i, z_layer in enumerate(Z):
            if i != len(Z)-1:
                z_layer[0] = 1
        for i, x_val in enumerate(x):
            Z[0][i+1] = x_val

        layers_num = len(self.__layers)
        for i in range(1, layers_num):
            units_num = len(Z[i])
            prev_layer_units_num = len(Z[i-1])
            activation_func = self.__afuncs[i]

            for j in range(1, units_num):
                a = 0
                for g in range(prev_layer_units_num):
                    a += Z[i-1][g] * W[i][j][g]
                Z[i][j] = activation_func(a)
        return Z

    def error_function(self, sample):
        """Return error. Sample must have form [f, f]."""
        x, t = sample[0], sample[1]
        return self.__error_function([x, t], self.__W)

    def __error_function(self, sample, W):
        # sample must has from [x=[..], y=[..]]
        x, t = sample[0], sample[1]
        Z = self.__process_forward_propagation(x, W)
        y = []
        for k in range(1, len(Z[-1])):
            y.append(Z[-1][k])
        err = 0
        for i, y_val in enumerate(y):
            err += 0.5 * (y_val - t[i])**2
        return err

    def _calculate_gradient_by_backpropagation(self, sample):
        """Calculate gradient by backpropagation method.

        Still without generalization. Now all calucaltion for 1d-output
        """
        # 1. Calculate all activations:
        x = sample[0]
        Z = self.__process_forward_propagation(x, self.__W)

        # 2. Calculate all backpropagations coefficients:
        # Preinit backpropagaion coefficients structure:
        B = []
        for units_num in self.__layers:
            B.append([None]*(units_num + 1))
        # 2.1. for output layer:
        t = [None]
        for y_val in sample[1]:
            t.append(y_val)
        output_afunc_deriv = self.__afunc_derivs[-1]
        for k in range(1, len(Z[-1])):
            z = Z[-1][k]
            B[-1][k] = (z - t[k]) * output_afunc_deriv(z)
        # 2.2. for hidden layers:
        for i in range(len(Z) - 2, 0, -1):
            afunc_deriv = self.__afunc_derivs[i]
            for j in range(1, len(Z[i])):
                tmp = 0
                for q in range(1, len(Z[i+1])):
                    tmp += self.__W[i+1][q][j] * B[i+1][q]
                B[i][j] = afunc_deriv(Z[i][j]) * tmp
        print('B after calculation:')
        for b_layer in B:
            print(b_layer)

        # 3. Calculate derivatives:
        # Preinit derivatives structure:
        D = []  # derivatives array has th same structure as weight array
        for _, units_num in enumerate(self.__layers):
            D.append([None]*(units_num + 1))
        for i in range(1, len(D)):
            for j in range(1, len(D[i])):
                D[i][j] = ['d_val'] * len(D[i-1])
        # Calculate derivatives:
        for i in range(1, len(Z)):
            for j in range(1, len(Z[i])):
                for g in range(len(Z[i-1])):
                    D[i][j][g] = B[i][j] * Z[i-1][g]
        return D

    def _calculate_gradient_numerically(self, sample):
        """Return gradient calculated numerically."""
        EPSILON = 1.0e-12
        # Preinit derivatives structure:
        D = []  # derivatives array has th same structure as weight array
        for _, units_num in enumerate(self.__layers):
            D.append([None]*(units_num + 1))
        for i in range(1, len(D)):
            for j in range(1, len(D[i])):
                D[i][j] = ['d_val'] * len(D[i-1])
        # Calculate derivatives:
        for i in range(1, len(D)):
            for j in range(1, len(D[i])):
                for g in range(len(D[i][j])):
                    weights_plus = copy.deepcopy(self.__W)
                    weights_minus = copy.deepcopy(self.__W)
                    weights_plus[i][j][g] += EPSILON
                    weights_minus[i][j][g] -= EPSILON
                    e_plus = self.__error_function(sample, weights_plus)
                    e_minus = self.__error_function(sample, weights_minus)
                    d = 0.5 * (e_plus - e_minus) / EPSILON
                    D[i][j][g] = d
        return D
