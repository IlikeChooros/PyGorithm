import Neuron

# These are hidden layers, input neurons are just a list
class Layer:
    def __init__(self, number_of_neurons: int, input_connections: int) -> None:
        self.__neurons = []
        self.__outputs = []

        for loop in range(number_of_neurons):
            self.__neurons.append(Neuron.Neuron(input_connections)) # Creating a list of neurons in layer
            self.__outputs.append(float(0)) # The list of outputs of this layer

        self.inputs = [] 
        self.neurons_in_layer = number_of_neurons
        

    def __str__(self) -> str:
        ret = "\n"
        for neuron in self.__neurons:
            ret += str(neuron)
            ret += "\n"
        return ret
    
    # Calculates and returns output values as a list, input values should be already set
    def calculate_output(self) -> list:
        for i in range(self.neurons_in_layer):
            self.__neurons[i].input = self.inputs
            self.__outputs[i] = self.__neurons[i].activation()

        return self.__outputs  
    
    
    def calculate_gradient(self, expected_values: list) -> None:
        for i in range(self.neurons_in_layer):
            self.__neurons[i].calculate_gradient(expected_values[i])

    
    def apply_gradient(self, learn_rate: float) -> None:
        for neuron in self.__neurons:
            neuron.apply_gradient(learn_rate)

    
    # Calculates difference between single expected value and a value producted by the network
    def cost(self, expected_values: list) -> float:
        cost = float(0)

        for itr in range(self.neurons_in_layer):
            cost += self.__neurons[itr].error(expected_values[itr])
        
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
        layers.calculate_gradient([1, 0, 0])
        layers.apply_gradient(1.5)
    
    print(layers)
    print(f"Cost: {layers.cost([1, 0, 0])}")
