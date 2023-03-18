import random, os, time

from data_converter import DataConverter
from NeuralNetwork import NeuralNetwork


class Timer:
    times = []
    ptr = 0

    def prev_timer(self):
        self.ptr -= 1

    def next_timer(self):
        self.ptr += 1

    def add_timer(self):
        self.times.append(time.time())

    def reset(self):
        self.times[self.ptr] = time.time()

    def del_timer(self):
        self.times.pop(self.ptr)
    
    def print_delta_ms(self, append: str):
        print(f"{append} {round((time.time() - self.times[self.ptr])*1000, 2)} ms.", end='\r')

    def print_delta_s(self, append: str):
        print(f"{append} {round((time.time() - self.times[self.ptr]), 3)} s.", end='\r')
    
    def print_eta(self, append: str, count: int):
        print(f"{append} ETA: {round((time.time() - self.times[self.ptr])*count, 2)} s.", end='\r')


class Interface:

    start = 0
    end = 0

    def progress_bar(self, idx, total):
        lenght = 20

        done = round((idx+1)/total*lenght)

        togo = lenght - done

        done_str = '#'*int(done)
        togo_str = '-'*int(togo)

        print(f'\t\t\tProgress: {done_str}{togo_str} {round((idx+1)/total*100, 2)}% ', end='\r')
    
    def loss(self, loss):
        print(f"Average Loss: {round(loss, 5)}   ", end='\r')

    def average_correct(self, correct, average_correct, itr, repeat, append: str):
        print(f"{append}Correct: {round(correct/repeat * 100, 2)} % : ", end='\r')
        print(f"{append}\t\t {round(average_correct/itr * 100, 2)} %   ", end='\r')

    def print_eta(self, timer, delta):
        timer.reset()
        timer.prev_timer()

        timer.print_delta_s('\t\t\t\t\t\t\t\t\t\t\t\t\t\tBatch: ')
        timer.print_eta('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', delta)
        timer.reset()
        timer.next_timer()
    
    def print_sec(self, timer):
        timer.print_delta_ms('\t\t\t\t\t\t\t\t\t\t\t  Single: ')
        timer.reset()


class TestCreator:
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

    

class Tester:
    def __init__(self, network: NeuralNetwork) -> None:
        self.__network = network
        self.learn_batch = []
    
    def teach(self):
        repeat = 10
        timer = Timer()
        output = Interface()
        
        max_batch = len(self.learn_batch)*repeat
        itr = 0

        correct = 0
        average_correct = 0

        timer.add_timer()
        timer.next_timer()

        timer.add_timer()

        for i in range(repeat):


            for data in self.learn_batch:
                itr += 1

                self.__network.learn(data)
                output.loss(self.__network.loss(itr))

                if self.__network.is_correct:
                    correct += 1

                if itr % repeat == 0:
                    output.progress_bar(itr, max_batch)
                    self.__network.apply(1.3, repeat)
                    average_correct += correct

                    output.average_correct(correct, average_correct, itr, repeat, '\t\t\t\t\t\t\t\t')
                    output.print_sec(timer)
                    
                    correct = 0
            
            output.print_eta(timer, repeat - i)

                
            
    def print_input(self, compare):

        try:
            x = float(input("Set x: "))
            y = float(input("Set y: "))

            self.__network.inputs = [x, y]

            self.__network.network_output()
            
            print(f"Network: {(self.__network.output[:])} should be {compare(x,y)}")

        except KeyboardInterrupt:
            print("\nExiting the program...")
            os._exit(0)


    
    def check(self, comparsion_func):

        print("\n")

        self.print_input(comparsion_func)
    
        while True:
            self.print_input(comparsion_func)


    def save_network(self, path):
        self.__network.save_to_txt(path)
    

    def load_network(self, path):
        self.__network.load_from_txt(path)



        


if __name__ == "__main__":

    data = DataConverter()
    test_creator = TestCreator()
    
    tester = Tester(NeuralNetwork([2,15,15,2]))
    tester.load_network("src/saved_networks/net.txt")

    comparsion_func = lambda x,y: (x-2.5)*(x-2.5) < 1 - (y-2.5)*(y-2.5)

    test_creator.create_point_test("src/tests/point_test.txt", comparsion_func)
    tester.learn_batch = data.list_to_Data(data.prepare_data_txt("src/tests/point_test.txt"), 2, 2)
    tester.teach()
    tester.save_network("src/saved_networks/net.txt")
    tester.check(comparsion_func) 
    