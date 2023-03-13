from .network import Layer


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
    same neuron share the same bias

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

        self.__neural_net_sturct = neurons_in_layers

        self.__layers = []
        self.__layers += [Layer(neurons, inputs) for (neurons, inputs) in zip(hidden_layers, input_layers)]

        self.__output_layer = self.__layers[self.__number_of_layers-1]
        self.__average_loss = float(0)
        self.current_loss = float(0)

        self.inputs = []
        self.output = []

    # Starts learning process for a single data point

    def learn(self, data: Data):
        output_neurons = self.__layers[self.__number_of_layers-1].neurons_in_layer

        assert len(data.expect) == output_neurons, f"Invalid number of expected values: {len(data.expect)} : number of output neurons {output_neurons}"

        self.inputs = data.input
        self.network_output()

        prev_layer = self.__output_layer.calculate_output_gradient(data.expect)
        output_values = self.__output_layer.output_values

        self.current_loss = self.cost(data.expect)
        self.__average_loss += self.current_loss

        for reverse in range(self.__number_of_layers-2, -1, -1):
            prev_layer = self.__layers[reverse].calculate_gradient(prev_layer, output_values)
            output_values = prev_layer.output_values


    def apply(self, learnrate: float, batch_size: int):
        for layer in self.__layers:
            layer.apply_gradient(learnrate, batch_size)


    def cost(self, expect: list):
        return self.__output_layer.cost(expect)
    
    def loss(self, batch_size: int):
        return  self.__average_loss / batch_size


    # Calculates network output on given input
    def network_output(self) -> None:
        temp = self.inputs

        for layers in self.__layers:
            layers.inputs = temp
            temp = layers.calculate_output()

        self.output = temp

    
    def classify(self):
        return self.output.index(max(self.output)) + 1
    
    def __str__(self):
        ret = "\n"
        itr = 1
        for layer in self.__layers:
            ret += "----------------------\n"
            ret += f"Layer {itr}:"
            ret += str(layer)
            itr += 1
        return ret

    # Saving it in format:
    #  Network sturcture 
    #  (Neuron1): Bias " " Weight1 " " Weight2 " " ... + \n
    #  ...
    def save_to_txt(self, path: str):

        with open(path, 'w') as file:

            for numbers in self.__neural_net_sturct:
                file.write(str(numbers)+ " ")
            
            file.write("\n")

            weight = float(0)
            bias = float(0)

            for layer in range(self.__number_of_layers):
                for neuron in range(self.__layers[layer].neurons_in_layer):

                    bias = self.__layers[layer].get_bias(neuron)

                    file.write(str(bias))

                    for connection in range(self.__neural_net_sturct[layer]):
                        weight = self.__layers[layer].get_weight(neuron, connection)
                        file.write(" "+str(weight))

                    file.write("\n")
    

    def load_from_txt(self, path: str):
        f = open(path,"r")
        data = f.readlines()
        f.close()
        network = []
        for i in range(len(data)):
            network.append(data[i].split())
        for i in range(len(network)):
            for j in range(len(network[i])):
                network[i][j] = float(network[i][j])

        idx = 0

        for layer in range(self.__number_of_layers):
            for neuron_idx in range(int(network[0][layer+1])):
                idx +=1
                self.__layers[layer].neurons[neuron_idx].bias = network[idx][0]

                for connection in range(int(network[0][layer])):
                    self.__layers[layer].neurons[neuron_idx].weights[connection] = network[idx][connection+1]

        
        


if __name__ == "__main__":
    network = NeuralNetwork([2,10,3,2])
    network.save_to_txt("src/saved_networks/test.txt")
    network.load_from_txt("src/saved_networks/test.txt")
