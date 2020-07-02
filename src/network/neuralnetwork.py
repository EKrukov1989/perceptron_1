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
import random
from . import weightstructure as ws
from . import unitstructure as us


class NeuralNetwork():
    """Implementation of multilayer perceptron."""

    __configuration = {}
    __W = None
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
        self.__W = ws.WeightStructure(configuration)
        self.__W.random_initialization()

    def process(self, x):
        """Calculate output of network for certain x.

        x must be a list, and y must be a list. Length must correspond with
        configuration of net.
        """
        Z = self.__process_forward_propagation(x, self.__W)
        return Z.get_output_layer()

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

    def __process_forward_propagation(self, x, W):
        """Return result as array, argument - array as well."""
        # Z - data structure with activations of all units
        Z = us.UnitStructure(self.__configuration)
        Z.init_imagine_units()
        for i, x_val in enumerate(x):
            Z.set_elt(0, i+1, x_val)

        for _, [i, j] in Z:
            if i == 0 or j == 0:
                continue
            weights = W.get_unit_elts(i, j)
            a = 0
            for w, [_, _, g] in weights:
                a += Z.get_elt(i-1, g) * w
            z_val = self.__afuncs[i](a)
            Z.set_elt(i, j, z_val)
        return Z

    def error_function(self, sample):
        """Return error. Sample must have form [f, f]."""
        return self.__error_function(sample, self.__W)

    def general_error_function(self, data_set):
        """Return error. Data_set must have form [[f,f],...]."""
        general_error = 0.0
        for sample in data_set:
            generalized_sample = [[sample[0]], [sample[1]]]
            error = self.__error_function(generalized_sample, self.__W)
            general_error += error
        return general_error

    def __error_function(self, sample, W):
        # sample must has from [x=[..], y=[..]]
        x, t = sample[0], sample[1]
        Z = self.__process_forward_propagation(x, W)
        y = Z.get_output_layer()
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
        B = us.UnitStructure(self.__configuration)
        t = [None]
        for y_val in sample[1]:
            t.append(y_val)

        for z, [i, j] in reversed(Z):
            if j == 0 or i == 0:
                continue
            afunc_deriv = self.__afunc_derivs[i]
            if i == (Z.get_layers_num() - 1):
                b = (z - t[j]) * afunc_deriv(z)
            else:
                tmp = 0
                for q in range(1, Z.get_layers()[i+1]):
                    tmp += self.__W.get_elt(i+1, q, j) * B.get_elt(i+1, q)
                b = afunc_deriv(z) * tmp
            B.set_elt(i, j, b)

        # 3. Calculate derivatives:
        D = ws.WeightStructure(self.__configuration)
        for _, [i, j, g] in D:
            derivative = B.get_elt(i, j) * Z.get_elt(i-1, g)
            D.set_elt(i, j, g, derivative)
        return D

    def _calculate_gradient_numerically(self, sample):
        """Return gradient calculated numerically."""
        EPSILON = 1.0e-10
        D = ws.WeightStructure(self.__configuration)
        for _, [i, j, g] in D:
            w_plus = copy.deepcopy(self.__W)
            w_minus = copy.deepcopy(self.__W)
            w_plus.set_elt(i, j, g, w_plus.get_elt(i, j, g) + EPSILON)
            w_minus.set_elt(i, j, g, w_minus.get_elt(i, j, g) - EPSILON)
            e_plus = self.__error_function(sample, w_plus)
            e_minus = self.__error_function(sample, w_minus)
            derivative = 0.5 * (e_plus - e_minus) / EPSILON
            D.set_elt(i, j, g, derivative)
        return D

    def train(self, train_data):
        """Train network. train_data must have format [[f,...], [f,...]]."""
        # The simplest stochastic gradient descent:
        report = 'Network training by SGD:\n'
        g_err = self.general_error_function(train_data)
        g_err_checkpoint = g_err
        STEP = 0.1
        MAX_ITER_NUM = 50000
        CHECKPOINT_NUMBER = 5000
        report += 'Initial state: g_err={}\n'.format(g_err)
        report += 'Initial weights:\n'
        report += self.__W.get_string()
        report += '\n\n'

        for iteration in range(MAX_ITER_NUM):
            report += 'Iteration #{}\n'.format(iteration)
            rand_index = random.randrange(0, len(train_data))
            sample = train_data[rand_index]
            gen_sample = [[sample[0]], [sample[1]]]
            grad = self._calculate_gradient_by_backpropagation(gen_sample)
            report += 'Gradient:'
            report += grad.get_string()
            for weight, [i, j, g] in self.__W:
                weight -= grad.get_elt(i, j, g) * STEP
            report += 'Recalculated weights:\n'
            report += self.__W.get_string()
            prev_g_err = g_err
            g_err = self.general_error_function(train_data)
            sample_impr = 1 - g_err / prev_g_err
            report += 'General error={:.4f}, improvement={:.6f}\n'.format(
                g_err, sample_impr)
            report += '\n\n'
            if iteration != 0 and iteration % CHECKPOINT_NUMBER == 0:
                report += ' * * * \n'
                report += 'Checkpoint on iteration #{}\n'.format(iteration)
                checkpoint_impr = 1 - g_err / g_err_checkpoint
                g_err_checkpoint = g_err
                report += 'Checkpoint improvement={:.6f}\n'.format(
                    checkpoint_impr)
                report += '\n\n'
                if checkpoint_impr < 0.0001:
                    report += 'Further training is unreasonable. Stop.\n'
                    break
        return report
