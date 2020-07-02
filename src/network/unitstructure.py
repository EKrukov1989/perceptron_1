"""Implementation of unit structure.

Neural network may have nontrivial structure - it may have different number
of units on each layer. That's why we need special data structure for it.

This structure provides access to value by indices - [i, j], where:
i - index of layer (starts from 0)
j - index of unit (starts from 0)
and it provides methods for forward and reverse iteration.
"""

import random


class UnitIterator():
    """Iterator for WeightSturcture."""

    __internal_array = []
    __counter = -1

    def __init__(self, internal_array):
        """Create iterator."""
        self.__internal_array = internal_array

    def __iter__(self):
        """Return oneself."""
        return self

    def __next__(self):
        """Return next element - [value, [i, j]]."""
        result = []
        self.__counter += 1
        try:
            result = self.__internal_array[self.__counter]
        except IndexError:
            raise StopIteration
        else:
            return result


class UnitStructure():
    """Structure for management of values that corresponding with units."""

    __index_map = []
    __internal_array = []
    __layers = []

    def __init__(self, configuration):
        """Create structure without initialization of weights."""
        # This structure can be used for another purposes, for instance - for
        # backpropogation coefficients. That's why initialization in
        # constructor is redundant.

        layers = []  # info about num of units for each layer
        layers.append(configuration['NumberOfInputUnits'] + 1)
        for info in configuration['LayersInfo']:
            layers.append(info['NumberOfUnits'] + 1)

        index_map = []
        internal_array = []
        idx = 0
        for i, units_num in enumerate(layers):
            index_map.append([None]*(units_num))
            for j in range(units_num):
                if i == (len(layers) - 1) and j == 0:
                    continue
                internal_array.append([None, [i, j]])
                index_map[i][j] = idx
                idx += 1
        self.__index_map = index_map
        self.__internal_array = internal_array
        self.__layers = layers

    def get_layers(self):
        """Return list with numbers of units on each layer.

        It returns number of units, including imagine units.
        Even for output layer.
        """
        return self.__layers

    def get_layers_num(self):
        """Return num of layers. Includes input and output layers."""
        return len(self.__layers)

    def init_imagine_units(self):
        """Initilize imagine units (zero unit on layer with value = 1)."""
        for i, layer in enumerate(self.__index_map):
            if i == (len(self.__index_map) - 1):
                continue
            idx = layer[0]
            _, ij = self.__internal_array[idx]
            self.__internal_array[idx] = [1, ij]

    def get_elt(self, i, j):
        """Get element by index."""
        idx = None
        try:
            idx = self.__index_map[i][j]
        except IndexError:
            raise AssertionError
        if idx is None:
            return None
        value, _ = self.__internal_array[idx]
        return value

    def set_elt(self, i, j, value):
        """Set element by index."""
        assert j != 0
        idx = self.__index_map[i][j]
        self.__internal_array[idx] = [value, [i, j]]

    def __iter__(self):
        """Return inerator. It provides all units as one sequence."""
        return UnitIterator(self.__internal_array)

    def get_string(self, colored=False):
        """Return graceful string representation of unit structure.

        Output string may consist color tags (for output in terminal) if
        corresponding argument set to True.
        """
        res = ''
        for i, layer in enumerate(self.__index_map):
            for j, idx in enumerate(layer):
                if idx is None:
                    continue
                value, _ = self.__internal_array[idx]
                if value:
                    str_val = '{:<10.5f}'.format(value)
                else:
                    str_val = '{:<10}'.format('None')
                if colored:
                    str_val = '\033[93m{}\033[0m'.format(str_val)
                res += 'U#{}-{}={} '.format(i, j, str_val)
            res += '\n'
        return res

    def __str__(self):
        """Return graceful string representation of weights structure."""
        return self.get_string(True)

    def __len__(self):
        """Return length of weights sequence."""
        return len(self.__internal_array)

    def __getitem__(self, idx):
        """Return tuple [value, [i, j, g]]."""
        return self.__internal_array[idx]

    def get_input_layer(self):
        """Return all values for input layer (without imagine unit)."""
        indices = self.__index_map[0]
        indices.pop(0)
        return list(map(lambda idx: self.__internal_array[idx][0], indices))

    def set_input_layer(self, input_arr):
        """Set values for input layer (input - without imagine unit)."""
        unit_indices = self.__index_map[0]
        assert len(input_arr) == (len(unit_indices) - 1)
        for j, idx in enumerate(unit_indices):
            if j == 0:
                continue
            self.__internal_array[idx] = input_arr[j-1]

    def get_output_layer(self):
        """Return all values for output layer (without imagine unit)."""
        indices = self.__index_map[-1]
        indices.pop(0)
        return list(map(lambda idx: self.__internal_array[idx][0], indices))

    def set_output_layer(self, output_arr):
        """Set values for ouput layer (output - without imagine unit)."""
        unit_indices = self.__index_map[-1]
        assert len(output_arr) == (len(unit_indices) - 1)
        for j, idx in enumerate(unit_indices):
            if j == 0:
                continue
            self.__internal_array[idx] = output_arr[j-1]
