"""Dummy network."""


class NeuralNetwork():
    """Imitation of normal network."""

    __configuration = None
    __network_trained = False

    def __init__(self, configuration):
        """Create MultilayerPerceptron with certain configuration."""
        self.__configuration = configuration
        pass

    def train(self, train_data):
        """Train network."""
        self.__network_trained = True
        pass

    def process(self, x):
        """Calculate output of network for certain x."""
        assert self.__network_trained
        return x

    def get_configure(self):
        """Return information about configuration of network."""
        pass

    def serialize_network(self):
        """Serialize configuration and clacluated weights.

        This required for repeated using of calcaulted values
        without repeating of long process of training.
        """
        pass

    def deserialize_network(self):
        """Deserialize configuration and clacluated weights."""
        pass
