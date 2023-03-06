import Layers
"""
Neural network stucture:

Input -> float list (not a layer)
Output -> float list (it is a layer)

Network:
    List of Layers

    As input -> list
    As output -> list (result of last layer activation)

Layers:
    number of neurons
    list of Neurons

    As input -> list 
    As output -> list (result of neuron activation)

Neurons:
    weight
    bias

    As input -> list
    As output -> float number (0 ; 1)

    Every input connection has its unique weight, but all connections to the
    same neuron have the same bias

    input1
      \\   \\
       \\    \\  weight (1,1)
        \\     \\
weight(1,2)\\     \\
            \\     neuron1 Activation( input[a] * weight[a] + bias1 )
              \\ //
              //\\
weight(2,1) //    \\
          //        \\
    input2 ========= neuron2 Activation( input[a] * weight[a] + bias2 )
            weight(2,2)  


""" 

# data-> list of data, expected_values -> expected neuron activation values
class Data:
    def __init__(self, data: list, expected_neuron_values: list):
        self.input = data
        self.expect = expected_neuron_values


class NeuralNetwork:

    # Last number in neurons_in_layers is number of output neurons, input neurons are list

    def __init__(self, neurons_in_layers: list):
        self.__number_of_layers = len(neurons_in_layers)-1

        hidden_layers = neurons_in_layers[1:]
        input_layers = neurons_in_layers[:-1]

        self.__layers = []
        self.__layers += [Layers.Layer(neurons, inputs) for (neurons, inputs) in zip(hidden_layers, input_layers)]

        self.__output_layer = self.__layers[self.__number_of_layers-1]

        self.inputs = []
        self.output = []

    # Starts learning process for a single data point

    def learn(self, data: Data, learnrate: float):
        output_neurons = self.__layers[self.__number_of_layers-1].neurons_in_layer

        assert len(data.expect) == output_neurons, f"Invalid number of expected values: {len(data.expect)} : number of output neurons {output_neurons}"

        self.inputs = data.input
        self.network_output()

        prev_layer = self.__output_layer.calculate_output_gradient(data.expect)
        output_values = self.__output_layer.output_values

        for reverse in range(output_neurons-2, -1, -1):
            prev_layer = self.__layers[reverse].calculate_gradient(prev_layer, output_values)
            output_values = prev_layer.output_values

        for layer in self.__layers:
            layer.apply_gradient(learnrate)

    def cost(self, data: Data):
        return self.__output_layer.cost(data.expect)

    # Calculates average difference between ALL expected values and values producted by the network
    def loss(self, expected_outputs: list) -> float:
        loss = float(0)
        for values in expected_outputs:
            self.network_output()
            loss += self.cost(values)
        
        return loss / len(expected_outputs)

    # Calculates network output on given input
    def network_output(self) -> None:
        temp = self.inputs

        for layers in self.__layers:
            layers.inputs = temp
            temp = layers.calculate_output()

        self.output = temp

    
    def classify(self):
        max_value = max(self.output)
        print(self.output[:])
        return self.output.index(max_value) + 1
    
    def __str__(self):
        ret = "\n"
        itr = 1
        for layer in self.__layers:
            ret += "----------------------\n"
            ret += f"Layer {itr}:"
            ret += str(layer)
            itr += 1
        return ret

if __name__ == "__main__":
    network = NeuralNetwork([2,3,2])
    network.learn(Data([4,3], [1,0]), 1.5)
    print(network)
    print(f"Cost {network.cost(Data([4,3], [1,0]))}")
    print(f"AI PICK: {network.classify()}")
    network.learn(Data([4,3], [1,0]), 1.5)
    network.learn(Data([4,3], [1,0]), 1.5)
    network.learn(Data([4,3], [1,0]), 1.5)
    print(network)
    print(f"Cost {network.cost(Data([4,3], [1,0]))}")
    print(f"AI PICK: {network.classify()}")

