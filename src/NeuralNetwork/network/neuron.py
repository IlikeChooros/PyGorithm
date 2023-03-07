import random
import math

class Neuron:
    def __init__(self, input_connections: int):
        
        self.weights = []

        # values between (-1,1)
        self.__bias = 1 - 2*random.random()
        self.weights += [1 - 2*random.random() for i in range(input_connections)]

        self.__gradient_bias = float(0)
        self.__gradient_weights = [float(0) for i in range(input_connections)]

        self.__connections = input_connections
        self.__activation = float(0)

        # partial dirivative: d(cost)/d(activation) * d(activation)/d(ouput)
        self.__output_const = float(0)

        self.input = []

    
    def __str__(self) -> str:
        ret = f"Bias: {self.__bias}\n"
        for i in range(self.__connections):
            ret += f"   {i}. Weight: {self.weights[i]} \n"

        ret += f"Act: {self.__activation}\n"
        return ret
    
    # Calculate output value
    def activation(self) -> float: 
        output = float(0)
        for i in range(self.__connections):
            output += self.weights[i] * self.input[i] + self.__bias

        # Using sigmoid function 1 / (e^-x + 1)
        self.__activation = 1 / (math.exp(-output) + 1)

        return self.__activation
    
    # Use after activation
    def calculate_output_gradient(self, expected_value: float) -> float:
        # dc/dw = dc/dA * dA/d(output) * d(output)/dw

        # dc/dA = d (Expected_value - Activation)^2 / d(Activation)
        #       = 2 * (Expected_value - Activation)

        # dA/d(output) = d( 1 / e^(-output) + 1)/d(output) = A(1 - A)

        # d(output)/dw = d(w*input + bias)/dw = input

        # Final answer dc/dw = 2 * (Exp - Act) * Act (1 - Act) * input

        self.__output_const = 2 * (expected_value - self.__activation) * self.__activation * (1 - self.__activation)

        for i in range(self.__connections):
            self.__gradient_weights[i] = self.__output_const * self.input[i]
        
        return self.__output_const
    

    def apply_gradient(self, learn_rate: float) -> None:
        self.__bias += self.__gradient_bias * learn_rate
        for i in range(self.__connections):
            self.weights[i] += self.__gradient_weights[i] * learn_rate

    
    # Using backpropagation
    def calculate_gradient(self, node_value):

        # For hidden layers
        # dc/dw(i) = output_const * Sum(w(i+1) * output_value(i+1)) * Ai * (1 - Ai) * input 
        # dc/db(i) = output_const * Sum(w(i+1) * output_value(i+1)) * Ai * (1- Ai)
        self.__output_const = self.__activation * (1 - self.__activation)

        self.__gradient_bias = node_value * self.__output_const

        for i in range(self.__connections):
            self.__gradient_weights[i] = node_value * self.__output_const * self.input[i]
        
        return self.__output_const


    def error(self, expected_value: float) -> float:
            error = expected_value - self.__activation
            error *= error
            return error

if __name__ == "__main__":
    neuron = Neuron(2)
    neuron.input = [0.5, 0.8]
    neuron.activation()
    print(neuron)
    print(neuron.error(1))
    print("")
    neuron.calculate_output_gradient(1)
    neuron.apply_gradient(1)
    neuron.activation()
    print(neuron)
    print(neuron.error(1))