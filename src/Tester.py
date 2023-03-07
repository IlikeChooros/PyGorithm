import random, data_converter

from NeuralNetwork import NeuralNetwork



class Tester:
    def __init__(self, network: NeuralNetwork) -> None:
        self.__network = network
        self.learn_batch = []
    
    def teach(self):
        
        for i in range(10):
            for data in self.learn_batch:
                self.__network.learn(data, 1)

    
    def check(self):

        x = float(input("Set x: "))
        y = float(input("Set y: "))
        self.__network.network_output()

        self.__network.inputs = [x, y]
        print("Network: "+str(self.__network.output[:]) + " X < Y  (1 0)")


    
        while True:
            x = float(input("Set x: "))
            y = float(input("Set y: "))
            self.__network.network_output()

            self.__network.inputs = [x, y]
            print("Network: "+str(self.__network.output[:]))


    

    # Creates test, by making random 100 points, setting output values via comparsion_function (lambda)
    # Network should have 2 inputs and 2 outputs
    def create_point_test(self, path: str, comparsion_function):
        x, y = 0.0, 0.0

        with open(path, 'w') as file:

            for i in range(1000):
                
                x = random.random()*5
                y = random.random()*5


                string = str(x) + " " + str(y)
                if comparsion_function(x,y):
                    string += " 1 0\n"

                else:
                    string += " 0 1\n"


                file.write(string)

        


if __name__ == "__main__":

    data = data_converter.DataConverter()
    
    tester = Tester(NeuralNetwork([2,100,2]))
    tester.create_point_test("src/tests/triangle.txt", lambda x,y: x < y)
    tester.learn_batch = data.list_to_Data(data.prepare_data_txt("src/tests/triangle.txt"), 2, 2)
    tester.teach()
    tester.check()
    