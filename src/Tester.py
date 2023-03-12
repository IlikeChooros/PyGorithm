import random, os

from data_converter import DataConverter
from NeuralNetwork import NeuralNetwork


def progress_bar(idx, total):
    lenght = 20

    done = round((idx+1)/total*lenght)

    togo = lenght - done

    done_str = '#'*int(done)
    togo_str = '-'*int(togo)

    print(f'\t\t\tProgress: {done_str}{togo_str} {round((idx+1)/total*100, 2)}% ', end='\r')
    



class Tester:
    def __init__(self, network: NeuralNetwork) -> None:
        self.__network = network
        self.learn_batch = []
    
    def teach(self):
        global progress_bar
        repeat = 100
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
                
                
            
    def print_input(self, compare):

        try:
            x = float(input("Set x: "))
            y = float(input("Set y: "))

            self.__network.inputs = [x, y]

            self.__network.network_output()
            
            print(f"Network: {(self.__network.output[:])} should be {compare(x,y)}")

            match self.__network.classify():
                case 1:
                    print("X < Y")
                case 2:
                    print("X > Y")
        except KeyboardInterrupt:
            print("\nExiting the program...")
            os._exit(0)

    
    def check(self, comparsion_func):

        print("\n")

        self.print_input(comparsion_func)
    
        while True:
            self.print_input(comparsion_func)


    

    # Creates test, by making random points, setting output values via comparsion function (lambda)
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
            
            # Now create points to improve accuracy

            for i in range(500):
                x = random.random()*5
                
                if i%2 == 0:
                    y = x + 0.001
                else:
                    y = x - 0.001
                
                string = str(x) + " " + str(y)
                if comparsion_function(x,y):
                    string += " 1 0\n"

                else:
                    string += " 0 1\n"

                file.write(string)


        


if __name__ == "__main__":

    data = DataConverter()
    
    tester = Tester(NeuralNetwork([2,15,10,2]))

    comparsion_func = lambda x,y: y > x

    tester.create_point_test("src/tests/point_test.txt", comparsion_func)
    tester.learn_batch = data.list_to_Data(data.prepare_data_txt("src/tests/point_test.txt"), 2, 2)
    tester.teach()
    tester.check(comparsion_func)
    