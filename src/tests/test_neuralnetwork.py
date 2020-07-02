"""Some tests for neuralnetrowk."""

from network.neuralnetwork import NeuralNetwork


def __get_config():
    config = {}
    config['NumberOfInputUnits'] = 1
    config['LayersInfo'] = [
        {"NumberOfUnits": 2, "ActivationFunction": "tanh"},
        {"NumberOfUnits": 2, "ActivationFunction": "tanh"},
        {"NumberOfUnits": 1, "ActivationFunction": "linear"}]
    return config


def test_calculation():
    """Check possibiliy of calculation."""
    config = __get_config()
    net = NeuralNetwork(config)
    x = [0.1]
    y = net.process(x)
    assert type(y[0]) == float


def test_error_calc():
    """Check possibiliy of calculation."""
    config = __get_config()
    net = NeuralNetwork(config)
    err = net.error_function([[0.1], [0.2]])
    print(err)
    assert err >= 0


def test_backpropagation():
    """Check backpropagaion algorithm."""
    config = __get_config()
    net = NeuralNetwork(config)
    sample = [[0.5], [15]]
    D1 = net._calculate_gradient_numerically(sample)
    D2 = net._calculate_gradient_by_backpropagation(sample)
    for deriv_1, [i, j, g] in D1:
        deriv_2 = D2.get_elt(i, j, g)
        error = abs((deriv_2 - deriv_1) / deriv_2)
        assert error < 0.02
