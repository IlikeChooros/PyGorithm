import random
import math

random.seed()



class Neuron:
    def __init__(self, input_connections: int):
        
        self.__weights = []

        # values between (-1,1)
        self.__bias = 1 - 2*random.random()
        self.__weights += [1 - 2*random.random() for i in range(input_connections)]

        self.__gradient_bias = float(0)
        self.__gradient_weights = [float(0) for i in range(input_connections)]

        self.__connections = input_connections
        self.__activation = float(0)

        self.input = []

    
    def __str__(self) -> str:
        ret = f"Bias: {self.__bias}\n"
        for i in range(self.__connections):
            ret += f"   {i}. Weight: {self.__weights[i]} \n"

        ret += f"Act: {self.__activation}\n"
        return ret
    
    # Calculate output value
    def activation(self) -> float: 
        output = float(0)
        for i in range(self.__connections):
            output += self.__weights[i] * self.input[i] + self.__bias

        # Using sigmoid function 1 / (e^-x + 1)
        self.__activation = 1 / (math.exp(-output) + 1)

        return self.__activation
    

    def apply_gradient(self, learn_rate: float) -> None:
        self.__bias -= self.__gradient_bias * learn_rate
        for i in range(self.__connections):
            self.__weights[i] -= self.__gradient_weights[i] * learn_rate

    
    # Should be optimized, using CALCULUS
    def calculate_gradient(self, expected_value: float) -> None:

        save_weight = float(0)
        save_bias = self.__bias

        original_error = self.error(expected_value)

        self.__bias += 0.0001
        self.activation()
        deltaCost = self.error(expected_value) - original_error

        self.__gradient_bias = deltaCost * 10000 # same as delataCost / 0.0001
        self.__bias = save_bias

        for i in range(self.__connections):
            original_error = self.error(expected_value)
            save_weight = self.__weights[i]

            self.__weights[i] += 0.0001
            self.activation()
            deltaCost = self.error(expected_value) - original_error

            self.__gradient_weights[i] = deltaCost * 10000
            self.__weights[i] = save_weight


    def error(self, expected_value: float) -> float:
            error = expected_value - self.__activation
            error *= error
            return error

if __name__ == "__main__":
    neuron = Neuron(2)
    neuron.input = [0.001, 0.2]
    neuron.activation()
    print(neuron)
    neuron.calculate_gradient(0.5)
    neuron.apply_gradient(2)
    neuron.activation()
    print(neuron)