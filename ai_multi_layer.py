import numpy
import scipy.special

class NeuralNetwork_multiLayer:
    def __init__(self, _nodes: list, learning_rate):
        self.nodes = _nodes
        self.learning_rate = learning_rate

        self.activation_function = lambda x: scipy.special.expit(x)

        self.weights = []

        self.weights.append(numpy.random.normal(0.0, pow(self.nodes[0], -0.5), (self.nodes[1], self.nodes[0])))

        weigth_layer = 1

        for nodes in self.nodes[1:-1]:
            self.weights.append(numpy.random.normal(0.0, pow(self.nodes[0], -0.5), (self.nodes[weigth_layer+1], self.nodes[weigth_layer])))
            weigth_layer += 1


    def train(self, input_list, target_list):
        targets = numpy.array(target_list, ndmin = 2).T

        _inputs = []
        _outputs = []
        layer_number = 0

        _inputs.append(numpy.array(input_list, ndmin = 2).T) 
        _outputs.append(self.activation_function(numpy.dot(self.weights[0], _inputs[0])))

        layer_number += 1


        for i in range(len(self.weights[1:])):
            _inputs.append(numpy.dot(self.weights[layer_number], _outputs[(layer_number-1)]))
            _outputs.append(self.activation_function(_inputs[layer_number]))
            layer_number += 1

        errors = []
        error_layer = 0
        errors.append(targets - _outputs[-1])

        error_layer += 1

        for i in range(len(self.nodes[1:])):
            errors.append(numpy.dot(numpy.transpose(self.weights[-error_layer]), errors[error_layer-1]))

            error_layer += 1

        correction_layer = 1

        self.weights[-1] += self.learning_rate * numpy.dot((errors[0] * _outputs[-1] * (1.0 - _outputs[-1])), numpy.transpose(_outputs[(-2)]))
        
        correction_layer += 1

        for i in range((len(self.nodes)-3)):
            self.weights[-correction_layer] += self.learning_rate * numpy.dot((errors[correction_layer-1] * _outputs[-correction_layer] * (1.0 - _outputs[-correction_layer])), numpy.transpose(_outputs[(-(correction_layer+1))]))
            correction_layer += 1

        self.weights[-correction_layer] += self.learning_rate * numpy.dot((errors[correction_layer-1] * _outputs[-correction_layer] * (1.0 - _outputs[-correction_layer])), numpy.transpose(_inputs[0]))

    def query(self, input_list):

        _inputs = []
        _outputs = []
        layer_number = 0

        _inputs.append(numpy.array(input_list, ndmin = 2).T) 
        _outputs.append(self.activation_function(numpy.dot(self.weights[0], _inputs[0])))

        layer_number += 1


        for i in range(len(self.weights[1:])):
            _inputs.append(numpy.dot(self.weights[layer_number], _outputs[(layer_number-1)]))
            _outputs.append(self.activation_function(_inputs[layer_number]))
            layer_number += 1

        return _outputs[-1]