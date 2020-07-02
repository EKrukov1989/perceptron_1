"""Some tests for weightsrtucture."""

from unitstructure import UnitStructure


def __get_config():
    config = {}
    config['NumberOfInputUnits'] = 1
    config['LayersInfo'] = [
        {"NumberOfUnits": 2, "ActivationFunction": "tanh"},
        {"NumberOfUnits": 2, "ActivationFunction": "tanh"},
        {"NumberOfUnits": 1, "ActivationFunction": "linear"}]
    return config


def test_init():
    """Check initialization result.

    NOTICE: remember that unit structure ignore imagine unit for output layer
    """
    config = __get_config()
    U = UnitStructure(config)
    assert len(U) == 9


def test_get_set():
    """Check get-set public methods."""
    config = __get_config()
    U = UnitStructure(config)
    U.set_elt(1, 1, 42)
    assert U.get_elt(1, 1) == 42


def test_iteration():
    """Check forward and reverse interation through weight structure."""
    config = __get_config()
    U = UnitStructure(config)
    forward_counter = 0
    reverse_counter = 8

    CORRECT_INDICES = [[0, 0], [0, 1],
                       [1, 0], [1, 1], [1, 2],
                       [2, 0], [2, 1], [2, 2],
                       [3, 1]]

    for _, ij in U:
        assert CORRECT_INDICES[forward_counter] == ij
        forward_counter += 1
    assert forward_counter == 9

    for _, ij in reversed(U):
        assert CORRECT_INDICES[reverse_counter] == ij
        reverse_counter -= 1
    assert reverse_counter == -1


def test_layers():
    """Check layers initialization.

    Number for each layer must include imagine units even for output layer
    """
    config = __get_config()
    U = UnitStructure(config)
    assert U.get_layers() == [2, 3, 3, 2]


def test_imagine_init():
    """Check that all values were assigned."""
    config = __get_config()
    U = UnitStructure(config)
    U.init_imagine_units()
    for i in range(U.get_layers_num()):
        if i == (U.get_layers_num() - 1):
            assert U.get_elt(i, 0) is None
        else:
            assert U.get_elt(i, 0) == 1
