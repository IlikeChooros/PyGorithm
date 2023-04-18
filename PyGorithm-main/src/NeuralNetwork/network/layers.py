from .neuron import Neuron

# These are hidden and output layers, input neurons are just a list
class Layer:
    def __init__(self, number_of_neurons: int, input_connections: int) -> None:
        self.neurons = []
        self.__outputs = []
        self.output_values = []

        for loop in range(number_of_neurons):
            self.neurons.append(Neuron(input_connections)) # Creating a list of neurons in layer
            self.__outputs.append(float(0)) # The list of outputs of this layer
            self.output_values.append(float(0))

        self.inputs = [] 
        self.neurons_in_layer = number_of_neurons
        self.input_conn = input_connections
        
    def get_weight(self, neuron_idx, idx):
        return self.neurons[neuron_idx].weights[idx]
    
    def get_bias(self, neuron_idx):
        return self.neurons[neuron_idx].bias

    def __str__(self) -> str:
        ret = "\n"
        itr = 1
        for neuron in self.neurons:
            ret += f"Neuron {itr}\n"
            ret += str(neuron)
            ret += "\n"
            itr += 1
        return ret
    
    # Calculates and returns output values as a list, input values should be already set
    def calculate_output(self) -> list:
        for i in range(self.neurons_in_layer):
            self.neurons[i].input = self.inputs
            self.__outputs[i] = self.neurons[i].activation()

        return self.__outputs  
    
    
    def calculate_gradient(self, prev_layer, output_values: list):
        
        for i in range(self.neurons_in_layer):
            node_value = float(0)
            
            for neuron in range(prev_layer.neurons_in_layer):
                node_value += prev_layer.get_weight(neuron, i) * output_values[neuron]

            self.output_values[i] = self.neurons[i].calculate_gradient(node_value)

        return self


    def calculate_output_gradient(self, expected_values: list):
        for i in range(self.neurons_in_layer):
            self.output_values[i] = self.neurons[i].calculate_output_gradient(expected_values[i])
        
        return self
    
    def apply_gradient(self, learn_rate: float, batch_size: int):
        for neuron in self.neurons:
            neuron.apply_gradient(learn_rate, batch_size)

    
    # Calculates difference between single expected value and a value producted by the network
    def cost(self, expected_values: list) -> float:
        cost = float(0)

        for itr in range(self.neurons_in_layer):
            cost += self.neurons[itr].error(expected_values[itr])
        
        return cost
            

if __name__ == "__main__":
    print("\n")
    layers = Layer(3, 2)
    layers.inputs = [3,2] 
    layers.calculate_output()
    print(layers)
    print(f"Cost: {layers.cost([1, 0, 0])}")

    for i in range(10):
        layers.calculate_output()
        layers.calculate_output_gradient([1, 0, 0]).apply_gradient(1)
    
    print(layers)
    print(f"Cost: {layers.cost([1, 0, 0])}")
