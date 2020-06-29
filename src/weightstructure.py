"""Implementation of weight structure.

Neural network may have nontrivial structure - it may have different
number of units on each layer and therefore different number of
weight for each unit and so on.
That's why we need special data structure for it.

This structure provides acces to weight by indices - [i, j, g], where:
i - index of layer (starts from 1, because input layer units have no weights)
j - index of unit (starts from 1, because imagine units have no weights)
g - index of weight (starts from 0)
and it provides methods for forward and reverse iteration.
"""

import random


class WeightIterator():
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
        """Return next element - [value, [i, j, g]]."""
        result = []
        self.__counter += 1
        try:
            result = self.__internal_array[self.__counter]
        except IndexError:
            raise StopIteration
        else:
            return result


class WeightStructure():
    """Structure for convenient weights management.

    Weights structure is pretty complex and if we use standard list for it
    - iteration will be very long and complex. On the other hand - sometimes
    access by index is also required. This class provides both ways of access.
    """

    __index_map = []
    __internal_array = []

    def __init__(self, configuration):
        """Create structure without initialization of weights."""
        # This structure can be used for another purposes, for instance - for
        # error function derivatives with regard of weights. That's why
        # initialization in constructor is redundant.

        layers = []  # info about num of units for each layer
        layers.append(configuration['NumberOfInputUnits'])
        for info in configuration['LayersInfo']:
            layers.append(info['NumberOfUnits'])

        idx = 0
        index_map = []
        internal_array = []
        for _, units_num in enumerate(layers):
            index_map.append([None]*(units_num + 1))
        for i in range(1, len(index_map)):
            for j in range(1, len(index_map[i])):
                unit_indices = []
                for g in range(len(index_map[i-1])):
                    unit_indices.append(idx)
                    internal_array.append([None, [i, j, g]])
                    idx += 1
                index_map[i][j] = unit_indices
        self.__index_map = index_map
        self.__internal_array = internal_array

    def random_initialization(self):
        """Init all weights randomly."""
        COEFF = 1.0
        for idx, [_, [i, j, g]] in enumerate(self.__internal_array):
            self.__internal_array[idx] = [random.random() * COEFF, [i, j, g]]

    def get_elt(self, i, j, g):
        """Get element by index."""
        idx = None
        try:
            idx = self.__index_map[i][j][g]
        except IndexError:
            raise AssertionError
        value, _ = self.__internal_array[idx]
        return value

    def set_elt(self, i, j, g, value):
        """Set element by index."""
        idx = self.__index_map[i][j][g]
        self.__internal_array[idx] = [value, [i, j, g]]

    def __iter__(self):
        """Return inerator.

        It provides all weights in structure as one sequence.
        """
        return WeightIterator(self.__internal_array)

    def get_string_representation(self, colored=False):
        """Return graceful string representation of weights structure.

        Output string may consist color tags (for output in terminal) if
        corresponding argument set to True.
        """
        res = ''
        imap = self.__index_map
        for i in range(1, len(imap)):
            res += '  Layer#{}\n'.format(i)
            for j in range(1, len(imap[i])):
                res += 'Unit#{}-{}:  '.format(i, j)
                for g in range(len(imap[i][j])):
                    idx = imap[i][j][g]
                    value, _ = self.__internal_array[idx]
                    if value:
                        str_val = '{:<10.5f}'.format(value)
                    else:
                        str_val = '{:<10}'.format('None')
                    if colored:
                        str_val = '\033[92m{}\033[0m'.format(str_val)
                    res += 'W#{}-{}-{}={} '.format(i, j, g, str_val)
                res += '\n'
        return res

    def __str__(self):
        """Return graceful string representation of weights structure."""
        return self.get_string_representation(True)

    def __len__(self):
        """Return length of weights sequence."""
        return len(self.__internal_array)

    def __getitem__(self, idx):
        """Return tuple [value, [i, j, g]]."""
        return self.__internal_array[idx]
