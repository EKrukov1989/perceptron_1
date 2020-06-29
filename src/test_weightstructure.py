"""Some tests for weightsrtucture."""

from weightstructure import WeightStructure
from weightstructure import WeightIterator


def __get_config():
    config = {}
    config['NumberOfInputUnits'] = 1
    config['LayersInfo'] = [
        {"NumberOfUnits": 2, "ActivationFunction": "tanh"},
        {"NumberOfUnits": 2, "ActivationFunction": "tanh"},
        {"NumberOfUnits": 1, "ActivationFunction": "linear"}]
    return config


def test_init():
    """Check initialization result."""
    config = __get_config()
    w = WeightStructure(config)
    assert len(w) == 13


def test_get_set():
    """Check get-set public methods."""
    config = __get_config()
    w = WeightStructure(config)
    w.set_elt(1, 1, 1, 42)
    assert w.get_elt(1, 1, 1) == 42


def test_iteration():
    """Check forward and reverse interation through weight structure."""
    config = __get_config()
    w = WeightStructure(config)
    forward_counter = 0
    reverse_counter = 12

    CORRECT_INDICES = [[1, 1, 0], [1, 1, 1],
                       [1, 2, 0], [1, 2, 1],
                       [2, 1, 0], [2, 1, 1], [2, 1, 2],
                       [2, 2, 0], [2, 2, 1], [2, 2, 2],
                       [3, 1, 0], [3, 1, 1], [3, 1, 2]]

    for _, [i, j, g] in w:
        assert CORRECT_INDICES[forward_counter] == [i, j, g]
        forward_counter += 1
    assert forward_counter == 13

    for _, [i, j, g] in reversed(w):
        assert CORRECT_INDICES[reverse_counter] == [i, j, g]
        reverse_counter -= 1
    assert reverse_counter == -1


def test_random_init():
    """Check that all values were assigned."""
    config = __get_config()
    w = WeightStructure(config)
    w.random_initialization()
    assert len(w) == 13
    for weight, _ in w:
        assert type(weight) == float
