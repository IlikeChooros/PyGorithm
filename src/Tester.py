import random

from data_converter import DataConverter
from NeuralNetwork import NeuralNetwork


def progress_bar(idx, total):
    lenght = 20

    done = round((idx+1)/total*lenght)

    togo = lenght - done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'\t\t\tProgress: {done_str}{togo_str} {round((idx+1)/total*100, 2)}% ', end='\r')
    



class Tester:
    def __init__(self, network: NeuralNetwork) -> None:
        self.__network = network
        self.learn_batch = []
    
    def teach(self):
        global progress_bar
        repeat = 50
        max_batch = len(self.learn_batch)*repeat
        itr = 0

        for i in range(repeat):
            for data in self.learn_batch:
                itr += 1

                self.__network.learn(data)
                print(f"Average Loss: {round(self.__network.loss(itr), 5)}   ", end='\r')

                if itr % repeat == 0:
                    progress_bar(itr, max_batch)
                    self.__network.apply(1.3, repeat)
                
                

            
    def print_input(self):

        x = float(input("Set x: "))
        y = float(input("Set y: "))

        self.__network.inputs = [x, y]

        self.__network.network_output()
        
        print(f"Network: {(self.__network.output[:])}")

        match self.__network.classify():
            case 1:
                print("X < Y")
            case 2:
                print("X > Y")

    
    def check(self):

        print("\n")

        self.print_input()
    
        while True:
            self.print_input()


    

    # Creates test, by making random points, setting output values via comparsion function (lambda)
    # Network should have 2 inputs and 2 outputs
    def create_point_test(self, path: str, comparsion_function):
        x, y = 0.0, 0.0

        with open(path, 'w') as file:

            for i in range(1000):
                
                x = random.randint(0, 10)*0.5
                y = random.randint(0, 10)*0.5


                string = str(x) + " " + str(y)
                if comparsion_function(x,y):
                    string += " 1 0\n"

                else:
                    string += " 0 1\n"

                file.write(string)

        


if __name__ == "__main__":

    data = DataConverter()
    
    tester = Tester(NeuralNetwork([2,50,50,2]))
    tester.create_point_test("src/tests/x_smaller_than_y.txt", lambda x,y: x < y)
    tester.learn_batch = data.list_to_Data(data.prepare_data_txt("src/tests/x_smaller_than_y.txt"), 2, 2)
    tester.teach()
    tester.check()
    